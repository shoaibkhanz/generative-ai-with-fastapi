"""
LESSON 4: Threading vs Async
=============================

Understanding the differences, tradeoffs, and when to use each approach.
This is crucial for making the right architectural decisions.

Author: Your AI Programming Instructor
Level: Advanced
"""

import asyncio
import threading
import time
import concurrent.futures
from typing import List


def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


# =============================================================================
# PART 1: Threading Basics
# =============================================================================


def blocking_io_task(name: str, duration: float) -> str:
    """
    A synchronous I/O task (simulated with sleep).
    This represents actual blocking I/O like file or network operations.
    """
    print(f"  🧵 Thread {threading.current_thread().name}: {name} starting")
    time.sleep(duration)  # Simulates blocking I/O
    result = f"{name} completed by {threading.current_thread().name}"
    print(f"  ✅ {result}")
    return result


def demo_threading_basics():
    """
    Demonstrates basic threading in Python.

    Key Concepts:
    - Each thread runs in parallel (OS-level)
    - Threads share memory space
    - Subject to Global Interpreter Lock (GIL)
    - Good for I/O-bound tasks (despite GIL)
    """
    print_section("PART 1: Threading Basics")

    print("\n📌 Running 3 tasks with threading:\n")

    start = time.time()

    # Create threads
    threads = []
    for i in range(1, 4):
        thread = threading.Thread(
            target=blocking_io_task, args=(f"Task-{i}", 1.0), name=f"Worker-{i}"
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print("💡 All threads ran in parallel → ~1 second total")


# =============================================================================
# PART 2: The Global Interpreter Lock (GIL)
# =============================================================================


def cpu_intensive_task(n: int) -> int:
    """
    A CPU-intensive task that actually computes something.
    This is affected by the GIL.
    """
    print(f"  🧵 Computing on thread {threading.current_thread().name}")
    result = sum(i * i for i in range(n))
    return result


def demo_gil_impact():
    """
    Demonstrates the GIL's impact on CPU-bound tasks.

    THE GIL (Global Interpreter Lock):
    - Only ONE thread can execute Python bytecode at a time
    - Prevents true parallelism for CPU-bound tasks
    - Released during I/O operations (that's why threading works for I/O!)
    - Does NOT affect async (async is single-threaded anyway)
    """
    print_section("PART 2: The Global Interpreter Lock (GIL)")

    print("""
    🔒 The GIL (Global Interpreter Lock):
    
    What it is:
    - A mutex that protects Python objects
    - Only ONE thread can hold the GIL at a time
    - Even on a 16-core CPU, only 1 thread executes at once
    
    Why it exists:
    - Simplifies memory management
    - Makes C extensions easier to write
    - Prevents race conditions in Python internals
    
    Impact:
    - ❌ CPU-bound: Threading doesn't help (GIL blocks parallelism)
    - ✅ I/O-bound: Threading works great (GIL released during I/O)
    """)

    print("\n📌 CPU-bound task with threading (GIL impact):\n")

    n = 10_000_000

    # Single-threaded (baseline)
    print("  Single-threaded:")
    start = time.time()
    result1 = cpu_intensive_task(n)
    elapsed_single = time.time() - start
    print(f"  ⏱️  Time: {elapsed_single:.2f}s\n")

    # Multi-threaded (GIL prevents speedup)
    print("  Multi-threaded (2 threads):")
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(cpu_intensive_task, n)
        future2 = executor.submit(cpu_intensive_task, n)
        result1 = future1.result()
        result2 = future2.result()
    elapsed_multi = time.time() - start
    print(f"  ⏱️  Time: {elapsed_multi:.2f}s\n")

    print(f"💡 Speedup: {elapsed_single / elapsed_multi:.2f}x")
    print("   Notice: No speedup! GIL prevents true parallelism.")
    print("   For CPU-bound tasks, use multiprocessing instead.")


# =============================================================================
# PART 3: Async vs Threading Comparison
# =============================================================================


async def async_io_task(name: str, duration: float) -> str:
    """Async version of I/O task"""
    print(f"  ⚡ Async: {name} starting")
    await asyncio.sleep(duration)
    result = f"{name} completed (async)"
    print(f"  ✅ {result}")
    return result


async def demo_async_vs_threading():
    """
    Direct comparison of async and threading for I/O tasks.
    """
    print_section("PART 3: Async vs Threading for I/O")

    # Threading approach
    print("\n📌 Threading approach:\n")
    start = time.time()
    threads = []
    for i in range(5):
        thread = threading.Thread(target=blocking_io_task, args=(f"Task-{i}", 0.5))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    threading_time = time.time() - start
    print(f"  ⏱️  Threading time: {threading_time:.2f}s")

    # Async approach
    print("\n📌 Async approach:\n")
    start = time.time()
    await asyncio.gather(*[async_io_task(f"Task-{i}", 0.5) for i in range(5)])
    async_time = time.time() - start
    print(f"  ⏱️  Async time: {async_time:.2f}s")

    print(f"\n📊 Comparison:")
    print(f"   Threading: {threading_time:.2f}s")
    print(f"   Async:     {async_time:.2f}s")
    print(f"   Both complete in ~0.5s (concurrent execution)")


# =============================================================================
# PART 4: Memory and Overhead Comparison
# =============================================================================


def demo_scalability():
    """
    Compares scalability of threading vs async.

    Key Difference:
    - Thread: ~8MB stack per thread (OS overhead)
    - Async: ~1KB per coroutine (Python object)

    Result: Async can handle 100,000+ concurrent operations easily
    """
    print_section("PART 4: Scalability - Threading vs Async")

    print("""
    📊 Resource Comparison:
    
    Threading:
    - Each thread: ~8MB stack (OS allocated)
    - Context switching: OS scheduler (heavier)
    - 1,000 threads ≈ 8GB memory
    - Practical limit: ~1,000-5,000 threads
    
    Async:
    - Each coroutine: ~1-3KB (Python object)
    - Context switching: Event loop (lightweight)
    - 1,000 coroutines ≈ 1-3MB memory
    - Practical limit: 100,000+ coroutines
    
    💡 Async scales MUCH better for high concurrency!
    """)

    print("\n📌 Creating 1,000 concurrent operations:\n")

    # Async version (fast and lightweight)
    async def quick_task(i):
        await asyncio.sleep(0.001)
        return i

    async def test_async_scale():
        start = time.time()
        results = await asyncio.gather(*[quick_task(i) for i in range(1000)])
        elapsed = time.time() - start
        print(f"  ⚡ Async (1,000 coroutines): {elapsed:.2f}s")
        return elapsed

    # Run async test
    async_time = asyncio.run(test_async_scale())

    print(f"\n💡 Async handled 1,000 concurrent operations easily!")
    print(f"   Creating 1,000 threads would be problematic (memory + overhead)")


# =============================================================================
# PART 5: When to Use What - Decision Matrix
# =============================================================================


def demo_decision_matrix():
    """
    Provides a decision matrix for choosing between approaches.
    """
    print_section("PART 5: Decision Matrix - When to Use What")

    print("""
    🎯 DECISION MATRIX
    
    ┌─────────────────────┬──────────────┬─────────────┬────────────────┐
    │  Scenario           │  Async       │  Threading  │  Multiprocess  │
    ├─────────────────────┼──────────────┼─────────────┼────────────────┤
    │ Network requests    │  ⭐⭐⭐⭐⭐    │  ⭐⭐⭐       │  ⭐             │
    │ File I/O            │  ⭐⭐⭐⭐      │  ⭐⭐⭐⭐      │  ⭐⭐            │
    │ Database queries    │  ⭐⭐⭐⭐⭐    │  ⭐⭐⭐       │  ⭐⭐            │
    │ Web scraping        │  ⭐⭐⭐⭐⭐    │  ⭐⭐⭐       │  ⭐⭐            │
    │ API calls (100+)    │  ⭐⭐⭐⭐⭐    │  ⭐⭐         │  ⭐             │
    │ CPU computation     │  ⭐           │  ⭐          │  ⭐⭐⭐⭐⭐       │
    │ Data processing     │  ⭐           │  ⭐          │  ⭐⭐⭐⭐⭐       │
    │ Image processing    │  ⭐           │  ⭐          │  ⭐⭐⭐⭐⭐       │
    │ Legacy code         │  ⭐           │  ⭐⭐⭐⭐     │  ⭐⭐            │
    │ GUI applications    │  ⭐⭐         │  ⭐⭐⭐⭐⭐    │  ⭐⭐            │
    └─────────────────────┴──────────────┴─────────────┴────────────────┘
    
    ═══════════════════════════════════════════════════════════════════
    
    🏆 USE ASYNC WHEN:
    ✅ High concurrency (1000+ operations)
    ✅ I/O-bound tasks (network, database, files)
    ✅ Modern async libraries available (aiohttp, asyncpg)
    ✅ Memory efficiency matters
    ✅ Building APIs (FastAPI, aiohttp)
    
    🧵 USE THREADING WHEN:
    ✅ I/O-bound with blocking libraries (no async version)
    ✅ Legacy code integration
    ✅ GUI applications (keep UI responsive)
    ✅ Moderate concurrency (< 1000 operations)
    ✅ Simpler mental model needed
    
    🚀 USE MULTIPROCESSING WHEN:
    ✅ CPU-bound tasks (computation, data processing)
    ✅ Need true parallelism
    ✅ Multiple CPU cores available
    ✅ Can tolerate inter-process communication overhead
    
    ⚙️ USE SYNCHRONOUS WHEN:
    ✅ Simple scripts
    ✅ Code clarity > performance
    ✅ Single operation at a time
    ✅ No concurrency needed
    """)


# =============================================================================
# PART 6: Hybrid Approaches
# =============================================================================


async def async_with_threading():
    """
    Demonstrates using threading within async code.

    Use Case: Running blocking code from async context
    """
    print_section("PART 6: Hybrid Approach - Async + Threading")

    print("\n📌 Running blocking code from async:\n")

    def blocking_operation(name: str) -> str:
        """A truly blocking operation (no async version)"""
        print(f"  🔨 {name}: Blocking operation starting")
        time.sleep(1)
        return f"{name} completed"

    print("  Using run_in_executor() to run blocking code:\n")

    loop = asyncio.get_event_loop()

    # Run blocking operations in thread pool
    start = time.time()
    results = await asyncio.gather(
        loop.run_in_executor(None, blocking_operation, "Task-1"),
        loop.run_in_executor(None, blocking_operation, "Task-2"),
        loop.run_in_executor(None, blocking_operation, "Task-3"),
    )
    elapsed = time.time() - start

    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print("💡 Used thread pool to run blocking code from async!")
    print("   Best of both worlds: async structure + blocking libraries")


# =============================================================================
# MAIN: Run All Demos
# =============================================================================


async def main():
    """
    Main async function to run all demonstrations.
    """
    print("\n" + "🎓" * 35)
    print("  LESSON 4: THREADING VS ASYNC")
    print("🎓" * 35)

    # Part 1: Threading basics
    demo_threading_basics()
    input("\n⏸️  Press Enter to continue...")

    # Part 2: GIL
    demo_gil_impact()
    input("\n⏸️  Press Enter to continue...")

    # Part 3: Comparison
    await demo_async_vs_threading()
    input("\n⏸️  Press Enter to continue...")

    # Part 4: Scalability
    demo_scalability()
    input("\n⏸️  Press Enter to continue...")

    # Part 5: Decision matrix
    demo_decision_matrix()
    input("\n⏸️  Press Enter to continue...")

    # Part 6: Hybrid
    await async_with_threading()

    print("\n" + "=" * 70)
    print("🎉 LESSON 4 COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   1. Threading: OS-level, ~8MB per thread, GIL limited")
    print("   2. Async: Python-level, ~1KB per coroutine, scales better")
    print("   3. GIL: Prevents true parallelism for CPU tasks")
    print("   4. Async >> Threading for high-concurrency I/O")
    print("   5. Use run_in_executor() for blocking code in async")
    print("\n🚀 Next Lesson: Multiprocessing for CPU-bound tasks")


if __name__ == "__main__":
    asyncio.run(main())
