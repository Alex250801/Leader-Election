from queue import Queue
from threading import Lock

# Global registry of queues for each node
message_queues = {}
queue_lock = Lock()

def register_node(node_id):
    with queue_lock:
        if node_id not in message_queues:
            message_queues[node_id] = Queue()

def send_message(receiver_id, message):
    with queue_lock:
        if receiver_id in message_queues:
            message_queues[receiver_id].put(message)

def receive_message(node_id):
    with queue_lock:
        queue = message_queues.get(node_id)
    if queue:
        try:
            return queue.get(timeout=0.1)
        except:
            return None
    return None



