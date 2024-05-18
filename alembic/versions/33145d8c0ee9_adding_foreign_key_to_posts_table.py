"""adding foreign key to posts table

Revision ID: 33145d8c0ee9
Revises: 9fbded6e9e05
Create Date: 2024-05-18 18:32:08.634303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33145d8c0ee9'
down_revision: Union[str, None] = '9fbded6e9e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('posts_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    pass
