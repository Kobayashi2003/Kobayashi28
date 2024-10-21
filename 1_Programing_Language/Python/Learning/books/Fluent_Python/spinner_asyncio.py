import itertools
import sys
import asyncio

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + " " + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    write(" " * len(status) + "\x08" * len(status))


async def slow_function():
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin("thinking!"))
    print("spinner object:", spinner)
    result = await slow_function()
    spinner.cancel()
    return result


def main():
    result = asyncio.run(supervisor())
    print("Answer:", result)


if __name__ == "__main__":
    main()