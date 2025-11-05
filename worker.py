import time
import subprocess
from job_queue import JobQueue

class Worker:
    def __init__(self, worker_id=1):
        self.worker_id = worker_id
        self.queue = JobQueue()
        self.running = True
    
    def process_job(self, job):
        job_id, command, state, attempts, max_retries, created_at, updated_at = job
        
        try:
            # Mark job as processing
            self.queue.update_state(job_id, 'processing')
            print(f"👷 Worker {self.worker_id} processing: {command}")
            
            # Execute command
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.queue.update_state(job_id, 'completed')
                print(f"✅ Worker {self.worker_id}: Completed job {job_id}")
            else:
                # Handle failure
                self.handle_failure(job_id, attempts, max_retries)
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Worker {self.worker_id}: Job {job_id} timed out")
            self.handle_failure(job_id, attempts, max_retries)
        except Exception as e:
            print(f"🚨 Worker {self.worker_id}: Error {e}")
            self.handle_failure(job_id, attempts, max_retries)
    
    def handle_failure(self, job_id, attempts, max_retries):
        new_attempts = attempts + 1
        
        if new_attempts >= max_retries:
            self.queue.update_state(job_id, 'dead')
            print(f"💀 Worker: Job {job_id} moved to DLQ after {new_attempts} attempts")
        else:
            # Update attempts and keep as pending for retry
            conn = self.queue.storage.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE jobs SET attempts = ?, state = 'pending', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_attempts, job_id))
            conn.commit()
            conn.close()
            
            delay = 2 ** new_attempts  # Exponential backoff
            print(f"🔄 Worker: Job {job_id} failed, retry in {delay}s (attempt {new_attempts}/{max_retries})")
    
    def start(self):
        print(f"👷 Worker {self.worker_id} started")
        while self.running:
            job = self.queue.get_next_job()
            if job:
                self.process_job(job)
            else:
                time.sleep(1)  # Wait for new jobs