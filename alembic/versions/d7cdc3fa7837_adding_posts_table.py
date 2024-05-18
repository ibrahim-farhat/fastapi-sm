"""adding posts table

Revision ID: d7cdc3fa7837
Revises: 
Create Date: 2024-05-18 16:04:42.859845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7cdc3fa7837'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts')
    op.add_column('posts', sa.Column('title', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True))
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
