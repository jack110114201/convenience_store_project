import sys
import datetime
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import json

# 用來接收從 Consumer instance 發出的 error 訊息
def error_cb(err):
    sys.stderr.write(f'Error: {err}')

def try_decode_utf8(data):
    return data.decode('utf-8') if data else None

# 當發生 commit時 被呼叫
def print_commit_result(err, partitions):
    if err:
        print(f'Failed to commit offsets: {err}: {partitions}')
    else:
        for p in partitions:
            print(f'Committed offsets for: {p.topic}-{p.partition} [offset={p.offset}]')

# kafka Producer-API
def kafkaProducer(topicname, key, data): #給予 topicName/keyName/data
    props = {'bootstrap.servers': '3.112.128.223',
            'error_cb': error_cb}
    producer = Producer(props)
    topicName = topicname
    dataJsonStr = json.dumps(data)
    try:
        print('Start sending messages ...')   
        # time_start = int(round(time.time() * 1000))      
        # dataJsonStr = json.dumps(data)
        producer.produce(topicName,
                         key=str(key), 
                         value=dataJsonStr)
        producer.poll(0)                    # 呼叫 poll 來讓 client 程式去檢查內部的 Buffer, 並觸發 callback                
        # time_spend = int(round(time.time() * 1000)) - time_start
        # print(f'Throughput  : {msgCount / time_spend * 1000} msg/sec')

    except BufferError as e:
        # 錯誤處理
        sys.stderr.write(f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again\n')
    except Exception as e:
        sys.stderr.write(str(e))

    producer.flush(10)
    print('Message sending completed!')

# kafka Consumer-API
def kafkaconsumer(topicname):#給予 topicName
    props = {
            'bootstrap.servers': '3.112.128.223',         # Kafka 集群在那裡? (置換成要連接的 Kafka 集群)
            'group.id': 'getdata',                         # ConsumerGroup
            'auto.offset.reset': 'earliest',               # 是否從這個 ConsumerGroup 尚未讀取的 partition/offset 開始讀
            'enable.auto.commit': True,                    # 是否啟動自動 commit
            'auto.commit.interval.ms': 5000,               # 自動 commit 的 interval
            'on_commit': print_commit_result,              # 設定接收 commit 訊息的 callback 函數
            'error_cb': error_cb                           # 設定接收 error 訊息的 callback 函數
        }
    consumer = Consumer(props)
    topicName = topicname
    consumer.subscribe([topicName])
    try:
        while True:
            # 請求 Kafka 把新的訊息吐出來
            records = consumer.consume(num_messages=500, timeout=5.0)  # 批次讀取
            if not records:
                continue
            for record in records:
                if not record:
                    continue

                # 檢查是否有錯誤
                if record.error() and record.error().code() != KafkaError._PARTITION_EOF:
                    raise KafkaException(record.error())
                else:
                    # 取出相關的 metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    msg_key = try_decode_utf8(record.key())
                    msg_value = try_decode_utf8(record.value())
                    print('{}-{}-{} : ({} , {})'.format(topic, partition, offset, msg_key, msg_value))

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(str(e))
    finally:
        #關掉 Consumer 實例的連線
        consumer.close()
