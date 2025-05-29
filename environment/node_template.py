import threading
import time
import random
from environment.message_queue import send_message, receive_message

class Node:
    def __init__(self, node_id, config):
        self.node_id = node_id
        self.config = config
        self.nodes = sorted([n['id'] for n in config['nodes']])
        self.heartbeat_interval = config['heartbeat_interval']
        self.timeout = config['timeout']
        self.leader_id = None
        self.last_heartbeat = time.time()
        self.running = True
        self.ok_received = False
        self.election_in_progress = False

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.heartbeat_check, daemon=True).start()
        self.start_election()

    def listen(self):
        while self.running:
            message = receive_message(self.node_id)
            if message:
                self.handle_message(message)
            time.sleep(0.05)

    def handle_message(self, message):
        msg_type = message.get('type')
        sender = message.get('sender')

        if msg_type == 'election':
            print(f"[Node {self.node_id}] Received election from {sender}")
            if self.node_id > sender:
                send_message(sender, {'type': 'ok', 'sender': self.node_id})
                self.start_election()

        elif msg_type == 'ok':
            print(f"[Node {self.node_id}] Received OK from {sender}")
            self.ok_received = True

        elif msg_type == 'coordinator':
            self.leader_id = sender
            self.last_heartbeat = time.time()
            print(f"[Node {self.node_id}] New leader is Node {self.leader_id}")


        elif msg_type == 'heartbeat':
            if sender == self.leader_id:
                self.last_heartbeat = time.time()
                print(f"[Node {self.node_id}] Heartbeat received from leader {sender}") 

    def start_election(self):
        self.election_start_time = time.time()
        if self.election_in_progress:
            return

        self.election_in_progress = True
        self.ok_received = False
        time.sleep(random.uniform(0.1, 0.3))
        print(f"[Node {self.node_id}] Starting election")

        higher_nodes = [n for n in self.nodes if n > self.node_id]
        for node_id in higher_nodes:
            send_message(node_id, {'type': 'election', 'sender': self.node_id})

        # Wait for OK or timeout
        wait_time = 2
        start = time.time()
        while time.time() - start < wait_time:
            if self.ok_received:
                break
            time.sleep(0.1)

        if not self.ok_received:
            self.leader_id = self.node_id
            self.announce_coordinator()
        else:
            # Wait for leader announcement
            wait_leader = 3
            while time.time() - start < wait_time + wait_leader:
                if self.leader_id is not None:
                    break
                time.sleep(0.1)

        self.election_in_progress = False

    def announce_coordinator(self):

        duration = time.time() - self.election_start_time
        print(f"[Node {self.node_id}] I am the new leader  (Election took: {duration:.2f} seconds)")
        for node_id in self.nodes:
            if node_id != self.node_id:
                send_message(node_id, {'type': 'coordinator', 'sender': self.node_id})

    def send_heartbeats(self):
        for nid in self.nodes:
            if nid != self.node_id:
                send_message(nid, {'type': 'heartbeat', 'sender': self.node_id})


    def heartbeat_check(self):
        while self.running:
            if self.node_id == self.leader_id:
                self.send_heartbeats()
            else:
                if time.time() - self.last_heartbeat > self.timeout:
                    print(f"[Node {self.node_id}] Leader {self.leader_id} timeout. Starting new election.")
                    self.start_election()
            time.sleep(self.heartbeat_interval)

