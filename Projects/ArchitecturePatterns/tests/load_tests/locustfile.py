from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)  # Wait between 1 and 2 seconds between tasks
    
    @task(2)
    def get_health(self):
        self.client.get("/health")
    
    @task(1)
    def create_item(self):
        self.client.post("/items/", params={"name": "load_test_item"})
    
    @task(3)
    def get_items(self):
        self.client.get("/items/") 