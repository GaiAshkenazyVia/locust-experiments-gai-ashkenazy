# from locust import HttpUser, task
#
#
# class TestUser(HttpUser):
#
#     @task
#     def hello_world(self):
#         self.client.get("/hello")
#         self.client.get("/world")
#
#     @task
#     def hello_slow(self):
#         self.client.get("/slow")
from locust import HttpLocust, TaskSet, task


class UserTasks(TaskSet):

    @task
    def index(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task
    def stats(self):
        self.client.get("/slow")


class WebsiteUser(HttpLocust):
    task_set = UserTasks
