"""create_users_table

Revision ID: e50ead1b8f01
Revises: 
Create Date: 2026-01-28 09:23:56.941311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e50ead1b8f01'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id',sa.Integer(),primary_key =True,nullable=False),
                    sa.Column('email',sa.String(),nullable=False,unique = True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
