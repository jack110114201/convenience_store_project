import KafkaAPI


if __name__ == '__main__':
    data = {'ip': '123456789', 'user_id': '00002156', 'name': 'Nametest', 'age': 55, 'MARITAL': 'unknow',
            'INCOME': 'www', 'HH_COMP': '15K',
            'photo_url': 'https:ppp:ppp'}
    KafkaAPI.kafkaProducer('topictest','addtest',data)