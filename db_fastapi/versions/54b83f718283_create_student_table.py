"""create student table

Revision ID: 54b83f718283
Revises: 
Create Date: 2025-01-08 12:22:41.404833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54b83f718283'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('student',
                    sa.Column('S_id',sa.Integer(),nullable=False),
                    sa.Column('S_name',sa.String(),nullable=False),
                    sa.Column('Roll_no',sa.Integer(),nullable=False),
                    sa.Column('Created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('S_id'),
                    sa.UniqueConstraint('Roll_no'))
def downgrade() -> None:
    op.drop_table('student')