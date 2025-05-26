import json
import time
import threading
from environment.node_template import Node
from environment.message_queue import register_node

with open("config.json", "r") as f:
    config = json.load(f)

nodes = []
id_to_node = {}

for node_conf in config['nodes']:
    node_id = node_conf['id']
    register_node(node_id)
    node = Node(node_id, config)
    nodes.append(node)
    id_to_node[node_id] = node

for node in nodes:
    threading.Thread(target=node.start, daemon=True).start()


## CRASH Simulation
def simulate_leader_crash():
    time.sleep(5)
    crash_node_id = max(id_to_node.keys())
    crashed_node = id_to_node[crash_node_id]
    print(f"\n***Simulating CRASH for Node {crash_node_id} ***\n")
    crashed_node.running = False

threading.Thread(target=simulate_leader_crash, daemon=True).start()

# Let the simulation run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation interrupted. Exiting...")
    for node in nodes:
        node.running = False
    time.sleep(1)
