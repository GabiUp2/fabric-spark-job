#!/usr/bin/env python3
"""
Test script for the PySpark job.
This script tests the job functionality without running indefinitely.
"""

import subprocess
import sys
import time


def test_graceful_exit():
    """Test the graceful exit mode."""
    print("Testing graceful exit mode...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "spark_job.cli", "--mode", "graceful-exit"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("✅ Graceful exit test passed")
            print("Output:", result.stdout)
        else:
            print("❌ Graceful exit test failed")
            print("Error:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Graceful exit test timed out")
        return False

    return True


def test_fail_mode():
    """Test the fail mode with different error types."""
    print("\nTesting fail mode...")

    error_types = ["ValueError", "RuntimeError", "TypeError"]

    for error_type in error_types:
        print(f"Testing {error_type}...")
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "spark_job.cli",
                    "--mode",
                    "fail",
                    "--error-type",
                    error_type,
                    "--error-message",
                    f"Test {error_type} error",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                print(f"✅ {error_type} test passed (expected failure)")
                if error_type in result.stderr:
                    print(f"✅ Error type correctly identified in output")
                else:
                    print(f"⚠️  Error type not found in stderr output")
            else:
                print(f"❌ {error_type} test failed (expected non-zero exit code)")
                return False
        except subprocess.TimeoutExpired:
            print(f"❌ {error_type} test timed out")
            return False

    return True


def test_argument_parsing():
    """Test argument parsing and help."""
    print("\nTesting argument parsing...")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "spark_job.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0 and "Execution mode" in result.stdout:
            print("✅ Help output test passed")
        else:
            print("❌ Help output test failed")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Help output test timed out")
        return False

    return True


def test_invalid_arguments():
    """Test invalid argument handling."""
    print("\nTesting invalid arguments...")

    # Test missing mode
    try:
        result = subprocess.run(
            [sys.executable, "-m", "spark_job.cli"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print("✅ Missing mode argument test passed (expected failure)")
        else:
            print("❌ Missing mode argument test failed (expected non-zero exit code)")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Missing mode argument test timed out")
        return False

    # Test invalid mode
    try:
        result = subprocess.run(
            [sys.executable, "-m", "spark_job.cli", "--mode", "invalid-mode"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print("✅ Invalid mode test passed (expected failure)")
        else:
            print("❌ Invalid mode test failed (expected non-zero exit code)")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Invalid mode test timed out")
        return False

    return True


def main():
    """Run all tests."""
    print("Starting PySpark Job Tests")
    print("=" * 50)

    tests = [
        test_argument_parsing,
        test_invalid_arguments,
        test_graceful_exit,
        test_fail_mode,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
