"""create_workers_table

Revision ID: 812c388d8ffb
Revises: 
Create Date: 2019-10-29 19:23:27.718683

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


# revision identifiers, used by Alembic.
revision = '812c388d8ffb'
down_revision = None
branch_labels = None
depends_on = None


class WorkerType(Enum):
    COLLECTOR = 1
    INSPECTOR = 2


def upgrade():
    op.create_table(
        'worker',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ean13', sa.Integer, unique=True, nullable=False),
        sa.Column('password', sa.String(20), nullable=False),
        sa.Column('name', sa.String(15)),
        sa.Column('surname', sa.String(15)),
        sa.Column('middle_name', sa.String(15)),
        sa.Column('type', ENUM(WorkerType, name="worker_type"), nullable=False),
        sa.Column('deleted', sa.Boolean, default=False, nullable=False)
    )


def downgrade():
    op.drop_table('worker')
