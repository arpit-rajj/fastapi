"""create_posts_table

Revision ID: d1e4909e8268
Revises: e50ead1b8f01
Create Date: 2026-01-28 09:29:00.895369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e4909e8268'
down_revision: Union[str, Sequence[str], None] = 'e50ead1b8f01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('content',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
