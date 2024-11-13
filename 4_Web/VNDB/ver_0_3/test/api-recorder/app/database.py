from app import db

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    host = db.Column(db.String(200), nullable=False)
    route = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    params = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'host': self.host,
            'route': self.route,
            'method': self.method,
            'params': self.params,
            'body': self.body,
            'created_at': self.created_at.isoformat()
        }