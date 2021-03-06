# models.py
# (c) Rice Apps 2017

from database import db
from flask_sqlalchemy import Model, SQLAlchemy
from collections import OrderedDict

def serialize_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

class BlueButtonRequest(db.Model):
    __tablename__ = 'request'
    request_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.case_id'), nullable=False)
    device_id = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    case = db.relationship('Case', backref=db.backref('bb-case-tracking'), lazy=True)
    
    # Optional?
    # def __init__(self, request_id, case_id, device_id, longitude, latitude, timestamp, case):
    #     self.request_id = request_id
    #     self.case_id = case_id
    #     self.device_id = device_id
    #     self.longitude = longitude
    #     self.latitude = latitude
    #     self.timestamp = timestamp
    #     self.case = case

    def __repr__(self):
        return "ID: {} - [{}] Lat {}, Long {}".format(self.case_id, self.timestamp, self.latitude, self.longitude)
    
    def serialize(self):
        return {
            "request_id": self.request_id,
            "case_id": self.case_id,
            "device_id": self.device_id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "timestamp": serialize_datetime(self.timestamp)
        }
    
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result
	
class Case(db.Model):
    __tablename__ = 'case'
    case_id = db.Column(db.Integer, primary_key=True)
    resolved = db.Column(db.Integer)
	
    def __repr__(self):
        return "ID <{}>".format(self.case_id)

    def serialize(self):
        return {
            "case_id": self.case_id,
            "resolved": self.resolved
        }
    
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)

        return result
	
class Number(db.Model):
    __tablename__ = 'numbers'
    name = db.Column(db.Text, primary_key=True)
    number = db.Column(db.Text)
    on_campus = db.Column(db.Integer)
    all_day = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __repr__(self):
        return "Number <{}>".format(self.name)

    def serialize(self):
        return {
            "name": self.name,
            "number": self.number,
            "on_campus": self.on_campus,
            "all_day": self.all_day,
            "description": self.description
        }
