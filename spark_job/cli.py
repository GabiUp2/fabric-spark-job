"""
Command Line Interface Module

Contains the argument parsing and main entry point for the Spark job.
"""

import argparse
import sys
import logging
from pyspark.sql import SparkSession
from spark_job.job_runner import SparkJobRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="PySpark Job for Microsoft Fabric with configurable execution modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run indefinitely with busy loop
  fabric-spark-job --mode busy-loop

  # Run indefinitely with idle loop (sleep 2 seconds)
  fabric-spark-job --mode idle-loop --sleep-interval 2.0

  # Fail with ValueError
  fabric-spark-job --mode fail --error-type ValueError --error-message "Custom error occurred"

  # Graceful exit
  fabric-spark-job --mode graceful-exit
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["busy-loop", "idle-loop", "fail", "graceful-exit"],
        required=True,
        help="Execution mode for the Spark job",
    )

    parser.add_argument(
        "--sleep-interval",
        type=float,
        default=1.0,
        help="Sleep interval in seconds for idle-loop mode (default: 1.0)",
    )

    parser.add_argument(
        "--error-type",
        choices=[
            "ValueError",
            "RuntimeError",
            "TypeError",
            "IndexError",
            "KeyError",
            "ZeroDivisionError",
            "FileNotFoundError",
            "PermissionError",
            "TimeoutError",
            "MemoryError",
            "RecursionError",
        ],
        help="Type of exception to raise in fail mode",
    )

    parser.add_argument(
        "--error-message",
        default="Job failed as requested",
        help="Error message to include in the exception (default: 'Job failed as requested')",
    )

    return parser.parse_args()


def main():
    """Main entry point for the Spark job."""
    args = parse_arguments()

    logger.info("Starting PySpark Job")
    logger.info(f"Execution mode: {args.mode}")

    # Initialize Spark session
    # Note: In Microsoft Fabric, the Spark session is typically pre-configured
    try:
        spark = SparkSession.builder.appName("FabricSparkJob").getOrCreate()

        logger.info(f"Spark session initialized: {spark.version}")

        # Create job runner
        job_runner = SparkJobRunner(spark)

        # Execute based on mode
        if args.mode == "busy-loop":
            job_runner.busy_loop()

        elif args.mode == "idle-loop":
            job_runner.idle_loop(args.sleep_interval)

        elif args.mode == "fail":
            if not args.error_type:
                logger.error("Error type must be specified for fail mode")
                sys.exit(1)
            job_runner.fail_with_error(args.error_type, args.error_message)

        elif args.mode == "graceful-exit":
            job_runner.graceful_exit()

        else:
            logger.error(f"Unknown mode: {args.mode}")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Job interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Job failed with exception: {type(e).__name__}: {str(e)}")
        raise
    finally:
        try:
            if "spark" in locals():
                spark.stop()
                logger.info("Spark session stopped")
        except Exception as e:
            logger.warning(f"Error stopping Spark session: {e}")


if __name__ == "__main__":
    main()
