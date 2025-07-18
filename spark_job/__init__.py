"""
Fabric Spark Job Package

A configurable PySpark job for Microsoft Fabric with different execution modes.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .job_runner import SparkJobRunner
from .cli import main

__all__ = ["SparkJobRunner", "main"]
