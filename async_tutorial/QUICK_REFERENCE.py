"""
QUICK REFERENCE: Async/Threading/Multiprocessing
=================================================

Quick lookup guide for senior engineers.
"""

CHEAT_SHEET = """
╔══════════════════════════════════════════════════════════════════════════╗
║                        ASYNC/AWAIT QUICK REFERENCE                        ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─ BASIC SYNTAX ─────────────────────────────────────────────────────────┐
│                                                                          │
│  # Define coroutine                                                      │
│  async def my_func():                                                    │
│      result = await other_async_func()                                  │
│      return result                                                       │
│                                                                          │
│  # Run coroutine                                                         │
│  asyncio.run(my_func())  # Python 3.7+                                  │
│                                                                          │
│  # Create task (schedule on event loop)                                 │
│  task = asyncio.create_task(my_func())                                  │
│  result = await task                                                     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ COMMON PATTERNS ──────────────────────────────────────────────────────┐
│                                                                          │
│  # Run multiple coroutines concurrently                                 │
│  results = await asyncio.gather(coro1(), coro2(), coro3())              │
│                                                                          │
│  # Wait for first completion                                            │
│  done, pending = await asyncio.wait(                                    │
│      tasks, return_when=asyncio.FIRST_COMPLETED                         │
│  )                                                                       │
│                                                                          │
│  # Process results as they complete                                     │
│  for coro in asyncio.as_completed([coro1(), coro2()]):                  │
│      result = await coro                                                 │
│                                                                          │
│  # Timeout                                                               │
│  result = await asyncio.wait_for(slow_func(), timeout=5.0)              │
│                                                                          │
│  # Run blocking code from async                                         │
│  loop = asyncio.get_event_loop()                                        │
│  result = await loop.run_in_executor(None, blocking_func)               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ ERROR HANDLING ───────────────────────────────────────────────────────┐
│                                                                          │
│  try:                                                                    │
│      result = await risky_operation()                                   │
│  except SpecificError as e:                                             │
│      handle_error(e)                                                     │
│                                                                          │
│  # With gather (continue on error)                                      │
│  results = await asyncio.gather(                                        │
│      coro1(), coro2(),                                                   │
│      return_exceptions=True                                              │
│  )                                                                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ THREADING ────────────────────────────────────────────────────────────┐
│                                                                          │
│  import threading                                                        │
│                                                                          │
│  # Basic thread                                                          │
│  thread = threading.Thread(target=func, args=(arg1, arg2))              │
│  thread.start()                                                          │
│  thread.join()  # Wait for completion                                   │
│                                                                          │
│  # Thread pool                                                           │
│  from concurrent.futures import ThreadPoolExecutor                      │
│  with ThreadPoolExecutor(max_workers=4) as executor:                    │
│      futures = [executor.submit(func, arg) for arg in args]             │
│      results = [f.result() for f in futures]                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ MULTIPROCESSING ──────────────────────────────────────────────────────┐
│                                                                          │
│  from multiprocessing import Pool                                       │
│                                                                          │
│  # Process pool                                                          │
│  with Pool(processes=4) as pool:                                        │
│      results = pool.map(cpu_func, data_list)                            │
│                                                                          │
│  # Or with ProcessPoolExecutor                                          │
│  from concurrent.futures import ProcessPoolExecutor                     │
│  with ProcessPoolExecutor(max_workers=4) as executor:                   │
│      results = list(executor.map(cpu_func, data_list))                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════╗
║                          DECISION FLOWCHART                               ║
╚══════════════════════════════════════════════════════════════════════════╝

                    START: Need concurrency?
                              │
                              ↓
                    ┌─────────────────────┐
                    │  What type of task? │
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         CPU-BOUND      I/O-BOUND       SIMPLE
     (computation)  (network/disk)    (no concurrency)
              │               │               │
              ↓               ↓               ↓
    ┌─────────────────┐ ┌─────────────┐  Use SYNC
    │ Multiprocessing │ │ High conc?  │   (regular)
    │  (bypass GIL)   │ └──────┬──────┘
    └─────────────────┘        │
                         ┌─────┴─────┐
                         ↓           ↓
                      YES (1000+)  NO (<1000)
                         │           │
                         ↓           ↓
                    Use ASYNC   Use THREADING
                   (asyncio)    or ASYNC

╔══════════════════════════════════════════════════════════════════════════╗
║                         COMMON GOTCHAS                                    ║
╚══════════════════════════════════════════════════════════════════════════╝

❌ WRONG: Forgetting await
   result = async_func()  # Returns coroutine, doesn't run it!

✅ RIGHT:
   result = await async_func()

────────────────────────────────────────────────────────────────────────────

❌ WRONG: Blocking in async
   async def bad():
       time.sleep(1)  # BLOCKS event loop!

✅ RIGHT:
   async def good():
       await asyncio.sleep(1)  # Yields control

────────────────────────────────────────────────────────────────────────────

❌ WRONG: Creating tasks without await
   task1 = asyncio.create_task(func1())
   task2 = asyncio.create_task(func2())
   # Tasks created but never awaited = may not complete!

✅ RIGHT:
   task1 = asyncio.create_task(func1())
   task2 = asyncio.create_task(func2())
   await asyncio.gather(task1, task2)

────────────────────────────────────────────────────────────────────────────

❌ WRONG: Mixing sync and async incorrectly
   async def bad():
       result = sync_func()  # If slow, blocks event loop

✅ RIGHT:
   async def good():
       loop = asyncio.get_event_loop()
       result = await loop.run_in_executor(None, sync_func)

════════════════════════════════════════════════════════════════════════════

PERFORMANCE RULES OF THUMB:

1. Async is ~10-100x more memory efficient than threading
2. Async can handle 100,000+ concurrent operations
3. Threading limited to ~1,000-5,000 threads
4. Multiprocessing: 1 process per CPU core is optimal
5. Context switching: Async < Threading < Multiprocessing

════════════════════════════════════════════════════════════════════════════
"""


def print_cheat_sheet():
    """Print the cheat sheet"""
    print(CHEAT_SHEET)


if __name__ == "__main__":
    print_cheat_sheet()
