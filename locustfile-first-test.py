from locust import HttpUser, task

class WebsiteUser(HttpUser):
    # this class will be used to simulate user scenario
    @task
    def hello_world(self):
        # assume that user will just land at home path
        self.client.get("/")

