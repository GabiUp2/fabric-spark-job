# PySpark Job for Microsoft Fabric

A configurable PySpark job that can be deployed to Microsoft Fabric with different execution modes controlled by command line arguments.

## Features

- **Indefinite Busy Loop**: Continuously performs Spark operations with minimal sleep
- **Indefinite Idle Loop**: Runs with configurable sleep intervals and periodic Spark operations
- **Controlled Failure**: Fails with custom error types and messages
- **Graceful Exit**: Performs data analysis and exits cleanly

## Usage

### Command Line Arguments

| Argument | Required | Choices | Description |
|----------|----------|---------|-------------|
| `--mode` | Yes | `busy-loop`, `idle-loop`, `fail`, `graceful-exit` | Execution mode for the job |
| `--sleep-interval` | No | Float | Sleep interval in seconds for idle-loop mode (default: 1.0) |
| `--error-type` | No* | Various exception types | Type of exception to raise in fail mode |
| `--error-message` | No | String | Error message for fail mode (default: "Job failed as requested") |

*Required when `--mode` is `fail`

### Available Error Types

- `ValueError`
- `RuntimeError`
- `TypeError`
- `IndexError`
- `KeyError`
- `ZeroDivisionError`
- `FileNotFoundError`
- `PermissionError`
- `TimeoutError`
- `MemoryError`
- `RecursionError`

## Examples

### Run Indefinitely with Busy Loop
```bash
python spark_job.py --mode busy-loop
```

### Run Indefinitely with Idle Loop (2-second intervals)
```bash
python spark_job.py --mode idle-loop --sleep-interval 2.0
```

### Fail with Custom Error
```bash
python spark_job.py --mode fail --error-type ValueError --error-message "Data validation failed"
```

### Graceful Exit
```bash
python spark_job.py --mode graceful-exit
```

## Microsoft Fabric Deployment

### Job Definition Parameters

When creating a Spark job definition in Microsoft Fabric, you can pass the command line arguments as parameters:

1. **Main file**: `spark_job.py`
2. **Arguments**: Add the desired command line arguments in the job definition

### Example Job Definitions

#### Busy Loop Job
```
Arguments: --mode busy-loop
```

#### Idle Loop Job (5-second intervals)
```
Arguments: --mode idle-loop --sleep-interval 5.0
```

#### Failure Test Job
```
Arguments: --mode fail --error-type RuntimeError --error-message "Simulated failure for testing"
```

#### Graceful Exit Job
```
Arguments: --mode graceful-exit
```

## Job Behavior

### Busy Loop Mode
- Continuously performs Spark operations
- Creates random data every 10 iterations
- Minimal sleep (0.1 seconds) to prevent system overload
- Suitable for testing resource utilization

### Idle Loop Mode
- Runs with configurable sleep intervals
- Performs Spark operations every 30 iterations
- More resource-friendly than busy loop
- Suitable for long-running monitoring jobs

### Fail Mode
- Creates sample data to demonstrate the job was working
- Raises the specified exception with custom message
- Useful for testing error handling and monitoring

### Graceful Exit Mode
- Creates sample employee data
- Performs data analysis (counts, averages, distributions)
- Exits cleanly after completing the analysis
- Suitable for batch processing jobs

## Logging

The job includes comprehensive logging that will appear in the Microsoft Fabric job logs:

- Job start/stop events
- Execution mode information
- Spark operation results
- Error details (when applicable)
- Performance metrics

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd fabric-spark-job

# Install in development mode
pip install -e .
```

### Building a Wheel

```bash
# Install build dependencies
pip install -r requirements.txt

# Build the wheel
python build_wheel.py

# Or build manually
python -m build --wheel
```

The wheel will be created in the `dist/` directory.

### Installing the Wheel

```bash
# Install the wheel
pip install dist/fabric_spark_job-*.whl

# Use the command
fabric-spark-job --help
```

## Dependencies

- Python 3.7+
- PySpark 3.4.0+

## Development

### Project Structure

```
fabric-spark-job/
├── spark_job/           # Main package
│   ├── __init__.py      # Package initialization
│   ├── job_runner.py    # SparkJobRunner class
│   └── cli.py          # Command line interface
├── setup.py            # Package setup
├── pyproject.toml      # Modern Python packaging
├── requirements.txt    # Dependencies
├── build_wheel.py      # Build script
└── README.md          # This file
```

### Building for Distribution

```bash
# Clean and build
python build_wheel.py

# The script will:
# 1. Clean previous builds
# 2. Build the wheel
# 3. Install it for testing
# 4. Verify the installation
```

## Notes

- The job is designed to work with Microsoft Fabric's pre-configured Spark environment
- No additional Spark configuration is required
- The job handles Spark session lifecycle automatically
- All exceptions are properly logged before being re-raised
- The job can be interrupted gracefully with Ctrl+C
- The package can be installed as a wheel for easy distribution
