import sqlite3
import time
from storage import JobStorage

class JobQueue:
    def __init__(self):
        self.storage = JobStorage()
    
    def enqueue(self, job_id, command, max_retries=3):
        conn = self.storage.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (id, command, max_retries)
            VALUES (?, ?, ?)
        ''', (job_id, command, max_retries))
        conn.commit()
        conn.close()
        print(f"✅ Enqueued job {job_id}: {command}")
    
    def get_next_job(self):
        conn = self.storage.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE state = 'pending' 
            ORDER BY created_at 
            LIMIT 1
        ''')
        job = cursor.fetchone()
        conn.close()
        return job
    
    def update_state(self, job_id, state):
        conn = self.storage.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jobs SET state = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (state, job_id))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        conn = self.storage.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT state, COUNT(*) FROM jobs GROUP BY state
        ''')
        stats = cursor.fetchall()
        conn.close()
        
        result = {'pending': 0, 'processing': 0, 'completed': 0, 'failed': 0, 'dead': 0}
        for state, count in stats:
            result[state] = count
        return result