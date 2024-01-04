from . import db
from datetime import datetime

# Make a table named user, with three columns, uid, name, gender
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'uid': self.uid,
            'name': self.name,
            'gender': self.gender
        }