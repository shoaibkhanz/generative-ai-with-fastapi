import asyncio
import time

# synchrous code
# def task():
#     print("Start of sync task")
#     time.sleep(3)
#     print("After 3 seconds of sleep")
#
#
# start = time.time()
# for _ in range(3):
#     task()
#
# duration = time.time() - start
# print(f"process completed in {duration} seconds")


# asynchronous code


async def task():
    print("Start of sync task")
    await asyncio.sleep(3)
    print("async task resumed after 3 seconds")


async def spawn_tasks():
    await asyncio.gather(task(), task(), task())


start = time.time()

asyncio.run(spawn_tasks())

duration = time.time() - start
print(f"process completed in {duration} seconds")
