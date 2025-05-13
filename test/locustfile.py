import time
from locust import HttpUser, task, between

class MainMapUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_main_map(self):
        self.client.get("/")
        time.sleep(1)
