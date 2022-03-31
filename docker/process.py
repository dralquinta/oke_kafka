#!/usr/bin/python3

import io
import json
from confluent_kafka import Consumer
from confluent_kafka import Producer, KafkaError  
import certifi
import traceback
import logging
import time
import random
import re
import datetime
from helpers.PropertyHandler import get_config_data
from helpers.Printer import debug


__REGION=get_config_data('artifact_config', 'stream.region')
__ORIGIN_STREAM=get_config_data('artifact_config', 'stream.origin')
__DESTINATION_STREAM=get_config_data('artifact_config', 'stream.destination')
__TENANCY_NAME=get_config_data('artifact_config', 'stream.tenancy')
__STREAMPOOL_OCID=get_config_data('artifact_config', 'stream.pool_ocid')
__OCI_USERNAME=get_config_data('artifact_config', 'stream.username')
__SASL_USERNAME=__TENANCY_NAME+'/'+__OCI_USERNAME+'/'+__STREAMPOOL_OCID
__SASL_TOKEN=get_config_data('artifact_config', 'stream.sasl_token')
delivered_records = 0  



def __main__(region, sasl_username, sasl_token, origin_stream, destination_stream):
    before=time.time()
    topic = origin_stream
    conf = {  
        'bootstrap.servers': 'cell-1.streaming.'+region+'.oci.oraclecloud.com', 
        'security.protocol': 'SASL_SSL',       
        'ssl.ca.location': certifi.where(),   
        'sasl.mechanism': 'PLAIN',
        'sasl.username': sasl_username,  
        'sasl.password': sasl_token,  
        'group.id':'group-0',
        'api.version.request': False,
        'session.timeout.ms': 6000,
    }  

    # Create Consumer instance
    consumer = Consumer(conf)

    # Subscribe to topic
    consumer.subscribe([topic])

    # Process messages
    try:
        while True:
            msg = consumer.poll(1.0)            
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                info_msg="Waiting for message or event/error in poll()"
                print(info_msg)
                logging.info(info_msg)
                continue
            elif msg.error():
                print(msg)
                logging.error(msg)
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = "Null" if msg.key() is None else msg.key().decode('utf-8')
                record_value = msg.value().decode('utf-8')
                returnable_value = "key: "+ record_key + " value: " + record_value
                response = { "message": returnable_value, "time": str(to_ms(time.time()-before))+" ms", "status": "SUCCESS", "date": format_date(datetime.datetime.now()) }
                logging.info(response)
                if response['status'] == "SUCCESS":
                        oci_producer(destination_stream, response, sasl_username, sasl_token, region)    
                
    except Exception as e:
        print(e.with_traceback())
    finally:
        print("Leave group and commit final offsets")
        consumer.close()    
  


def oci_producer(destination_stream, message, sasl_username, sasl_token, region):    
    topic = destination_stream
    conf = {  
        'bootstrap.servers': 'cell-1.streaming.'+region+'.oci.oraclecloud.com', 
        'security.protocol': 'SASL_SSL',      
        'ssl.ca.location': certifi.where(),               
        'sasl.mechanism': 'PLAIN',
        'sasl.username': sasl_username,  
        'sasl.password': sasl_token,  
        'session.timeout.ms': 6000,
    }  
    producer = Producer(**conf)  
    
    
    
    record_key = "messageKey" + str(random.randint(1, 1000))
    record_value = "messageValue" + str(message)  
    info_message = "Producing record: {}\t{}".format(record_key, record_value)
    print(info_message)  
    logging.info(info_message)
    producer.produce(topic, key=record_key, value=record_value, on_delivery=acked)      
    producer.poll(0) 
    producer.flush() 
            
def to_ms(seconds):
    return seconds * 1000.0

def acked(err, msg):  
    global delivered_records  
    """Delivery report handler called on  
        successful or failed delivery of message """  
    if err is not None:  
        print("Failed to deliver message: {}".format(err))  
    else:  
        delivered_records += 1  
        
        
def format_date(date):
    #use this example to return formatted date: Thu, 31 Mar 2022 02:59:53 GMT
    return date.strftime("%a, %d %b %Y %H:%M:%S GMT")   
    
def to_ms(seconds):
    return seconds * 1000.0   
    
    
__main__(__REGION, __SASL_USERNAME, __SASL_TOKEN, __ORIGIN_STREAM, __DESTINATION_STREAM)