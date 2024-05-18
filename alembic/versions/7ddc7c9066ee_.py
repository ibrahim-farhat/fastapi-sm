"""empty message

Revision ID: 7ddc7c9066ee
Revises: d7cdc3fa7837
Create Date: 2024-05-18 16:23:59.584993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ddc7c9066ee'
down_revision: Union[str, None] = 'd7cdc3fa7837'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users')
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_primary_key('users_pk', table_name='users', columns=['id'])
    op.create_unique_constraint('email_uc', columns=['email'], table_name='users')
    pass


def downgrade() -> None:
    op.drop_table('users')
    op.drop_constraint('users_pk', table_name="users")
    op.drop_constraint('email_uc', table_name="users")
    pass
