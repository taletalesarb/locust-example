from locust import HttpUser, task, between
import json


class WebsiteUser(HttpUser):
    # we assume someone who is browsing the website,
    # generally has some waiting time (between
    # 5 and 10 seconds)
    wait_time = between(5, 10)

    def on_start(self):
        # start by waiting so that the simulated users
        # won't all arrive at the same time
        self.wait()
        # assume all users arrive at the index page
        self.hello_world()
        # assume all users will login
        self.login()

    def login(self):
        response = self.client.post("/login", data={"username": "user", "password": "pass"})
        self.token = response.json()["access_token"]

    @task(1)
    def hello_world(self):
        self.client.get("/")

    @task(5)
    def auth_get(self):
        self.client.get("/protected-get", headers={"Authorization": f"Bearer {self.token}"})

    @task(5)
    def auth_post(self):
        self.client.post(
            "/protected-post/test-path-1?param=test-param-1",
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            json={
                "name": "name-1",
                "description": "description-1",
                "price": 0,
                "tax": 0
            }
        )