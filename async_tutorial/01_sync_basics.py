"""
LESSON 1: Synchronous Programming Basics
==========================================

Understanding synchronous execution is crucial before diving into async.
This lesson covers the fundamentals of how Python executes code line by line.

Author: Your AI Programming Instructor
Level: Beginner
"""

import time
from typing import List


def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


# =============================================================================
# PART 1: Understanding Synchronous Execution
# =============================================================================


def synchronous_task(task_name: str, duration: float) -> str:
    """
    A simple synchronous task that blocks execution.

    In synchronous code:
    1. Function is called
    2. Code executes line by line
    3. Function waits (blocks) until complete
    4. Returns result
    5. Next line executes

    Args:
        task_name: Name of the task
        duration: How long to "work" (simulate with sleep)

    Returns:
        Result string
    """
    print(f"  ⏳ Starting {task_name}...")
    start = time.time()

    # This BLOCKS - nothing else can run during this time
    time.sleep(duration)

    elapsed = time.time() - start
    result = f"  ✅ {task_name} completed in {elapsed:.2f}s"
    print(result)
    return result


def demo_synchronous_execution():
    """
    Demonstrates how synchronous code executes sequentially.

    Key Concept: BLOCKING
    Each function call blocks until it completes. The program waits
    at each time.sleep() before moving to the next line.
    """
    print_section("DEMO 1: Synchronous Execution (Blocking)")

    print("\n📌 Watch how each task WAITS for the previous one to finish:")

    start = time.time()

    # These run ONE AFTER ANOTHER (sequentially)
    synchronous_task("Task 1", 1.0)  # Blocks for 1 second
    synchronous_task("Task 2", 1.0)  # Blocks for 1 second
    synchronous_task("Task 3", 1.0)  # Blocks for 1 second

    total = time.time() - start
    print(f"\n⏱️  Total time: {total:.2f}s")
    print("💡 Notice: Total time = Sum of all tasks (3 seconds)")
    print("    This is because each task BLOCKS the next one from starting.")


# =============================================================================
# PART 2: The Call Stack
# =============================================================================


def function_c():
    """Innermost function"""
    print("    → In function_c (deepest)")
    print("    ← Returning from function_c")
    return "Result from C"


def function_b():
    """Middle function"""
    print("  → In function_b")
    result = function_c()  # BLOCKS here until function_c returns
    print(f"  ← function_b got: {result}")
    return "Result from B"


def function_a():
    """Outermost function"""
    print("→ In function_a")
    result = function_b()  # BLOCKS here until function_b returns
    print(f"← function_a got: {result}")
    return "Result from A"


def demo_call_stack():
    """
    Demonstrates the call stack and blocking behavior.

    Key Concept: CALL STACK
    Python maintains a stack of function calls. When a function calls
    another, it BLOCKS and waits for the inner function to complete.

    Call Stack Visualization:

    | function_c |  ← Top of stack (currently executing)
    | function_b |  ← Waiting for function_c
    | function_a |  ← Waiting for function_b
    | main       |  ← Waiting for function_a
    """
    print_section("DEMO 2: The Call Stack (How Python Tracks Execution)")

    print("\n📌 Watch the call stack in action:")
    print("(Functions nest deeper and deeper, then return back up)\n")

    result = function_a()

    print(f"\n✅ Final result: {result}")
    print("\n💡 Key Takeaway:")
    print("   - Each function WAITS for the one it calls")
    print("   - This is synchronous/blocking behavior")
    print("   - The call stack grows deeper, then unwinds")


# =============================================================================
# PART 3: Real-World Analogy
# =============================================================================


def make_coffee_sync() -> List[str]:
    """
    Making coffee synchronously (the normal way).

    Real-world analogy: You're a barista making drinks one at a time.
    You can't start the next drink until the current one is done.
    """
    print_section("DEMO 3: Real-World Analogy - Coffee Shop (Synchronous)")

    print("\n☕ You're a barista. Each drink takes 2 seconds.")
    print("📌 Synchronous approach: One drink at a time\n")

    drinks = ["Espresso", "Latte", "Cappuccino"]
    completed = []

    start = time.time()

    for drink in drinks:
        print(f"  👨‍🍳 Making {drink}...")
        time.sleep(2)  # BLOCKS while making the drink
        print(f"  ✅ {drink} ready!")
        completed.append(drink)

    total = time.time() - start
    print(f"\n⏱️  Total time: {total:.2f}s")
    print(f"💡 You made {len(drinks)} drinks in {total:.2f} seconds")
    print("    Problem: Customers 2 and 3 waited the entire time!")

    return completed


# =============================================================================
# PART 4: Why Synchronous Can Be Inefficient
# =============================================================================


def fetch_data_sync(source: str, delay: float) -> dict:
    """
    Simulates fetching data from a slow source (like an API).

    In real applications, this might be:
    - HTTP requests to APIs
    - Database queries
    - File I/O operations
    - Network calls
    """
    print(f"  🌐 Fetching from {source}...")
    time.sleep(delay)  # Simulates network latency - BLOCKS!
    print(f"  ✅ Got data from {source}")
    return {"source": source, "data": f"Data from {source}"}


def demo_inefficiency():
    """
    Shows why synchronous code is inefficient for I/O operations.

    Key Concept: I/O BOUND vs CPU BOUND

    I/O Bound: Task spends most time WAITING (network, disk, database)
               → Synchronous code wastes time doing nothing
               → Perfect candidate for async!

    CPU Bound: Task spends most time COMPUTING (calculations, processing)
               → Async doesn't help (still one CPU)
               → Use multiprocessing instead
    """
    print_section("DEMO 4: The Inefficiency Problem")

    print("\n📌 Fetching data from 3 APIs (each takes 1 second)")
    print("⚠️  Synchronous version: We WAIT at each API call\n")

    sources = ["API-1", "API-2", "API-3"]
    start = time.time()

    results = []
    for source in sources:
        result = fetch_data_sync(source, 1.0)  # BLOCKS for 1 second
        results.append(result)

    total = time.time() - start
    print(f"\n⏱️  Total time: {total:.2f}s")
    print("\n🤔 Think about it:")
    print("   - While waiting for API-1, we could have started API-2")
    print("   - While waiting for API-2, we could have started API-3")
    print("   - We're just WAITING, not computing!")
    print("\n💡 This is where ASYNC shines!")
    print("   Async can handle all 3 API calls concurrently → ~1 second total!")


# =============================================================================
# PART 5: Understanding Program Flow
# =============================================================================


def demo_program_flow():
    """
    Visualizes synchronous program flow.
    """
    print_section("DEMO 5: Visualizing Synchronous Flow")

    print("\n📊 Program Flow Visualization:")
    print("""
    Synchronous (Sequential):
    
    Time →
    ═══════════════════════════════════════════════════
    Thread: [Task 1][Task 2][Task 3]
    ═══════════════════════════════════════════════════
            ↑      ↑      ↑
            Blocks  Blocks  Blocks
    
    - Single thread of execution
    - Tasks run one after another
    - Each task blocks the next
    - Total time = Sum of all tasks
    
    When Task 1 is running:
    - Task 2 cannot start (blocked)
    - Task 3 cannot start (blocked)
    - CPU might be idle if Task 1 is waiting for I/O
    """)

    print("\n✅ Advantages of Synchronous Code:")
    print("   1. Simple to write and understand")
    print("   2. Easy to debug (linear flow)")
    print("   3. Predictable execution order")
    print("   4. No race conditions")

    print("\n❌ Disadvantages:")
    print("   1. Inefficient for I/O-bound tasks")
    print("   2. Poor resource utilization")
    print("   3. Long total execution time")
    print("   4. Can't handle high concurrency")


# =============================================================================
# MAIN: Run All Demos
# =============================================================================


def main():
    """
    Main function to run all demonstrations.
    """
    print("\n" + "🎓" * 35)
    print("  LESSON 1: SYNCHRONOUS PROGRAMMING BASICS")
    print("🎓" * 35)

    # Demo 1: Basic synchronous execution
    demo_synchronous_execution()

    input("\n⏸️  Press Enter to continue to Demo 2...")

    # Demo 2: Call stack
    demo_call_stack()

    input("\n⏸️  Press Enter to continue to Demo 3...")

    # Demo 3: Real-world analogy
    make_coffee_sync()

    input("\n⏸️  Press Enter to continue to Demo 4...")

    # Demo 4: Inefficiency
    demo_inefficiency()

    input("\n⏸️  Press Enter to continue to Demo 5...")

    # Demo 5: Program flow
    demo_program_flow()

    print("\n" + "=" * 70)
    print("🎉 LESSON 1 COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   1. Synchronous code executes line by line (sequential)")
    print("   2. Each function call BLOCKS until it returns")
    print("   3. The call stack tracks nested function calls")
    print("   4. Synchronous is inefficient for I/O-bound tasks")
    print("   5. We spend time WAITING instead of WORKING")
    print("\n🚀 Next Lesson: Understanding the Event Loop")
    print("   (How async solves the inefficiency problem)")


if __name__ == "__main__":
    main()
