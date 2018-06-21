from confluent_kafka import Consumer, KafkaError

class kafkaMessage(object):

    def get_topic_messages(self, topics, server):
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
                # print(msg)
                if msg is None:
                    continue
                elif not msg.error():
                    messages.append(msg.value())
                    # print('Received message: {0}'.format(msg.value()))
                elif msg.error().code() == KafkaError._PARTITION_EOF:
                    # print('End of partition reached {0}/{1}'
                    #    .format(msg.topic(), msg.partition()))
                    break
                else:
                    print('Error occured: {0}'.format(msg.error().str()))
        except KeyboardInterrupt:
            pass
        finally:
            c.close()

        return messages

    def match_file_with_kafka(self, sku, kafka):

        result = []
        for sku_id in sku:

            found = False
            for msg in kafka:
                if sku_id in msg:
                    found = True
            if not found:
                return False
        
        return True

        
            
