import importlib

def load_module(module_name):
    return importlib.import_module(module_name)

def reload_module(module):
    return importlib.reload(module)


if __name__ == '__main__':
    module_name = 'example_module'

    with open('example_module.py', 'w') as f:
        f.write('def say_hello():\n')
        f.write('    print("Hello!")\n')

    print('Loading module...')
    example_module = load_module(module_name)
    example_module.say_hello()

    with open('example_module.py', 'w') as f:
        f.write('def say_hello():\n')
        f.write('    print("Hello World!")\n')

    print('Reloading module...')
    importlib.invalidate_caches()
    example_module = reload_module(example_module)
    example_module.say_hello()