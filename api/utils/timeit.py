import asyncio
import functools
import time
from asyncio.log import logger


def timeit(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                total_time = time.perf_counter() - start_time
                logger.info(f"Is a coroutine function name: \"{func.__name__}\"  time:{total_time:.6f} seconds")
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                runtime = time.perf_counter() - start_time
                logger.info(f"Is a normal function name: \"{func.__name__}\" time:{runtime:.6f} secs")
        return wrapper
