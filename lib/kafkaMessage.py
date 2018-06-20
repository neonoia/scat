from kafka import KafkaConsumer

class kafkaMessage(object):

    def get_topic_messages(self, topics, server):
        '''Creates a keyword named "Get Topic Messages"
        This keyword takes two arguments, the topic and the port
        '''
        consumer = KafkaConsumer(topics,bootstrap_servers=server,consumer_timeout_ms=10000)
        # consumer.assign()
        for message in consumer:
            print ("%s key=%s value=%s" % (message.topic,message.key,
                                                message.value))
                                                
        consumer.close()

if __name__ == "__main__":
    n = kafkaMessage()
    test = 'StorageCreateRequested'
    lc = "10.99.143.96:9092"
    print("test")
    n.get_topic_messages(test,lc)