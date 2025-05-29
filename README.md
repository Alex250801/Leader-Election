## Leader Election using Bully Algorithm

##  Features

- Bully algorithm for leader election
- Heartbeat messages from the leader
- Simulated node crashes and recoveries
- Message-passing via internal thread-safe queues
- Simple logging to show election and heartbeat flow
- Runtime measurement of leader election process

## Requirements

- Python 3.10+
- No external libraries needed (uses only built-in Python modules like `threading`, `queue`, `time`, etc.)

---
## ▶️ How to Run

1. **Clone or Download the Repository**

```bash
git clone https://github.com/your-repo-name/leader-election.git
cd leader-election
```

2. **Check or Edit Node Config**
```
{
  "nodes": [
    {"id": 1},
    {"id": 2},
    {"id": 3}
  ]
}
```

3. **Run the simulation**
```
python3 setup_test.py
```
You should now be able to see the election starting.





