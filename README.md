#  Leader Election in Distributed Systems – Bully Algorithm Simulation

This project simulates a **distributed leader election algorithm** using the **Bully Algorithm**. It demonstrates how nodes in a distributed system elect a coordinator, send heartbeats, and handle failure scenarios such as leader crashes.

## Features

- Bully algorithm for leader election
- Heartbeat messages from the leader
- Simulated node crashes and recoveries
- Message-passing via internal thread-safe queues
- Simple logging to show election and heartbeat flow
- Runtime measurement of leader election process

---

## ⚙️ Requirements

- Python 3.10+
- No external libraries needed (uses only built-in Python modules like `threading`, `queue`, `time`, etc.)

---

## ▶️ How to Run

1. **Clone or Download the Repository**

```bash
git clone https://github.com/your-repo-name/leader-election.git
cd leader-election
```

2. **Modifiy the *config.json* (OPTIONAL)**
```
{
  "nodes": [
    {"id": 1, "port": 5001},
    {"id": 2, "port": 5002},
    {"id": 3, "port": 5003}
  ],
  "heartbeat_interval": 5,
  "timeout": 5
}
```
You can modify the nodes id, add nodes, and set different times for *heartbeat_interval* and *timeout*.

3. ✅ **Run the simulation**
```
python3 setup_test.py
```
You should now be able to see the election having place.



