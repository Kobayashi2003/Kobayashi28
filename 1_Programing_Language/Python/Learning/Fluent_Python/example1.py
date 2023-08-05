import asyncio

async def main():
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")

coro = main()

asyncio.run(coro)