import asyncio
import concurrent
from functools import partial


async def to_async(func, *args, **keywords):
    executor = concurrent.futures.ThreadPoolExecutor()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, partial(func, *args, **keywords))


def to_sync(func, *args, **keywords):
    pool = concurrent.futures.ThreadPoolExecutor()
    return pool.submit(asyncio.run, func(*args, **keywords)).result()
