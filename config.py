class Config:
    DEFAULT_MAX_RETRIES = 3
    BACKOFF_BASE = 2  # For exponential backoff: 2^attempts
    WORKER_POLL_INTERVAL = 1  # seconds
    
    @classmethod
    def set_max_retries(cls, value):
        cls.DEFAULT_MAX_RETRIES = value
    
    @classmethod
    def set_backoff_base(cls, value):
        cls.BACKOFF_BASE = value