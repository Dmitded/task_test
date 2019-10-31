"""create_activity_log_table

Revision ID: 5dbf60d1bceb
Revises: 812c388d8ffb
Create Date: 2019-10-29 21:02:31.285556

"""
from alembic import op
from _datetime import datetime as dt
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


# revision identifiers, used by Alembic.
revision = '5dbf60d1bceb'
down_revision = '812c388d8ffb'
branch_labels = None
depends_on = None


class ActivityType(Enum):
    SELECT_CONTENT_TYPE = 1
    COLLECT = 2
    REVIEW = 3


class ActivityStatus(Enum):
    SUCCESS = 1
    ERROR_CONTENT_TYPE_NOT_FOUND = 2
    ERROR_COLLECTOR_NOT_FOUND = 3
    ERROR_DUPLICATED = 4


def upgrade():
    op.create_table(
        'activity_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('box_code', sa.Integer(), nullable=False),
        sa.Column('worker_id', sa.Integer, sa.ForeignKey('worker.id')),
        sa.Column('payload', sa.Integer()),
        sa.Column('type', ENUM(ActivityType, name="type")),
        sa.Column('status', ENUM(ActivityStatus, name="status")),
        sa.Column('local_time', sa.DateTime()),
        sa.Column('server_time', sa.DateTime(), default=dt.now)
    )


def downgrade():
    op.drop_table('activity_log')
