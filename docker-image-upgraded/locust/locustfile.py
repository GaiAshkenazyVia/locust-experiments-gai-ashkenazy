from locust import HttpUser, task

class TestUser(HttpUser):

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task
    def hello_slow(self):
        self.client.get("/slow")
