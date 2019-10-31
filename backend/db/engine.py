from sqlalchemy import create_engine

from config import config


engine = create_engine(
    '{engine}://{username}:{password}@{host}:{port}/{db}'.format(
        **config['postgresql']
    )
)
