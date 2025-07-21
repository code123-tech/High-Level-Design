import requests
import time
import docker
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FailoverTest:
    def __init__(self):
        self.api_url = "http://localhost:8888"
        self.docker_client = docker.from_env()
        self.db_container_name = "single-node-db-1"

    def create_test_item(self):
        """Create a test item and return its ID"""
        try:
            response = requests.post(
                f"{self.api_url}/items/",
                params={"name": f"failover_test_{datetime.now().timestamp()}"}
            )
            response.raise_for_status()
            return response.json()["id"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create test item: {e}")
            return None

    def check_api_health(self):
        """Check if the API is healthy"""
        try:
            response = requests.get(f"{self.api_url}/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def simulate_db_failure(self):
        """Simulate database failure by stopping the container"""
        try:
            container = self.docker_client.containers.get(self.db_container_name)
            logger.info("Stopping database container...")
            container.stop()
            return True
        except docker.errors.NotFound:
            logger.error(f"Container {self.db_container_name} not found")
            return False
        except Exception as e:
            logger.error(f"Failed to stop database: {e}")
            return False

    def restore_db(self):
        """Restore the database by starting the container"""
        try:
            container = self.docker_client.containers.get(self.db_container_name)
            logger.info("Starting database container...")
            container.start()
            return True
        except Exception as e:
            logger.error(f"Failed to start database: {e}")
            return False

    def run_failover_test(self):
        """Run the complete failover test"""
        logger.info("Starting failover test...")

        # Create initial test item
        item_id = self.create_test_item()
        if not item_id:
            logger.error("Failed to create initial test item")
            return False

        # Check initial health
        if not self.check_api_health():
            logger.error("API is not healthy before starting the test")
            return False

        # Simulate database failure
        if not self.simulate_db_failure():
            return False

        # Check API health during failure
        time.sleep(5)  # Wait for failure to propagate
        unhealthy = not self.check_api_health()
        logger.info(f"API health check during failure: {'Failed as expected' if unhealthy else 'Unexpectedly healthy'}")

        # Restore database
        if not self.restore_db():
            return False

        # Wait for recovery
        recovery_timeout = 30
        start_time = time.time()
        recovered = False

        while time.time() - start_time < recovery_timeout:
            if self.check_api_health():
                recovered = True
                break
            time.sleep(1)

        if recovered:
            logger.info(f"System recovered in {time.time() - start_time:.2f} seconds")
        else:
            logger.error("System failed to recover within timeout")

        return recovered

def main():
    test = FailoverTest()
    success = test.run_failover_test()
    logger.info(f"Failover test {'succeeded' if success else 'failed'}")

if __name__ == "__main__":
    main() 