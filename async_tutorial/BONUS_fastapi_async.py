"""
BONUS: FastAPI Async Deep Dive
================================

How async concepts apply to your FastAPI + AWS Bedrock application.

Author: Your AI Programming Instructor
Level: Advanced (Apply knowledge to real project)
"""

import asyncio
import time
from typing import List, Dict
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


# =============================================================================
# PART 1: Why FastAPI Uses Async
# =============================================================================


def explain_fastapi_async():
    """
    Explains why FastAPI is built on async.
    """
    print_section("PART 1: Why FastAPI Uses Async")

    print("""
    🚀 FastAPI's Async Architecture
    
    FastAPI is built on:
    1. Starlette (ASGI framework)
    2. Uvicorn (ASGI server with asyncio)
    3. Pydantic (data validation)
    
    Why Async?
    ✓ Handle 1000+ concurrent requests on single process
    ✓ Perfect for I/O-bound operations (APIs, databases)
    ✓ Non-blocking during AWS Bedrock API calls
    ✓ Low memory footprint
    ✓ Excellent performance
    
    Your Current Stack:
    ┌─────────────────────────────────────────┐
    │  Client Request                          │
    ├─────────────────────────────────────────┤
    │  FastAPI (async route handler)          │
    ├─────────────────────────────────────────┤
    │  boto3 bedrock.converse()               │
    │  (Currently BLOCKING! ⚠️)                │
    ├─────────────────────────────────────────┤
    │  AWS Bedrock API                        │
    │  (Network I/O - could be async)         │
    └─────────────────────────────────────────┘
    
    Problem: boto3 is synchronous!
    Your async route handler blocks on boto3 calls.
    
    Solution: Use run_in_executor() or aioboto3
    """)


# =============================================================================
# PART 2: Your Current FastAPI App (Blocking Issue)
# =============================================================================


# Simulated bedrock client (your actual code uses boto3)
class MockBedrockClient:
    """Mock bedrock client that simulates blocking behavior"""

    def converse(self, modelId: str, messages: List, **kwargs) -> Dict:
        """This BLOCKS the event loop!"""
        print(f"  🔨 BLOCKING call to {modelId}")
        time.sleep(1.0)  # Simulates network latency
        return {
            "output": {"message": {"content": [{"text": "Response"}]}},
            "usage": {"inputTokens": 10, "outputTokens": 20},
        }


app = FastAPI()
bedrock_client = MockBedrockClient()


# CURRENT VERSION: Blocks event loop!
@app.post("/chat-blocking")
async def chat_blocking(prompt: str):
    """
    ⚠️ PROBLEM: This blocks the event loop!

    Even though this is an async function, boto3.converse()
    is synchronous and will block for ~1 second.

    Impact:
    - Other requests must wait
    - Can't handle concurrent requests efficiently
    - Defeats the purpose of async FastAPI
    """
    response = bedrock_client.converse(  # ← BLOCKS HERE!
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 1000, "temperature": 0.7},
    )
    return {"response": response["output"]["message"]["content"][0]["text"]}


async def demo_blocking_issue():
    """
    Demonstrates the blocking issue.
    """
    print_section("PART 2: The Blocking Issue")

    print("\n📌 Testing blocking endpoint with 3 concurrent requests:\n")

    # Simulate 3 concurrent requests
    import httpx

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        start = time.time()

        # These should be concurrent, but will block sequentially
        tasks = [
            client.post("/chat-blocking", json={"prompt": f"Request {i}"})
            for i in range(3)
        ]

        responses = await asyncio.gather(*tasks)
        elapsed = time.time() - start

        print(f"\n⏱️  Total time: {elapsed:.2f}s")
        print("⚠️  Expected: ~1s (concurrent)")
        print("❌  Got: ~3s (sequential blocking)")


# =============================================================================
# PART 3: Solution 1 - run_in_executor()
# =============================================================================


@app.post("/chat-executor")
async def chat_with_executor(prompt: str):
    """
    ✅ SOLUTION 1: Use run_in_executor()

    This runs the blocking boto3 call in a thread pool,
    freeing up the event loop to handle other requests.
    """
    loop = asyncio.get_event_loop()

    # Run blocking operation in thread pool
    response = await loop.run_in_executor(
        None,  # Use default ThreadPoolExecutor
        lambda: bedrock_client.converse(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 1000, "temperature": 0.7},
        ),
    )

    return {"response": response["output"]["message"]["content"][0]["text"]}


def explain_executor_solution():
    """
    Explains the run_in_executor solution.
    """
    print_section("PART 3: Solution 1 - run_in_executor()")

    print("""
    ✅ Using run_in_executor()
    
    What it does:
    1. Takes blocking function
    2. Runs it in a thread from ThreadPoolExecutor
    3. Returns awaitable Future
    4. Event loop free to handle other requests
    
    Code:
    ```python
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,  # Default thread pool
        blocking_function,
        arg1, arg2
    )
    ```
    
    Pros:
    ✓ Works with any blocking library (boto3, requests, etc.)
    ✓ Easy to implement
    ✓ No need to change library
    
    Cons:
    ⚠️ Still uses threads (memory overhead)
    ⚠️ Limited by thread pool size
    ⚠️ Not true async (but good enough!)
    
    Performance:
    - 3 requests: ~1s (concurrent) ✅
    - 100 requests: Still good
    - 1000+ requests: Thread pool becomes bottleneck
    """)


# =============================================================================
# PART 4: Solution 2 - aioboto3 (True Async)
# =============================================================================

"""
# Uncomment if aioboto3 is installed
import aioboto3

@app.post("/chat-async")
async def chat_fully_async(prompt: str):
    '''
    ✅ SOLUTION 2: Use aioboto3 (True async boto3)
    
    This is truly async - no threads needed!
    '''
    session = aioboto3.Session()
    async with session.client("bedrock-runtime", region_name="us-west-2") as bedrock:
        response = await bedrock.converse(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 1000, "temperature": 0.7}
        )
        return {"response": response["output"]["message"]["content"][0]["text"]}
"""


def explain_aioboto3_solution():
    """
    Explains the aioboto3 solution.
    """
    print_section("PART 4: Solution 2 - aioboto3 (True Async)")

    print("""
    ✅ Using aioboto3 (Async boto3)
    
    What it is:
    - Async wrapper around boto3
    - Uses aiohttp for HTTP calls
    - Truly non-blocking
    
    Installation:
    ```bash
    pip install aioboto3
    ```
    
    Code:
    ```python
    import aioboto3
    
    session = aioboto3.Session()
    async with session.client("bedrock-runtime") as bedrock:
        response = await bedrock.converse(...)
    ```
    
    Pros:
    ✓ True async (no threads)
    ✓ Maximum concurrency
    ✓ Best performance
    ✓ Low memory footprint
    
    Cons:
    ⚠️ Additional dependency
    ⚠️ Slightly different API
    
    Performance:
    - 3 requests: ~1s ✅
    - 100 requests: ~1s ✅  
    - 1000+ requests: ~2-3s ✅ (Amazing!)
    """)


# =============================================================================
# PART 5: Comparison & Recommendations
# =============================================================================


def comparison_table():
    """
    Compares the different approaches.
    """
    print_section("PART 5: Comparison & Recommendations")

    print("""
    📊 COMPARISON TABLE
    
    ┌────────────────┬──────────────┬─────────────────┬──────────────┐
    │  Approach      │  Complexity  │  Performance    │  Scalability │
    ├────────────────┼──────────────┼─────────────────┼──────────────┤
    │  Blocking      │  ⭐ Simple   │  ❌ Poor (3s)   │  ❌ Low      │
    │  (Current)     │              │                 │              │
    ├────────────────┼──────────────┼─────────────────┼──────────────┤
    │  Executor      │  ⭐⭐ Easy   │  ✅ Good (1s)   │  ⭐⭐⭐ Med  │
    │  (Threading)   │              │                 │              │
    ├────────────────┼──────────────┼─────────────────┼──────────────┤
    │  aioboto3      │  ⭐⭐⭐ Med  │  ⭐⭐⭐⭐⭐ Best │  ⭐⭐⭐⭐⭐   │
    │  (True async)  │              │                 │              │
    └────────────────┴──────────────┴─────────────────┴──────────────┘
    
    🎯 RECOMMENDATIONS
    
    For Your FastAPI + Bedrock App:
    
    1. SHORT TERM (Easiest):
       ✅ Use run_in_executor()
       - Change: 3-5 lines of code
       - Works with existing boto3
       - Good enough for most cases
       - Handles 100s of concurrent requests
    
    2. LONG TERM (Best):
       ✅ Switch to aioboto3
       - True async, best performance
       - Handles 1000s of concurrent requests
       - Future-proof
       - Minimal code changes
    
    3. PRODUCTION TIPS:
       ✓ Use connection pooling
       ✓ Set timeouts on all API calls
       ✓ Implement retry logic
       ✓ Add request rate limiting
       ✓ Monitor event loop lag
       ✓ Use background tasks for non-urgent work
    """)


# =============================================================================
# PART 6: FastAPI Async Best Practices
# =============================================================================


def fastapi_best_practices():
    """
    Best practices for async FastAPI.
    """
    print_section("PART 6: FastAPI Async Best Practices")

    print("""
    🏆 FASTAPI ASYNC BEST PRACTICES
    
    1. Route Handlers:
       ✓ Use 'async def' for I/O-bound endpoints
       ✓ Use 'def' for CPU-bound (FastAPI runs in threadpool)
       
       ```python
       @app.get("/fast")
       async def io_bound():  # I/O operations
           data = await fetch_from_api()
           return data
       
       @app.get("/compute")
       def cpu_bound():  # Heavy computation
           result = complex_calculation()
           return result
       ```
    
    2. Dependencies:
       ✓ Make dependencies async if they do I/O
       
       ```python
       async def get_db():
           # Async database connection
           async with database.session() as session:
               yield session
       
       @app.get("/data")
       async def get_data(db = Depends(get_db)):
           return await db.query(...)
       ```
    
    3. Background Tasks:
       ✓ Use BackgroundTasks for non-urgent work
       
       ```python
       from fastapi import BackgroundTasks
       
       async def log_interaction(data):
           await save_to_db(data)
       
       @app.post("/chat")
       async def chat(bg_tasks: BackgroundTasks):
           response = await get_response()
           bg_tasks.add_task(log_interaction, response)
           return response  # Return immediately
       ```
    
    4. Startup/Shutdown Events:
       ✓ Initialize connections at startup
       
       ```python
       @app.on_event("startup")
       async def startup():
           app.state.bedrock = await init_bedrock_client()
       
       @app.on_event("shutdown")
       async def shutdown():
           await app.state.bedrock.close()
       ```
    
    5. Error Handling:
       ✓ Use timeouts
       ✓ Handle exceptions properly
       
       ```python
       @app.post("/chat")
       async def chat(prompt: str):
           try:
               response = await asyncio.wait_for(
                   bedrock_call(prompt),
                   timeout=30.0
               )
               return response
           except asyncio.TimeoutError:
               raise HTTPException(504, "Request timeout")
           except Exception as e:
               raise HTTPException(500, str(e))
       ```
    
    6. Monitoring:
       ✓ Track event loop lag
       ✓ Monitor response times
       ✓ Log slow requests
       
       ```python
       import time
       
       @app.middleware("http")
       async def log_requests(request, call_next):
           start = time.time()
           response = await call_next(request)
           duration = time.time() - start
           
           if duration > 1.0:
               logger.warning(f"Slow request: {duration:.2f}s")
           
           return response
       ```
    """)


# =============================================================================
# MAIN: Run All Demos
# =============================================================================


def main():
    """
    Main function to run all demonstrations.
    """
    print("\n" + "🎓" * 35)
    print("  BONUS: FASTAPI ASYNC DEEP DIVE")
    print("🎓" * 35)

    # Part 1: Why async
    explain_fastapi_async()
    input("\n⏸️  Press Enter to continue...")

    # Part 3: Executor solution
    explain_executor_solution()
    input("\n⏸️  Press Enter to continue...")

    # Part 4: aioboto3 solution
    explain_aioboto3_solution()
    input("\n⏸️  Press Enter to continue...")

    # Part 5: Comparison
    comparison_table()
    input("\n⏸️  Press Enter to continue...")

    # Part 6: Best practices
    fastapi_best_practices()

    print("\n" + "=" * 70)
    print("🎉 BONUS LESSON COMPLETE!")
    print("=" * 70)
    print("\n📚 Key Takeaways:")
    print("   1. FastAPI is built on async for high concurrency")
    print("   2. boto3 is blocking - use run_in_executor()")
    print("   3. aioboto3 offers true async boto3")
    print("   4. Use 'async def' for I/O-bound routes")
    print("   5. Use BackgroundTasks for non-urgent work")
    print("\n🚀 Apply this to your FastAPI + Bedrock app!")
    print("   Update basics/basic_fastapi.py with run_in_executor()")


if __name__ == "__main__":
    main()
