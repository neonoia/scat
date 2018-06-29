from confluent_kafka import Consumer, KafkaError
from robot.api import logger
import time

def success(item):
    info = item + " exists in Kafka Topic"
    logger.console(info)
    logger.info(info)

def fail(item):
    info = item + " does not exist in Kafka Topic"
    logger.error(info)

def get_topic_messages(topics, server):
    '''
    This function takes two argument, the topic and the kafka server
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
                fail('Error occured: {0}'.format(msg.error().str()))
    except KeyboardInterrupt:
        pass
    finally:
        c.close()

    return messages

def match_kafka_item_details(row, col, items, topics, server):
    '''
    Creates a keyword named "Match Item Details"
    Search the item details in kafka messages list. 
    Returns boolean value whether the details are 
    present in kafka messages or not.
    '''

    timeout = time.time() + 60
    kafka = get_topic_messages(topics,server)

    for i in range (row):
        for j in range (col):
            
            item = items[i][j]
            if type(item) is not int:
                item = str(item)
                item = item.lower()
                found = False           # set the flag

                while (not found):
                    for msg in kafka:
                        msg = str(msg)
                        msg = msg.lower()
                        if item in msg:
                            found = True
                            if (j == 0):
                                success(item)
                            break

                    if not found:
                        # refetch messages
                        kafka = get_topic_messages(topics,server)

                    if time.time() > timeout:
                        # error message
                        fail(item)
                        break

    return True