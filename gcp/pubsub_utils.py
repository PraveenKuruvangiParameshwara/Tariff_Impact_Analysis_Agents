from google.cloud import pubsub_v1

def publish_message(project_id, topic_id, data_dict):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(data_dict).encode('utf-8')
    future = publisher.publish(topic_path, data=data)
    return future.result()
