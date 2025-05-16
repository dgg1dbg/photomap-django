import time
from locust import HttpUser, task, constant

class MainMapUser(HttpUser):
    wait_time = constant(0)

    @task
    def load_main_map(self):
        self.client.get("/")
