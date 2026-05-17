class JobNotFoundException(Exception):
   def __init__(self, job_id: int):
      self.job_id = job_id