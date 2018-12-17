import asyncio
from asyncio import AbstractEventLoop

loop = asyncio.get_event_loop()


def get_loop(loop_current: loop) -> AbstractEventLoop:
    if not loop_current:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
