# Installation Guide

This guide explains how to install and use the Fabric Spark Job wheel package.

## Quick Start

### 1. Install the Wheel

```bash
# Install the wheel directly
pip install dist/fabric_spark_job-1.0.0-py3-none-any.whl

# Or install from a remote location
pip install fabric-spark-job
```

### 2. Verify Installation

```bash
# Check if the command is available
fabric-spark-job --help

# Test the package import
python -c "import spark_job; print('Package installed successfully')"
```

### 3. Use the Job

```bash
# Run with graceful exit (for testing)
fabric-spark-job --mode graceful-exit

# Run indefinitely with busy loop
fabric-spark-job --mode busy-loop

# Run indefinitely with idle loop (5-second intervals)
fabric-spark-job --mode idle-loop --sleep-interval 5.0

# Fail with custom error
fabric-spark-job --mode fail --error-type ValueError --error-message "Test error"
```

## Microsoft Fabric Deployment

### Option 1: Upload Wheel File

1. Upload the wheel file (`fabric_spark_job-1.0.0-py3-none-any.whl`) to your Fabric workspace
2. In your Spark job definition:
   - **Main file**: `spark_job/cli.py`
   - **Arguments**: Add your desired command line arguments
   - **Dependencies**: The wheel will be automatically installed

### Option 2: Use as Library

1. Install the wheel in your Fabric environment
2. Import and use the `SparkJobRunner` class directly:

```python
from spark_job import SparkJobRunner
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MyJob").getOrCreate()
runner = SparkJobRunner(spark)

# Use the runner methods directly
runner.graceful_exit()
```

## Development Installation

For development work, install in editable mode:

```bash
# Clone the repository
git clone <repository-url>
cd fabric-spark-job

# Install in development mode
pip install -e .

# Run tests
python test_job.py
```

## Building from Source

```bash
# Install build dependencies
pip install -r requirements.txt

# Build the wheel
python build_wheel.py

# The wheel will be created in dist/
```

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure the wheel is installed correctly
   ```bash
   pip list | grep fabric-spark-job
   ```

2. **Import errors**: Check Python version compatibility (requires Python 3.7+)
   ```bash
   python --version
   ```

3. **Spark session issues**: In Microsoft Fabric, Spark is pre-configured
   - The job will automatically create a Spark session
   - No additional configuration needed

### Uninstalling

```bash
pip uninstall fabric-spark-job
```

## Package Information

- **Package Name**: `fabric-spark-job`
- **Version**: 1.0.0
- **Python Version**: 3.7+
- **Dependencies**: PySpark 3.4.0+
- **License**: MIT

## Support

For issues or questions:
1. Check the README.md for detailed usage instructions
2. Review the test_job.py for examples
3. Check the logs for detailed error information
