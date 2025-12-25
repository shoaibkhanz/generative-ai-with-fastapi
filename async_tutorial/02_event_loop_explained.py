"""
LESSON 2: The Event Loop Explained
===================================

The event loop is the HEART of async programming. Understanding it deeply
will make async/await intuitive instead of magical.

Author: Your AI Programming Instructor
Level: Intermediate
"""

import asyncio
import time
from typing import List


def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


# =============================================================================
# PART 1: What IS an Event Loop?
# =============================================================================


def explain_event_loop_concept():
    """
    Conceptual explanation of the event loop.

    THE EVENT LOOP IS:
    - A while loop that runs forever
    - Manages and schedules coroutines (async functions)
    - Switches between tasks when they're waiting (I/O)
    - Single-threaded but handles concurrency through cooperation
    """
    print_section("PART 1: What IS an Event Loop?")

    print("""
    🔄 The Event Loop (Simplified Pseudocode):
    
    class EventLoop:
        def __init__(self):
            self.tasks = []  # Queue of tasks to run
            self.running = True
        
        def run_forever(self):
            while self.running:
                # 1. Get next task from queue
                task = self.get_next_task()
                
                # 2. Run the task until it yields control
                task.run_until_blocked()
                
                # 3. If task is waiting (I/O), move to next task
                if task.is_waiting():
                    self.tasks.append(task)  # Re-queue for later
                
                # 4. If task is done, remove it
                elif task.is_complete():
                    self.remove_task(task)
    
    """)

    print("💡 Key Concepts:")
    print("   1. EVENT LOOP = Scheduler + Task Manager")
    print("   2. Tasks COOPERATE by yielding control when waiting")
    print("   3. Single thread, but many tasks make progress concurrently")
    print("   4. Works because I/O operations don't need CPU")

    print("\n🔑 The Secret Sauce: COOPERATIVE MULTITASKING")
    print("   - Task says: 'I'm waiting for network, you can run others'")
    print("   - Event loop switches to another task")
    print("   - Original task resumes when I/O is ready")
    print("   - All in ONE thread!")


# =============================================================================
# PART 2: Simulating an Event Loop (Educational)
# =============================================================================


class SimpleTask:
    """A simple task that can yield control"""

    def __init__(self, name: str, steps: List[str]):
        self.name = name
        self.steps = steps
        self.current_step = 0
        self.complete = False

    def run_step(self) -> bool:
        """Run one step. Returns True if more work to do."""
        if self.current_step >= len(self.steps):
            self.complete = True
            return False

        step = self.steps[self.current_step]
        print(f"  🏃 {self.name}: {step}")
        self.current_step += 1
        return not self.complete


class SimpleEventLoop:
    """
    Educational event loop implementation.

    This shows HOW an event loop works under the hood.
    Real asyncio is more complex, but the concept is the same.
    """

    def __init__(self):
        self.tasks: List[SimpleTask] = []

    def add_task(self, task: SimpleTask):
        """Add a task to the event loop"""
        self.tasks.append(task)
        print(f"  ➕ Added task: {task.name}")

    def run(self):
        """Run the event loop until all tasks complete"""
        print(f"\n  🔄 Event Loop Starting with {len(self.tasks)} tasks...\n")

        iteration = 0
        while self.tasks:
            iteration += 1
            print(f"  --- Iteration {iteration} ---")

            # Process each task
            for task in self.tasks[:]:  # Copy list to avoid modification issues
                has_more_work = task.run_step()

                if not has_more_work:
                    print(f"  ✅ {task.name} completed!")
                    self.tasks.remove(task)

            print()  # Blank line between iterations

        print("  🎉 All tasks complete! Event loop exiting.")


def demo_simple_event_loop():
    """
    Demonstrates a simple event loop with cooperative multitasking.
    """
    print_section("PART 2: Simple Event Loop Demo")

    print("\n📌 Creating 3 tasks that will cooperate:")

    # Create tasks
    task1 = SimpleTask(
        "Cook Pasta",
        [
            "Boil water",
            "Add pasta (then wait)",  # Yields control here
            "Drain pasta",
            "Serve",
        ],
    )

    task2 = SimpleTask(
        "Make Sauce",
        [
            "Heat pan",
            "Add ingredients (then simmer)",  # Yields control here
            "Stir",
            "Done",
        ],
    )

    task3 = SimpleTask("Set Table", ["Get plates", "Arrange utensils", "Done"])

    # Create and run event loop
    loop = SimpleEventLoop()
    loop.add_task(task1)
    loop.add_task(task2)
    loop.add_task(task3)

    print("\n💡 Watch how tasks take turns (round-robin):")
    loop.run()

    print("\n🎓 What Just Happened:")
    print("   1. Event loop ran in ONE thread")
    print("   2. Each task did one step, then yielded control")
    print("   3. All tasks made progress concurrently")
    print("   4. This is COOPERATIVE MULTITASKING")


# =============================================================================
# PART 3: Real Asyncio Event Loop
# =============================================================================


async def async_task(name: str, duration: float) -> str:
    """
    An actual async task using asyncio.

    Key: await asyncio.sleep() YIELDS CONTROL back to event loop.
    Other tasks can run during this time!
    """
    print(f"  ⏳ {name} starting...")

    # This is the magic: await YIELDS control
    # Event loop can run other tasks while we "sleep"
    await asyncio.sleep(duration)

    print(f"  ✅ {name} completed!")
    return f"Result from {name}"


async def demo_real_event_loop():
    """
    Demonstrates the real asyncio event loop.

    Key Concept: await = "Yield control to event loop"
    """
    print_section("PART 3: Real Asyncio Event Loop")

    print("\n📌 Running 3 tasks concurrently with asyncio:")
    print("   (Compare this to Lesson 1's synchronous version!)\n")

    start = time.time()

    # Create tasks (these are scheduled on the event loop)
    task1 = asyncio.create_task(async_task("Task 1", 1.0))
    task2 = asyncio.create_task(async_task("Task 2", 1.0))
    task3 = asyncio.create_task(async_task("Task 3", 1.0))

    # Wait for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)

    total = time.time() - start
    print(f"\n⏱️  Total time: {total:.2f}s")
    print(f"💡 Notice: ~1 second total (not 3!)")
    print(f"    All tasks ran CONCURRENTLY on ONE thread!")
    print(f"\n📊 Results: {results}")


# =============================================================================
# PART 4: Event Loop Lifecycle
# =============================================================================


async def demo_event_loop_lifecycle():
    """
    Demonstrates the lifecycle of tasks in the event loop.
    """
    print_section("PART 4: Event Loop Lifecycle")

    print("""
    📊 Task Lifecycle in Event Loop:
    
    1. CREATED
       ↓
       task = asyncio.create_task(my_coroutine())
       ↓
    2. SCHEDULED (added to event loop)
       ↓
    3. RUNNING (event loop executes task)
       ↓
    4. WAITING (task hits 'await', yields control)
       ↓                         ↓
       Other tasks run     I/O completes
       ↓                         ↓
       ← ← ← ← ← ← ← ← ← ← ← ← ←
       ↓
    5. RUNNING (resumes where it left off)
       ↓
    6. COMPLETE (task returns result)
    
    """)

    print("🔍 Let's trace a task through this lifecycle:\n")

    async def traced_task(name: str):
        print(f"  1️⃣  {name}: CREATED & RUNNING")

        print(f"  2️⃣  {name}: About to await (will YIELD control)")
        await asyncio.sleep(0.5)
        print(f"  3️⃣  {name}: RESUMED after await")

        print(f"  4️⃣  {name}: About to await again")
        await asyncio.sleep(0.5)
        print(f"  5️⃣  {name}: RESUMED again")

        print(f"  6️⃣  {name}: COMPLETE")
        return f"{name} done"

    # Run two tasks to see interleaving
    await asyncio.gather(traced_task("Task-A"), traced_task("Task-B"))

    print("\n💡 Observations:")
    print("   - Tasks interleave at 'await' points")
    print("   - Event loop switches between them")
    print("   - Each task picks up where it left off")


# =============================================================================
# PART 5: Event Loop Internals
# =============================================================================


def demo_event_loop_internals():
    """
    Shows how to access and inspect the event loop.
    """
    print_section("PART 5: Event Loop Internals")

    print("\n🔍 Accessing the Event Loop:\n")

    # Get the current event loop
    loop = asyncio.get_event_loop()
    print(f"  Event Loop: {loop}")
    print(f"  Is Running: {loop.is_running()}")
    print(f"  Is Closed: {loop.is_closed()}")

    print("\n📊 Event Loop Properties:")
    print(f"   - Time: {loop.time():.2f}")
    print(f"   - Debug Mode: {loop.get_debug()}")

    print("""
    
    🛠️  Common Event Loop Methods:
    
    - loop.run_until_complete(coro)  → Run one coroutine
    - loop.run_forever()             → Run until stop() called
    - loop.create_task(coro)         → Schedule a coroutine
    - loop.call_soon(callback)       → Schedule a callback
    - loop.call_later(delay, callback) → Schedule delayed callback
    - loop.stop()                    → Stop the loop
    - loop.close()                   → Close the loop
    
    """)

    print("💡 In modern Python (3.7+), you rarely interact with loop directly.")
    print("   Use asyncio.run() and it manages the loop for you!")


# =============================================================================
# PART 6: Visualizing Concurrent Execution
# =============================================================================


async def visualize_concurrency():
    """
    Visually demonstrates concurrent execution.
    """
    print_section("PART 6: Visualizing Concurrent Execution")

    print("\n📊 Let's visualize how tasks overlap in time:\n")

    async def timed_task(name: str, delay: float):
        start = time.time()
        print(f"  {time.time() - start:.2f}s | {name} START")
        await asyncio.sleep(delay)
        print(f"  {time.time() - start:.2f}s | {name} END")

    start = time.time()
    await asyncio.gather(
        timed_task("Task-1", 1.0),
        timed_task("Task-2", 0.5),
        timed_task("Task-3", 0.8),
    )

    print(f"\n⏱️  Total: {time.time() - start:.2f}s")
    print("""
    📊 Timeline Visualization:
    
    0.0s: Task-1 START, Task-2 START, Task-3 START
    0.5s: Task-2 END
    0.8s: Task-3 END
    1.0s: Task-1 END
    
    All tasks overlap! This is concurrency on a single thread.
    """)


# =============================================================================
# MAIN: Run All Demos
# =============================================================================


async def main():
    """
    Main async function to run all demonstrations.
    """
    print("\n" + "🎓" * 35)
    print("  LESSON 2: THE EVENT LOOP EXPLAINED")
    print("🎓" * 35)

    # Part 1: Concept
    explain_event_loop_concept()
    input("\n⏸️  Press Enter to continue...")

    # Part 2: Simple event loop
    demo_simple_event_loop()
    input("\n⏸️  Press Enter to continue...")

    # Part 3: Real asyncio
    await demo_real_event_loop()
    input("\n⏸️  Press Enter to continue...")

    # Part 4: Lifecycle
    await demo_event_loop_lifecycle()
    input("\n⏸️  Press Enter to continue...")

    # Part 5: Internals
    demo_event_loop_internals()
    input("\n⏸️  Press Enter to continue...")

    # Part 6: Visualization
    await visualize_concurrency()

    print("\n" + "=" * 70)
    print("🎉 LESSON 2 COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   1. Event loop = Task scheduler + Manager")
    print("   2. 'await' yields control back to event loop")
    print("   3. Tasks cooperate by yielding when waiting")
    print("   4. Concurrency on single thread through cooperation")
    print("   5. Perfect for I/O-bound operations")
    print("\n🚀 Next Lesson: Async/Await Fundamentals")
    print("   (Writing async code and mastering the syntax)")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
