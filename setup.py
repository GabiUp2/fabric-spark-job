#!/usr/bin/env python3
"""
Setup script for the PySpark Job wheel package.
"""

from setuptools import setup, find_packages
import os


# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [
            line.strip() for line in fh if line.strip() and not line.startswith("#")
        ]


setup(
    name="fabric-spark-job",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A configurable PySpark job for Microsoft Fabric with different execution modes",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fabric-spark-job",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "fabric-spark-job=spark_job:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
    keywords="pyspark, microsoft-fabric, data-processing, spark-jobs",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fabric-spark-job/issues",
        "Source": "https://github.com/yourusername/fabric-spark-job",
        "Documentation": "https://github.com/yourusername/fabric-spark-job#readme",
    },
)
