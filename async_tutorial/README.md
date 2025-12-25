# 🚀 Async/Sync Programming Masterclass

A comprehensive tutorial on synchronous, asynchronous, multithreading, and multiprocessing in Python.

## 📚 Table of Contents

1. **Lesson 1**: Synchronous Programming Basics
2. **Lesson 2**: The Event Loop Explained
3. **Lesson 3**: Async/Await Fundamentals
4. **Lesson 4**: Threading vs Async
5. **Lesson 5**: Multiprocessing
6. **Lesson 6**: Real-World Examples
7. **Lesson 7**: FastAPI Async Deep Dive

## 🎯 Learning Path

### Beginner Track
1. Start with `01_sync_basics.py` - Understand synchronous execution
2. Move to `02_event_loop_explained.py` - Learn how async works under the hood
3. Practice with `03_async_fundamentals.py` - Master async/await syntax

### Intermediate Track
4. Compare with `04_threading_vs_async.py` - Understand when to use what
5. Explore `05_multiprocessing.py` - CPU-bound tasks
6. Study `06_real_world_examples.py` - Practical patterns

### Advanced Track
7. Deep dive into `07_fastapi_async.py` - Production patterns
8. Review `08_pitfalls_and_best_practices.py` - Avoid common mistakes
9. Complete `09_advanced_patterns.py` - Expert techniques

## 🏃 Quick Start

```bash
# Run any lesson
python async_tutorial/01_sync_basics.py

# Run all lessons in order
python async_tutorial/run_all_lessons.py

# Interactive examples
python async_tutorial/interactive_demo.py
```

## 🎓 Key Concepts You'll Learn

- **Event Loop**: The heart of async programming
- **Coroutines**: Async functions that can be paused and resumed
- **Tasks**: Wrapped coroutines running in the event loop
- **Threading**: OS-level concurrency for I/O-bound tasks
- **Multiprocessing**: True parallelism for CPU-bound tasks
- **GIL**: Python's Global Interpreter Lock and its implications
- **Async Patterns**: gather, wait, create_task, etc.

## 📊 Comparison Table

| Approach | Use Case | Concurrency | Parallelism | Memory | Complexity |
|----------|----------|-------------|-------------|--------|------------|
| **Sync** | Simple tasks | ❌ No | ❌ No | ✅ Low | ⭐ Easy |
| **Threading** | I/O-bound | ✅ Yes | ❌ No (GIL) | ⚠️ Medium | ⭐⭐ Medium |
| **Async** | I/O-bound | ✅ Yes | ❌ No | ✅ Low | ⭐⭐⭐ Medium |
| **Multiprocessing** | CPU-bound | ✅ Yes | ✅ Yes | ❌ High | ⭐⭐⭐⭐ Hard |

## 🎯 When to Use What?

### Use Synchronous
- Simple scripts
- CPU-bound single tasks
- When code clarity > performance

### Use Async (asyncio)
- ✅ **I/O-bound tasks** (network, file, database)
- ✅ **Many concurrent operations** (1000+ connections)
- ✅ **FastAPI, web scraping, API calls**
- ✅ **Low memory overhead**

### Use Threading
- ⚠️ I/O-bound tasks (but async is often better)
- Legacy code integration
- When you can't use async
- GUI applications

### Use Multiprocessing
- ✅ **CPU-bound tasks** (computation, data processing)
- ✅ **True parallelism needed**
- ✅ **Bypassing the GIL**

## 🛠️ Requirements

```bash
pip install aiohttp aiofiles httpx fastapi uvicorn
```

## 📝 Notes for Senior Engineers

This tutorial assumes you understand:
- Python basics
- Functions and decorators
- Context managers
- Generators (helpful but not required)

We'll dive deep into:
- Event loop internals
- Coroutine scheduling
- Task lifecycle management
- Performance profiling
- Production best practices
