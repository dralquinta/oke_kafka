from confluent_kafka import Producer, KafkaError  
import certifi


__REGION='sa-santiago-1'
__STREAM_NAME='send'
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
        'api.version.request': False,
    }  
  
   # Create Producer instance  
    producer = Producer(**conf)  
    delivered_records = 0  
  
   # Optional per-message on_delivery handler (triggered by poll() or flush())  
   # when a message has been successfully delivered or permanently failed delivery after retries.  
    def acked(err, msg):  
        global delivered_records  
        """Delivery report handler called on  
            successful or failed delivery of message """  
        if err is not None:  
            print("Failed to deliver message: {}".format(err))  
        else:  
            delivered_records += 1  
            print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))  

    for n in range(2):  
        record_key = "messageKey" + str(n)  
        record_value = "messageValue" + str(n)  
        print("Producing record: {}\t{}".format(record_key, record_value))  
        producer.produce(topic, key=record_key, value=record_value, on_delivery=acked)  
        # p.poll() serves delivery reports (on_delivery) from previous produce() calls.  
        producer.poll(0)  

    producer.flush()  
    print("{} messages were produced to topic {}!".format(delivered_records, topic))