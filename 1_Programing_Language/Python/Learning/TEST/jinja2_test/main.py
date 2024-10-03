from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template('template.html')

context = {
    'navigation': [
        {'href': '/', 'caption': 'Home'},
        {'href': '/about', 'caption': 'About'},
        {'href': '/contact', 'caption': 'Contact'}
    ],
    'a_variable': 'Hello, World!'
}

output = template.render(context)

print(output)