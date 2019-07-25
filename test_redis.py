from redis import Redis
import rq

queue = rq.Queue('AppFlaskLogin', connection=Redis.from_url('redis://'))
job = queue.enqueue('app.tasks.example', 23)
print(job.get_id())
print(job.is_finished)