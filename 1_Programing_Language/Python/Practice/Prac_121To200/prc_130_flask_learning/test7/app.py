from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 Test 模型
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# 定义事件监听器
@event.listens_for(Test, 'after_delete')
def receive_after_delete(mapper, connection, target):
    print(f"Test object with id {target.id} and name {target.name} was deleted!")

# 创建表
with app.app_context():
    db.create_all()

# 路由：创建测试数据
@app.route('/create/<name>')
def create_test(name):
    test = Test(name=name)
    db.session.add(test)
    db.session.commit()
    return jsonify({"message": f"Test object created with id {test.id}"})

# 路由：使用 ORM 删除测试数据
@app.route('/delete/orm/<int:id>')
def delete_test_orm(id):
    test = Test.query.get(id)
    if test:
        db.session.delete(test)
        db.session.commit()
        return jsonify({"message": f"Test object with id {id} deleted using ORM"})
    return jsonify({"message": "Test object not found"}), 404

# 路由：使用 query.delete() 删除测试数据
@app.route('/delete/query/<int:id>')
def delete_test_query(id):
    deleted = Test.query.filter_by(id=id).delete()
    db.session.commit()
    if deleted:
        return jsonify({"message": f"Test object with id {id} deleted using query.delete()"})
    return jsonify({"message": "Test object not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)