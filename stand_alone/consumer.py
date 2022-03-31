from confluent_kafka import Consumer
import certifi


__REGION='sa-santiago-1'
__STREAM_NAME='receive'
__TENANCY_NAME='ecrcloud'
__STREAMPOOL_OCID='ocid1.streampool.oc1.sa-santiago-1.amaaaaaatwfhi7yann7kjkdd4ftxo6xjzutflmqvb7za3xovrm4nc6qwmxia'
__OCI_USERNAME='ecrcloud/oracleidentitycloudservice/denny.alquinta@oracle.com'
__SASL_USERNAME=__OCI_USERNAME+'/'+__STREAMPOOL_OCID
__SASL_TOKEN='T_YUSe3W7VIbMui2kbj:'

if __name__ == '__main__':

    topic = __STREAM_NAME  
    conf = {  
        'bootstrap.servers': 'cell-1.streaming.sa-santiago-1.oci.oraclecloud.com', #usually of the form cell-1.streaming.<region>.oci.oraclecloud.com:9092  
        'security.protocol': 'SASL_SSL',       
        'ssl.ca.location': certifi.where(),   
        'sasl.mechanism': 'PLAIN',
        'sasl.username': __SASL_USERNAME,  # from step 2 of Prerequisites section
        'sasl.password': __SASL_TOKEN,  # from step 7 of Prerequisites section
        'group.id':'group-0',
        'api.version.request': False,
        'session.timeout.ms': 6000,
        
    }  

    # Create Consumer instance
    print(__SASL_USERNAME)
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
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print(msg)
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = "Null" if msg.key() is None else msg.key().decode('utf-8')
                record_value = msg.value().decode('utf-8')
                print("Consumed record with key "+ record_key + " and value " + record_value)
    except Exception as e:
        print(e.with_traceback())
    finally:
        print("Leave group and commit final offsets")
        consumer.close()