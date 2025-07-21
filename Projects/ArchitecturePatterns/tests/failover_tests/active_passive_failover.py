import requests
import time
import docker
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_URL = "http://localhost:8889"
ITEMS_ENDPOINT = f"{API_URL}/items/"
HEALTH_ENDPOINT = f"{API_URL}/health"
DB_STATUS_ENDPOINT = f"{API_URL}/database/status"

def check_api_health():
    """Check the health of the API and return the active database"""
    try:
        response = requests.get(HEALTH_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return None

def get_database_status():
    """Get detailed status of both databases"""
    try:
        response = requests.get(DB_STATUS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get database status: {e}")
        return None

def create_test_item(name="test_item", description="test description"):
    """Create a test item and return its data"""
    try:
        response = requests.post(ITEMS_ENDPOINT, params={"name": name, "description": description})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to create test item: {e}")
        return None

def get_items():
    """Get all items and return which database served the request"""
    try:
        response = requests.get(ITEMS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get items: {e}")
        return None

def stop_primary_db():
    """Stop the primary database container"""
    try:
        client = docker.from_env()
        container = client.containers.get('architecturepatterns-primary-db-1')
        container.stop()
        logger.info("Primary database stopped")
        return True
    except Exception as e:
        logger.error(f"Failed to stop primary database: {e}")
        return False

def start_primary_db():
    """Start the primary database container"""
    try:
        client = docker.from_env()
        container = client.containers.get('architecturepatterns-primary-db-1')
        container.start()
        logger.info("Primary database started")
        return True
    except Exception as e:
        logger.error(f"Failed to start primary database: {e}")
        return False

def run_failover_test():
    """Run a complete failover test scenario"""
    logger.info("Starting failover test...")

    # Step 1: Check initial health
    logger.info("Step 1: Checking initial health...")
    initial_health = check_api_health()
    if not initial_health:
        logger.error("Initial health check failed")
        return False
    logger.info(f"Initial health: {initial_health}")

    # Step 2: Create test item
    logger.info("Step 2: Creating test item...")
    item = create_test_item()
    if not item:
        logger.error("Failed to create test item")
        return False
    logger.info(f"Created item: {item}")

    # Step 3: Stop primary database
    logger.info("Step 3: Stopping primary database...")
    if not stop_primary_db():
        logger.error("Failed to stop primary database")
        return False
    
    # Wait for failover
    time.sleep(5)

    # Step 4: Check health after primary failure
    logger.info("Step 4: Checking health after primary failure...")
    failover_health = check_api_health()
    if not failover_health:
        logger.error("Health check after failover failed")
        return False
    logger.info(f"Health after failover: {failover_health}")

    # Step 5: Try to read items from standby
    logger.info("Step 5: Reading items from standby...")
    items_result = get_items()
    if not items_result:
        logger.error("Failed to read items from standby")
        return False
    logger.info(f"Read items from {items_result['database']}")

    # Step 6: Start primary database
    logger.info("Step 6: Starting primary database...")
    if not start_primary_db():
        logger.error("Failed to start primary database")
        return False

    # Wait for primary to recover
    time.sleep(10)

    # Step 7: Final health check
    logger.info("Step 7: Final health check...")
    final_health = check_api_health()
    if not final_health:
        logger.error("Final health check failed")
        return False
    logger.info(f"Final health: {final_health}")

    logger.info("Failover test completed successfully!")
    return True

if __name__ == "__main__":
    success = run_failover_test()
    sys.exit(0 if success else 1) 