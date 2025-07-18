"""
Spark Job Runner Module

Contains the main SparkJobRunner class that handles different execution modes.
"""

import time
import logging
import random
from typing import Optional
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

logger = logging.getLogger(__name__)


class SparkJobRunner:
    """Main class to handle different Spark job execution modes."""

    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.counter = 0

    def create_sample_data(self) -> None:
        """Create sample data for demonstration purposes."""
        logger.info("Creating sample data...")

        # Create a simple DataFrame
        data = [
            ("Alice", 25, "Engineer"),
            ("Bob", 30, "Manager"),
            ("Charlie", 35, "Developer"),
            ("Diana", 28, "Analyst"),
            ("Eve", 32, "Designer"),
        ]

        schema = StructType(
            [
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True),
                StructField("role", StringType(), True),
            ]
        )

        df = self.spark.createDataFrame(data, schema)
        df.createOrReplaceTempView("employees")

        # Show the data
        logger.info("Sample data created:")
        df.show()

        # Perform a simple transformation
        result = df.filter(df.age > 25).select("name", "role")
        logger.info("Filtered data (age > 25):")
        result.show()

    def busy_loop(self) -> None:
        """Run an indefinite busy loop with Spark operations."""
        logger.info(
            "Starting busy loop mode - will run indefinitely with Spark operations"
        )

        try:
            while True:
                self.counter += 1

                # Perform some Spark operations
                if self.counter % 10 == 0:
                    # Create some random data every 10 iterations
                    random_data = [
                        (
                            f"User_{random.randint(1000, 9999)}",
                            random.randint(18, 65),
                            f"Role_{random.randint(1, 5)}",
                        )
                        for _ in range(5)
                    ]

                    temp_df = self.spark.createDataFrame(
                        random_data, ["name", "age", "role"]
                    )
                    count = temp_df.count()
                    logger.info(f"Iteration {self.counter}: Processed {count} records")

                # Simulate some computation
                _ = sum(range(1000))

                # Small delay to prevent overwhelming the system
                time.sleep(0.1)

        except KeyboardInterrupt:
            logger.info("Busy loop interrupted by user")
            raise

    def idle_loop(self, sleep_interval: float = 1.0) -> None:
        """Run an indefinite idle loop with periodic Spark operations."""
        logger.info(
            f"Starting idle loop mode - will run indefinitely with {sleep_interval}s intervals"
        )

        try:
            while True:
                self.counter += 1

                # Perform periodic Spark operations
                if self.counter % 30 == 0:  # Every 30 iterations
                    logger.info(
                        f"Idle loop iteration {self.counter}: Performing Spark operation"
                    )

                    # Simple Spark operation
                    result = self.spark.sql(
                        "SELECT COUNT(*) as total_employees FROM employees"
                    )
                    count = result.collect()[0]["total_employees"]
                    logger.info(f"Total employees in dataset: {count}")

                # Sleep for the specified interval
                time.sleep(sleep_interval)

        except KeyboardInterrupt:
            logger.info("Idle loop interrupted by user")
            raise

    def fail_with_error(self, error_type: str, error_message: str) -> None:
        """Fail the job with a specified error type and message."""
        logger.error(f"Job configured to fail with {error_type}: {error_message}")

        # Create some sample data first to show the job was working
        self.create_sample_data()

        # Raise the specified exception
        if error_type.lower() == "valueerror":
            raise ValueError(error_message)
        elif error_type.lower() == "runtimeerror":
            raise RuntimeError(error_message)
        elif error_type.lower() == "typeerror":
            raise TypeError(error_message)
        elif error_type.lower() == "indexerror":
            raise IndexError(error_message)
        elif error_type.lower() == "keyerror":
            raise KeyError(error_message)
        elif error_type.lower() == "zerodivisionerror":
            raise ZeroDivisionError(error_message)
        elif error_type.lower() == "filenotfounderror":
            raise FileNotFoundError(error_message)
        elif error_type.lower() == "permissionerror":
            raise PermissionError(error_message)
        elif error_type.lower() == "timeouterror":
            raise TimeoutError(error_message)
        elif error_type.lower() == "memoryerror":
            raise MemoryError(error_message)
        elif error_type.lower() == "recursionerror":
            raise RecursionError(error_message)
        else:
            # Default to RuntimeError for unknown error types
            raise RuntimeError(f"Unknown error type '{error_type}': {error_message}")

    def graceful_exit(self) -> None:
        """Run the job and exit gracefully."""
        logger.info("Starting graceful exit mode")

        # Create sample data
        self.create_sample_data()

        # Perform some meaningful work
        logger.info("Performing data analysis...")

        # Count total records
        total_count = self.spark.sql(
            "SELECT COUNT(*) as total FROM employees"
        ).collect()[0]["total"]
        logger.info(f"Total records processed: {total_count}")

        # Average age
        avg_age = self.spark.sql("SELECT AVG(age) as avg_age FROM employees").collect()[
            0
        ]["avg_age"]
        logger.info(f"Average age: {avg_age:.2f}")

        # Role distribution
        role_dist = self.spark.sql("""
            SELECT role, COUNT(*) as count
            FROM employees
            GROUP BY role
            ORDER BY count DESC
        """)
        logger.info("Role distribution:")
        role_dist.show()

        logger.info("Job completed successfully - exiting gracefully")
