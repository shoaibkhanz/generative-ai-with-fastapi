"""
LESSON 3: Async/Await Fundamentals
===================================

Master the async/await syntax and learn how to write asynchronous code.
This lesson covers coroutines, tasks, and common async patterns.

Author: Your AI Programming Instructor
Level: Intermediate
"""

import asyncio
import time
import aiohttp
from typing import List, Any


def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


# =============================================================================
# PART 1: Coroutines - The Building Blocks
# =============================================================================


async def simple_coroutine():
    """
    A coroutine is a function defined with 'async def'.

    Key Points:
    - Defined with 'async def' (not just 'def')
    - Can use 'await' inside
    - Returns a coroutine object when called (not the result!)
    - Must be awaited or scheduled on event loop
    """
    print("  🎯 Inside simple_coroutine")
    await asyncio.sleep(0.1)  # Yield control to event loop
    return "Coroutine result"


async def demo_coroutines():
    """
    Demonstrates what coroutines are and how they work.
    """
    print_section("PART 1: Understanding Coroutines")

    print("\n📌 Creating a coroutine:")
    coro = simple_coroutine()  # This does NOT run the function!
    print(f"   Type: {type(coro)}")
    print(f"   Value: {coro}")

    print("\n💡 To actually run it, we need to 'await' it:")
    result = await coro
    print(f"   Result: {result}")

    print("""
    
    🔑 Key Concepts:
    
    1. async def  → Defines a coroutine function
    2. Calling it → Returns a coroutine object (not the result!)
    3. await coro → Actually executes it and gets the result
    
    Analogy:
    - async def = Recipe (instructions)
    - Calling it = Getting the recipe card
    - await = Actually cooking the recipe
    """)


# =============================================================================
# PART 2: Await - The Magic Keyword
# =============================================================================


async def fetch_data(source: str, delay: float) -> dict:
    """Simulates fetching data asynchronously"""
    print(f"  🌐 Fetching from {source}...")
    await asyncio.sleep(delay)  # Simulates I/O wait
    return {"source": source, "data": f"Data from {source}"}


async def demo_await():
    """
    Demonstrates the 'await' keyword.

    'await' does 3 things:
    1. Suspends the current coroutine
    2. Yields control to event loop
    3. Resumes when awaited operation completes
    """
    print_section("PART 2: The 'await' Keyword")

    print("\n📌 Sequential awaits (one after another):")
    start = time.time()

    result1 = await fetch_data("API-1", 1.0)  # Wait 1 second
    result2 = await fetch_data("API-2", 1.0)  # Wait 1 second
    result3 = await fetch_data("API-3", 1.0)  # Wait 1 second

    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s (sequential)")
    print("💡 Each 'await' blocks until complete (like sync code)")

    print("\n" + "-" * 70)
    print("\n📌 Concurrent execution (all at once):")
    start = time.time()

    # Schedule all tasks at once
    task1 = asyncio.create_task(fetch_data("API-1", 1.0))
    task2 = asyncio.create_task(fetch_data("API-2", 1.0))
    task3 = asyncio.create_task(fetch_data("API-3", 1.0))

    # Wait for all to complete
    results = await asyncio.gather(task1, task2, task3)

    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s (concurrent)")
    print("💡 All tasks ran concurrently → Much faster!")


# =============================================================================
# PART 3: Tasks - Scheduled Coroutines
# =============================================================================


async def long_running_task(name: str, duration: float) -> str:
    """A task that takes some time"""
    print(f"  🚀 {name} started")
    await asyncio.sleep(duration)
    print(f"  ✅ {name} completed")
    return f"Result from {name}"


async def demo_tasks():
    """
    Demonstrates asyncio Tasks.

    Task = Coroutine wrapped for execution on event loop

    Key Differences:
    - Coroutine: Not running yet, needs to be awaited
    - Task: Scheduled on event loop, running in background
    """
    print_section("PART 3: Tasks - Scheduled Coroutines")

    print("\n📌 Creating tasks (schedules them immediately):")

    # create_task() schedules the coroutine on event loop
    task1 = asyncio.create_task(long_running_task("Task-1", 2.0))
    task2 = asyncio.create_task(long_running_task("Task-2", 1.0))

    print(f"   Task-1: {task1}")
    print(f"   Task-2: {task2}")
    print(f"   Task-1 done? {task1.done()}")
    print(f"   Task-2 done? {task2.done()}")

    print("\n💡 Tasks are now running in the background!")
    print("   (Event loop is executing them concurrently)")

    print("\n⏳ Waiting for tasks to complete...")
    result1 = await task1
    result2 = await task2

    print(f"\n✅ Results:")
    print(f"   Task-1: {result1}")
    print(f"   Task-2: {result2}")
    print(f"   Task-1 done? {task1.done()}")
    print(f"   Task-2 done? {task2.done()}")


# =============================================================================
# PART 4: Common Async Patterns
# =============================================================================


async def demo_gather():
    """
    asyncio.gather() - Run multiple coroutines concurrently.

    Characteristics:
    - Waits for ALL tasks to complete
    - Returns results in order
    - If one fails, all fail (by default)
    """
    print_section("PART 4A: asyncio.gather()")

    print("\n📌 gather() waits for all tasks:\n")

    start = time.time()
    results = await asyncio.gather(
        fetch_data("API-1", 0.5),
        fetch_data("API-2", 0.3),
        fetch_data("API-3", 0.8),
    )
    elapsed = time.time() - start

    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Results (in order): {results}")
    print("💡 All completed concurrently, results preserved order")


async def demo_wait():
    """
    asyncio.wait() - Wait for tasks with more control.

    Supports different return conditions:
    - FIRST_COMPLETED: Return when first task completes
    - FIRST_EXCEPTION: Return when first task raises exception
    - ALL_COMPLETED: Return when all tasks complete (default)
    """
    print_section("PART 4B: asyncio.wait()")

    print("\n📌 wait() with FIRST_COMPLETED:\n")

    tasks = {
        asyncio.create_task(fetch_data("Fast-API", 0.3)),
        asyncio.create_task(fetch_data("Medium-API", 0.6)),
        asyncio.create_task(fetch_data("Slow-API", 1.0)),
    }

    start = time.time()
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    elapsed = time.time() - start

    print(f"\n⏱️  Time until first complete: {elapsed:.2f}s")
    print(f"✅ Completed: {len(done)} task(s)")
    print(f"⏳ Pending: {len(pending)} task(s)")

    # Cancel pending tasks
    for task in pending:
        task.cancel()

    print("\n💡 Use wait() when you need the FIRST result quickly")


async def demo_as_completed():
    """
    asyncio.as_completed() - Process results as they complete.

    Perfect for: Processing results as soon as they're available
    """
    print_section("PART 4C: asyncio.as_completed()")

    print("\n📌 as_completed() processes results immediately:\n")

    tasks = [
        fetch_data("API-1", 0.8),
        fetch_data("API-2", 0.3),
        fetch_data("API-3", 0.5),
    ]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  ✅ Got result: {result['source']}")

    print("\n💡 Results processed in completion order (not submission order)")


# =============================================================================
# PART 5: Error Handling in Async
# =============================================================================


async def failing_task(name: str):
    """A task that will fail"""
    print(f"  🚀 {name} started")
    await asyncio.sleep(0.5)
    raise ValueError(f"{name} failed!")


async def demo_error_handling():
    """
    Demonstrates error handling in async code.
    """
    print_section("PART 5: Error Handling")

    print("\n📌 Basic try/except:\n")

    try:
        await failing_task("Task-1")
    except ValueError as e:
        print(f"  ❌ Caught error: {e}")

    print("\n" + "-" * 70)
    print("\n📌 Error handling with gather:\n")

    try:
        # return_exceptions=True prevents gather from raising
        results = await asyncio.gather(
            fetch_data("API-1", 0.3),
            failing_task("Bad-Task"),
            fetch_data("API-2", 0.3),
            return_exceptions=True,  # Important!
        )

        print(f"  📊 Results:")
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"    Task {i}: ❌ Error: {result}")
            else:
                print(f"    Task {i}: ✅ {result}")
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")


# =============================================================================
# PART 6: Timeouts
# =============================================================================


async def slow_operation():
    """A very slow operation"""
    print("  🐌 Starting slow operation...")
    await asyncio.sleep(5.0)
    return "Finally done!"


async def demo_timeouts():
    """
    Demonstrates timeout handling with async.
    """
    print_section("PART 6: Timeouts")

    print("\n📌 Using asyncio.wait_for() with timeout:\n")

    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=2.0,  # Wait max 2 seconds
        )
        print(f"  ✅ Result: {result}")
    except asyncio.TimeoutError:
        print("  ⏱️  Timeout! Operation took too long.")

    print("\n💡 Use wait_for() to prevent operations from hanging forever")


# =============================================================================
# PART 7: Real-World Example
# =============================================================================


async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a URL asynchronously"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return {
                "url": url,
                "status": response.status,
                "length": len(await response.text()),
            }
    except Exception as e:
        return {"url": url, "error": str(e)}


async def demo_real_world():
    """
    Real-world example: Fetching multiple URLs concurrently.
    """
    print_section("PART 7: Real-World Example - HTTP Requests")

    print("\n📌 Fetching 3 websites concurrently:\n")

    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"✅ Fetched {len(results)} URLs in {elapsed:.2f}s")
    for result in results:
        if "error" in result:
            print(f"  ❌ {result['url']}: {result['error']}")
        else:
            print(
                f"  ✅ {result['url']}: {result['status']} ({result['length']} bytes)"
            )

    print(f"\n💡 All requests ran concurrently → ~{elapsed:.1f}s total")
    print(f"    Sequential would take ~{len(urls)}s")


# =============================================================================
# MAIN: Run All Demos
# =============================================================================


async def main():
    """
    Main async function to run all demonstrations.
    """
    print("\n" + "🎓" * 35)
    print("  LESSON 3: ASYNC/AWAIT FUNDAMENTALS")
    print("🎓" * 35)

    # Part 1: Coroutines
    await demo_coroutines()
    input("\n⏸️  Press Enter to continue...")

    # Part 2: Await
    await demo_await()
    input("\n⏸️  Press Enter to continue...")

    # Part 3: Tasks
    await demo_tasks()
    input("\n⏸️  Press Enter to continue...")

    # Part 4A: gather
    await demo_gather()
    input("\n⏸️  Press Enter to continue...")

    # Part 4B: wait
    await demo_wait()
    input("\n⏸️  Press Enter to continue...")

    # Part 4C: as_completed
    await demo_as_completed()
    input("\n⏸️  Press Enter to continue...")

    # Part 5: Error handling
    await demo_error_handling()
    input("\n⏸️  Press Enter to continue...")

    # Part 6: Timeouts
    await demo_timeouts()
    input("\n⏸️  Press Enter to continue...")

    # Part 7: Real-world
    await demo_real_world()

    print("\n" + "=" * 70)
    print("🎉 LESSON 3 COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   1. async def = Define coroutine")
    print("   2. await = Suspend and yield control")
    print("   3. create_task() = Schedule on event loop")
    print("   4. gather() = Run multiple, wait for all")
    print("   5. wait() = More control over completion")
    print("   6. as_completed() = Process as ready")
    print("\n🚀 Next Lesson: Threading vs Async")
    print("   (Understanding when to use each approach)")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
