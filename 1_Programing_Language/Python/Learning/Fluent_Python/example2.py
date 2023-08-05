import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return f"{what} - {delay}"


async def main():


    print(f"started at {time.strftime('%X')}")

    ret = await asyncio.gather(
        say_after(1, 'hello'),
        say_after(2, 'world'),
    )

    print(ret)

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
