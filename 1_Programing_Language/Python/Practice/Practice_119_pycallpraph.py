# https://graphviz.org/documentation/
# https://blog.csdn.net/qq_37177765/article/details/95886071
from pycallgraph2 import PyCallGraph, Config, GlobbingFilter
from pycallgraph2.output import GraphvizOutput

import asyncio


def print_test(num):
    print(f'print_test {num}')


async def test():
    for i in range(5):
        print_test(i)
        await asyncio.sleep(1)


async def test2():
    for i in range(10):
        print_test(i)
        await asyncio.sleep(0.5)


async def main():
    await asyncio.gather(test(), test2())
    print('main')


if __name__ == '__main__':
    import os
    config = Config(max_depth=10)
    ouput_file = os.path.join(os.path.dirname(__file__), 'filter_max_depth.png')
    graphviz = GraphvizOutput(output_file=ouput_file)
    with PyCallGraph(output=graphviz, config=config):
        import asyncio
        asyncio.run(main())
