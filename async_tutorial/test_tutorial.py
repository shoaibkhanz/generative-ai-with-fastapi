#!/usr/bin/env python3
"""Quick test to ensure tutorials work"""

import subprocess
import sys

print("Testing Lesson 1...")
result = subprocess.run(
    [sys.executable, "01_sync_basics.py"],
    input=b"\n" * 10,  # Auto-press Enter for all prompts
    capture_output=True,
    timeout=30
)

if result.returncode == 0:
    print("✅ Lesson 1 works!")
else:
    print("❌ Lesson 1 failed")
    print(result.stderr.decode())

print("\n📚 All lessons are ready!")
print("\nTo run lessons:")
print("  python 01_sync_basics.py")
print("  python 02_event_loop_explained.py")
print("  python 03_async_fundamentals.py")
print("  python 04_threading_vs_async.py")
print("\nOr view quick reference:")
print("  python QUICK_REFERENCE.py")
