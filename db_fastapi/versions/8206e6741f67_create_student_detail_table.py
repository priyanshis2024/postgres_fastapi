"""Create Student detail table

Revision ID: 8206e6741f67
Revises: 54b83f718283
Create Date: 2025-01-08 14:39:33.567701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8206e6741f67'
down_revision: Union[str, None] = '54b83f718283'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('s_detail',
                    sa.Column('Roll_no',sa.Integer(),nullable=False),
                    sa.Column('Sf_id',sa.Integer(),nullable=False),
                    sa.Column('S_name',sa.String(),nullable=False),
                    sa.Column('Email',sa.String(),nullable=False),
                    sa.Column('Gender',sa.String(),nullable=False),
                    sa.Column('Address',sa.String(),nullable=True),
                    sa.Column('Semester',sa.Integer(),nullable=False),
                    sa.Column('Created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('Roll_no'),
                    sa.UniqueConstraint('Email'),
                    sa.ForeignKeyConstraint(['Sf_id'],['student.S_id']))

def downgrade() -> None:
    op.drop_table('s_detail')