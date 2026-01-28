"""create_fk

Revision ID: a2dd125aaac7
Revises: d1e4909e8268
Create Date: 2026-01-28 09:33:28.520282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2dd125aaac7'
down_revision: Union[str, Sequence[str], None] = 'd1e4909e8268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_user_fk',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
