from confluent_kafka import Consumer, KafkaError
from robot.api import logger
import time
import SkuEventMessage_pb2

def success(item):
    info = item + " exists in Kafka Topic"
    logger.info(info)

def fail(item):
    info = item + " does not exist in Kafka Topic"
    logger.console(info)
    logger.error(info)

def get_topic_messages(topics, server):
    '''
    This function takes two argument, the topic and the kafka server.
    Returns a list messages inside the topic.
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
                messages.append(msg.value())
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                break
            else:
                fail('Error occured: {0}'.format(msg.error().str()))
    except KeyboardInterrupt:
        pass
    finally:
        c.close()

    return messages

def match_kafka_item_details(items, topics, server):
    '''
    Creates a keyword named "Match Item Details"
    Search the item details in kafka messages list. 
    Returns boolean value whether the details are 
    present in kafka messages or not.
    '''

    kafka = get_topic_messages(topics,server)
    messages = SkuEventMessage_pb2.SkuEventMessage()

    row = len(items)
    col = len(items[0])
    logger.console("\n")

    for i in range (row):
        found = False
        timeout = time.time() + 30   # set timeout as 30s

        while not found:

            for msg in kafka:
                messages.ParseFromString(msg)
                if messages.HasField('data') and (items[i][0] == messages.data.code):
                    if check_message_details(messages.data, items[i]):
                        found = True
                        break

            if not found:
                # refetch messages
                kafka = get_topic_messages(topics,server)

            if time.time() > timeout:
                # error message
                fail(item)
                return False

    return True

def check_message_details(msg, item):
    score = 0
    sku = item[0]
    if (item[1] == msg.name):
        success(sku + ": " + item[1])
        score += 1
    if (item[2] == msg.specification):
        success(sku + ": " + item[2])
        score += 1
    if (item[3] == msg.uom):
        success(sku + ": " + item[3])
        score += 1
    if ((str(item[4])).lower() == (str(msg.type)).lower()):
        success(sku + ": " + item[4])
        score += 1
    if (item[5] == msg.handling_list):
        success(sku + ": " + item[5])
        score += 1
    if (item[6] == msg.size.inner.length):
        success(sku + ": " + str(item[6]))
        score += 1
    if (item[7] == msg.size.inner.width):
        success(sku + ": " + str(item[7]))
        score += 1
    if (item[8] == msg.size.inner.height):
        success(sku + ": " + str(item[8]))
        score += 1
    if (item[9] == msg.size.inner.weight):
        success(sku + ": " + str(item[9]))
        score += 1
    if (item[10] == msg.size.inner.size_category):
        success(sku + ": " + item[10])
        score += 1
    if (item[11] == msg.size.outer.length):
        success(sku + ": " + str(item[11]))
        score += 1
    if (item[12] == msg.size.outer.width):
        success(sku + ": " + str(item[12]))
        score += 1
    if (item[13] == msg.size.outer.height):
        success(sku + ": " + str(item[13]))
        score += 1
    if (item[14] == msg.size.outer.weight):
        success(sku + ": " + str(item[14]))
        score += 1
    if (item[15] == msg.size.outer.size_category):
        success(sku + ": " + str(item[15]))
        score += 1
    if (item[16] == msg.size.packages.length):
        success(sku + ": " + str(item[16]))
        score += 1
    if (item[17] == msg.size.packages.width):
        success(sku + ": " + str(item[17]))
        score += 1
    if (item[18] == msg.size.packages.height):
        success(sku + ": " + str(item[18]))
        score += 1
    if (item[19] == msg.size.packages.weight):
        success(sku + ": " + str(item[19]))
        score += 1
    if (item[20] == msg.size.packages.size_category):
        success(sku + ": " + str(item[20]))
        score += 1
        
    if (score == 20):
        logger.console("All " + str(sku) + " details are present in Kafka Broker.")
        return True
    else:
        fail("Some item details currently not present in Kafka Broker.")
        return False