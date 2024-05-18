"""adding posts[id] as primary key

Revision ID: 9fbded6e9e05
Revises: 090bd01b3f3c
Create Date: 2024-05-18 18:25:24.113583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fbded6e9e05'
down_revision: Union[str, None] = '090bd01b3f3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_primary_key('posts_pk', table_name='posts', columns=['id'])
    pass


def downgrade() -> None:
    op.drop_constraint('posts_pk', table_name="posts")
    pass
