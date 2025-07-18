#!/usr/bin/env python3
"""
Build script for creating the PySpark Job wheel package.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def clean_build_dirs():
    """Clean build and dist directories."""
    dirs_to_clean = ["build", "dist", "*.egg-info"]

    for dir_name in dirs_to_clean:
        if "*" in dir_name:
            # Handle glob patterns
            for path in Path(".").glob(dir_name):
                if path.is_dir():
                    print(f"Removing {path}")
                    shutil.rmtree(path)
        else:
            path = Path(dir_name)
            if path.exists():
                print(f"Removing {path}")
                shutil.rmtree(path)


def build_wheel():
    """Build the wheel package."""
    print("Building wheel package...")

    try:
        # Build the wheel
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel"],
            capture_output=True,
            text=True,
            check=True,
        )

        print("✅ Wheel built successfully!")
        print(result.stdout)

        # List the created wheel
        dist_dir = Path("dist")
        if dist_dir.exists():
            wheels = list(dist_dir.glob("*.whl"))
            if wheels:
                print(f"\n📦 Created wheel: {wheels[0].name}")
                return wheels[0]

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build wheel: {e}")
        print(f"Error output: {e.stderr}")
        return None


def install_wheel(wheel_path):
    """Install the wheel for testing."""
    print(f"\nInstalling wheel: {wheel_path.name}")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", str(wheel_path)],
            capture_output=True,
            text=True,
            check=True,
        )

        print("✅ Wheel installed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install wheel: {e}")
        print(f"Error output: {e.stderr}")
        return False


def test_installation():
    """Test that the installation works."""
    print("\nTesting installation...")

    try:
        # Test importing the package
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import spark_job; print('✅ Package imported successfully')",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        print(result.stdout)

        # Test the command line interface
        result = subprocess.run(
            [sys.executable, "-m", "spark_job.cli", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )

        if "Execution mode" in result.stdout:
            print("✅ Command line interface works!")
        else:
            print("⚠️  Command line interface may have issues")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Installation test failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main build process."""
    print("🚀 Starting PySpark Job Wheel Build")
    print("=" * 50)

    # Clean previous builds
    print("Cleaning previous builds...")
    clean_build_dirs()

    # Build wheel
    wheel_path = build_wheel()
    if not wheel_path:
        return 1

    # Install wheel
    if not install_wheel(wheel_path):
        return 1

    # Test installation
    if not test_installation():
        return 1

    print("\n" + "=" * 50)
    print("🎉 Wheel build completed successfully!")
    print(f"📦 Wheel file: {wheel_path}")
    print("\nTo install in another environment:")
    print(f"pip install {wheel_path}")
    print("\nTo use the command:")
    print("fabric-spark-job --help")

    return 0


if __name__ == "__main__":
    sys.exit(main())
