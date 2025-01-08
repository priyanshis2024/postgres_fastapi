"""Remove foreign key constraint

Revision ID: 2e9b4aa87635
Revises: 8206e6741f67
Create Date: 2025-01-08 15:27:44.777551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e9b4aa87635'
down_revision: Union[str, None] = '8206e6741f67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('Sf_id',table_name='s_detail')

def downgrade() -> None:
    op.create_foreign_key(
        'fk_student_s_detail',  # It's better to name the constraint clearly
        source_table='student',  # The source table (the one holding the foreign key)
        referent_table='s_detail',  # The referent table (the one being referenced)
        local_cols=['S_id'],  # The column(s) in the source table
        remote_cols=['Sf_id'],  # The column(s) in the referent table
        ondelete='CASCADE'  # Action to take when a referenced row in s_detail is deleted
    )
    
