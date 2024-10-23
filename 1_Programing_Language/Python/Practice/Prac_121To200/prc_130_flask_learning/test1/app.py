from flask import Flask, request

app = Flask(__name__)

class MyHandler:
    def __init__(self, greeting):
        self.greeting = greeting
    
    def __call__(self, *args, **kwargs):
        name = request.args.get('name', 'Guest')
        return f"{self.greeting}, {name}!"

# 实例化对象
hello_handler = MyHandler("Hello")
goodbye_handler = MyHandler("Goodbye")

# 将URL绑定到实例化的对象
app.add_url_rule('/hello', 'hello', hello_handler)
app.add_url_rule('/goodbye', 'goodbye', goodbye_handler)

if __name__ == '__main__':
    app.run(debug=True)