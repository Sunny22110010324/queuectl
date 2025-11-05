# QueueCTL - Background Job Queue System

A CLI-based background job queue system with worker processes, retry mechanism, and Dead Letter Queue.

## Features
- ✅ Job queue with SQLite persistence
- ✅ Worker processes with parallel execution  
- ✅ Exponential backoff retries
- ✅ Dead Letter Queue (DLQ) for failed jobs
- ✅ CLI interface

##  How It Works
1. Jobs are enqueued via CLI and stored in SQLite database

2. Worker processes pick up pending jobs

3. Failed jobs are retried with exponential backoff

4. After max retries, jobs move to Dead Letter Queue

5. All job states persist across restarts

## Installation
git clone https://github.com/Sunny22110010324/queuectl.git

cd queuectl

pip install click

## Quick Start
```bash
# Install dependencies
pip install click

# Enqueue jobs
python queuectl.py enqueue "echo 'Hello World'"
python queuectl.py enqueue "sleep 5"

# Check status
python queuectl.py status

# Start workers
python queuectl.py start --count 2

# View failed jobs
python queuectl.py dlq list

# All Commands
python queuectl.py enqueue "command"      # Add job
python queuectl.py status                 # Show queue status
python queuectl.py list --state pending   # List jobs by state
python queuectl.py start --count 3        # Start workers
python queuectl.py dlq list               # View DLQ
