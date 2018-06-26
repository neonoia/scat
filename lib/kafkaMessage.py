from confluent_kafka import Consumer, KafkaError
import re
import string

class kafkaMessage(object):

    def get_topic_messages(self, topics, server):
        '''
        Creates a keyword named "Get Topic Messages"
        This keyword takes two argument, the topic and the kafka server
        and returns a list messages inside the topic.
        '''

        settings = {
            'bootstrap.servers': server,
            'group.id': 'item-service',
            'client.id': 'client-1',
            'enable.auto.commit': False,
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'}
        }

        c = Consumer(settings)
        c.subscribe([topics])
        messages = []

        try:
            while True:
                msg = c.poll(0.1)
                if msg is None:
                    continue
                elif not msg.error():
                    temp = msg.value()
                    messages.append(temp)
                elif msg.error().code() == KafkaError._PARTITION_EOF:
                    break
                else:
                    print('Error occured: {0}'.format(msg.error().str()))
        except KeyboardInterrupt:
            pass
        finally:
            c.close()

        return messages

    def match_item_details(self, item, kafka):
        '''
        Creates a keyword named "Match Item Details"
        Search the item details in kafka messages list. 
        Returns boolean value whether the details are 
        present in kafka messages or not.
        '''
        if type(item) is int:
            return True

        item = str(item)
        item = item.lower()

        for msg in kafka:

            msg = str(msg)
            msg = msg.lower()
            if item in msg:
                return True

        return False

#k = kafkaMessage()
#s = k.get_topic_messages('SkuCreateRequested','10.99.143.96:9092')