from kafka import KafkaConsumer

class kafkaMessage(object):

    def get_topic_messages(self, topics, server):
        '''Creates a keyword named "Get Topic Messages"
        This keyword takes two arguments, the topic and the port
        '''
        messages = []
        consumer = KafkaConsumer(topics,bootstrap_servers=server,auto_offset_reset='earliest')
        # consumer.assign()
        for msg in consumer:
            messages.append(msg)

        return messages