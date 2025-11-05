import click
import time
import threading
import json
from job_queue import JobQueue
from worker import Worker

@click.group()
def cli():
    """QueueCTL - Background Job Queue System"""
    pass

@cli.command()
@click.argument('command')
@click.option('--job-id', default=None, help='Custom job ID')
@click.option('--max-retries', default=3, help='Maximum retry attempts')
def enqueue(command, job_id, max_retries):
    """Enqueue a new job"""
    queue = JobQueue()
    job_id = job_id or f"job_{int(time.time())}"
    
    queue.enqueue(job_id, command, max_retries)

@cli.command()
def status():
    """Show queue status"""
    queue = JobQueue()
    stats = queue.get_stats()
    
    click.echo("📊 Queue Status:")
    click.echo(f"   Pending: {stats['pending']}")
    click.echo(f"   Processing: {stats['processing']}")
    click.echo(f"   Completed: {stats['completed']}")
    click.echo(f"   Failed: {stats['failed']}")
    click.echo(f"   Dead: {stats['dead']}")

@cli.command()
@click.option('--state', default='pending', help='Filter by state')
def list(state):
    """List jobs by state"""
    queue = JobQueue()
    conn = queue.storage.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, command, state, attempts, max_retries, created_at
        FROM jobs WHERE state = ? ORDER BY created_at
    ''', (state,))
    
    jobs = cursor.fetchall()
    conn.close()
    
    if jobs:
        click.echo(f"📋 Jobs with state '{state}':")
        for job in jobs:
            click.echo(f"   {job[0]}: {job[1]} (attempts: {job[3]}/{job[4]})")
    else:
        click.echo(f"📭 No jobs with state '{state}'")

@cli.command()
@click.option('--job-id', help='Specific job ID')
def show(job_id):
    """Show job details in JSON format"""
    queue = JobQueue()
    conn = queue.storage.get_connection()
    cursor = conn.cursor()
    
    if job_id:
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
    else:
        cursor.execute('SELECT * FROM jobs ORDER BY created_at DESC LIMIT 1')
    
    job = cursor.fetchone()
    conn.close()
    
    if job:
        job_data = {
            "id": job[0],
            "command": job[1],
            "state": job[2],
            "attempts": job[3],
            "max_retries": job[4],
            "created_at": job[5],
            "updated_at": job[6]
        }
        click.echo(json.dumps(job_data, indent=2))
    else:
        click.echo("Job not found")

workers = []

@cli.command()
@click.option('--count', default=1, help='Number of workers to start')
def start(count):
    """Start worker processes"""
    global workers
    workers = []
    
    for i in range(count):
        worker = Worker(worker_id=i+1)
        workers.append(worker)
        # Start worker in background thread
        thread = threading.Thread(target=worker.start)
        thread.daemon = True
        thread.start()
        print(f"🚀 Started worker {i+1}")
    
    click.echo(f"🎯 {count} workers running. Press Ctrl+C to stop.")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("🛑 Stopping workers...")
        for worker in workers:
            worker.running = False

@cli.group()
def dlq():
    """Dead Letter Queue commands"""
    pass

@dlq.command()
def list():
    """List DLQ jobs"""
    queue = JobQueue()
    conn = queue.storage.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, command, attempts, max_retries, created_at
        FROM jobs WHERE state = 'dead' ORDER BY created_at
    ''')
    
    jobs = cursor.fetchall()
    conn.close()
    
    if jobs:
        click.echo("💀 Dead Letter Queue:")
        for job in jobs:
            click.echo(f"   {job[0]}: {job[1]} (failed {job[2]}/{job[3]} times)")
    else:
        click.echo("📭 DLQ is empty")

if __name__ == '__main__':
    cli()