import grpc
import pubsub_pb2
import pubsub_pb2_grpc
import time
from threading import Thread

def publish(stub):
    while True:
        topic = input("Enter topic to publish (or 'q' to quit): ")
        if topic.lower() == 'q':
            break
        content = input("Enter message content: ")
        ttl = int(input("Enter message TTL in seconds: "))
        
        # Create and send a publish request
        message = pubsub_pb2.Message(topic=topic, content=content, ttl=ttl)
        request = pubsub_pb2.PublishRequest(message=message)
        stub.Publish(request)
        print(f"Published message to topic '{topic}'")

def subscribe(stub):
    topic = input("Enter topic to subscribe: ")
    request = pubsub_pb2.SubscribeRequest(topic=topic)
    # Stream messages from the subscribed topic
    for message in stub.Subscribe(request):
        print(f"Received message on topic '{message.topic}': {message.content}")

def run():
    # Create a gRPC channel and stub
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pubsub_pb2_grpc.PubSubServiceStub(channel)
        
        # Start a separate thread for subscribing
        subscribe_thread = Thread(target=subscribe, args=(stub,))
        subscribe_thread.start()
        
        # Run the publish function in the main thread
        publish(stub)
        
        # Wait for the subscribe thread to finish
        subscribe_thread.join()

if __name__ == '__main__':
    run()