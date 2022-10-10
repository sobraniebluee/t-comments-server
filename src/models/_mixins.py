from src.db import db
from sqlalchemy import func


class Timestamp(object):
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
