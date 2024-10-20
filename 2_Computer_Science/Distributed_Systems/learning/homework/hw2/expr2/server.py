import time
from concurrent import futures
import grpc
import pubsub_pb2
import pubsub_pb2_grpc

class PubSubServicer(pubsub_pb2_grpc.PubSubServiceServicer):
    def __init__(self):
        # Initialize a dictionary to store topics and their messages
        self.topics = {}

    def Subscribe(self, request, context):
        topic = request.topic
        if topic not in self.topics:
            self.topics[topic] = []
        
        while True:
            current_time = int(time.time())
            # Remove expired messages
            self.topics[topic] = [msg for msg in self.topics[topic] if msg.timestamp + msg.ttl > current_time]
            
            # Yield all messages for the subscribed topic
            for message in self.topics[topic]:
                yield message
            time.sleep(1)  # Check for new messages every second

    def Publish(self, request, context):
        message = request.message
        # Set the current timestamp for the message
        message.timestamp = int(time.time())
        
        if message.topic not in self.topics:
            self.topics[message.topic] = []
        
        # Add the new message to the topic
        self.topics[message.topic].append(message)
        return pubsub_pb2.Empty()

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pubsub_pb2_grpc.add_PubSubServiceServicer_to_server(PubSubServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()