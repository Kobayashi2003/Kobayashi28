from flask import Flask, url_for, render_template

app = Flask(__name__)

def get_dirs():
    # get all dirs in static/images
    import os 
    dirs_name = os.listdir('./static/images')
    files_num = []
    first_file = []

    for dir in dirs_name:
        count = 0
        for file in os.listdir('./static/images/' + dir):
            count += 1
            if count == 1:
                first_file.append(file)
        files_num.append(count)
    dirs = [(dirs_name[i], files_num[i], first_file[i]) for i in range(len(dirs_name))]
    return dirs


@app.route('/')
def index():
    dirs = get_dirs()
    return render_template('index.html', dirs=dirs) 


@app.route('/<dir_name>')
def show_dir(dir_name):
    import os
    files_tmp = os.listdir('./static/images/' + dir_name)
    files = []
    new_dirname = dir_name
    while files_tmp:
        if os.path.isdir('./static/images/' + dir_name + '/' + files_tmp[0]):
            files_tmp.extend(os.listdir('./static/images/' + dir_name + '/' + files_tmp[0]))
            new_dirname = dir_name + '/' + files_tmp[0]
            files_tmp.pop(0)
        else:
            files.append(files_tmp.pop(0))
    # return f'files: {files}'
    dir_name = new_dirname
    return render_template('viewer.html', files=files, dir_name=dir_name)

# if __name__ == '__main__':
#     show_dir('1')


@app.route('/num/<int:num>')
def show_number(num):
    return f'Hello, {num}!'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# with app.test_request_context():
#     print(url_for('hello_world'))
#     print(url_for('show_number', num=42))
#     print(url_for('show_user_profile', username='John Doe'))