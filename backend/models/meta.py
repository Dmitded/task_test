from sqlalchemy.ext.declarative import declarative_base
from libs.sqlalchemy import CustomQuery, base_model
from db.session import Session

Base = declarative_base(cls=base_model(Session))
