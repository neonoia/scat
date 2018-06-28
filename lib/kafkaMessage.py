from confluent_kafka import Consumer, KafkaError
from robot.api import logger

def success(item):
    info = item + " exists in Kafka Topic"
    logger.info(info)

def fail(item):
    info = item + " does not exist in Kafka Topic"
    logger.error(info)

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

    def match_kafka_item_details(self, row, col, items, kafka):
        '''
        Creates a keyword named "Match Item Details"
        Search the item details in kafka messages list. 
        Returns boolean value whether the details are 
        present in kafka messages or not.
        '''

        for i in range (row):

            for j in range (col):
                
                item = items[i][j]
                
                if type(item) is int:
                    success(str(item))
                else:
                    item = str(item)
                    item = item.lower()
                    found = False

                    for msg in kafka:
                        msg = str(msg)
                        msg = msg.lower()
                        if item in msg:
                            found = True
                            success(item)
                            break

                if not found:
                    fail(item)
                    return False

        return True

#k = kafkaMessage()
#s = k.get_topic_messages('SkuCreateRequested','10.99.143.96:9092')