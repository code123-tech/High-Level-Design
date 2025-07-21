from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URLs
PRIMARY_DB_URL = os.getenv("PRIMARY_DB_URL", "postgresql://postgres:postgres@primary-db:5432/postgres")
STANDBY_DB_URL = os.getenv("STANDBY_DB_URL", "postgresql://postgres:postgres@standby-db:5432/postgres")

# Create Base class for declarative models
Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        # Initialize engines
        self.primary_engine = create_engine(PRIMARY_DB_URL)
        self.standby_engine = create_engine(STANDBY_DB_URL)
        
        # Create session factories
        self.PrimarySession = sessionmaker(autocommit=False, autoflush=False, bind=self.primary_engine)
        self.StandbySession = sessionmaker(autocommit=False, autoflush=False, bind=self.standby_engine)

    def check_primary_health(self):
        """Check if primary database is healthy"""
        try:
            with self.PrimarySession() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Primary database health check failed: {e}")
            return False

    def check_standby_health(self):
        """Check if standby database is healthy"""
        try:
            with self.StandbySession() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Standby database health check failed: {e}")
            return False

    def get_write_session(self):
        """Get a session for write operations (always primary)"""
        return self.PrimarySession()

    def get_read_session(self):
        """Get a session for read operations (try primary first, fallback to standby)"""
        try:
            if self.check_primary_health():
                return self.PrimarySession()
        except Exception as e:
            logger.warning(f"Failed to get primary session: {e}")

        try:
            if self.check_standby_health():
                return self.StandbySession()
        except Exception as e:
            logger.error(f"Failed to get standby session: {e}")
            raise

    def init_db(self):
        """Initialize database schema"""
        Base.metadata.create_all(bind=self.primary_engine)

# Create global instance
db_manager = DatabaseManager() 