"""add users table

Revision ID: 090bd01b3f3c
Revises: 7ddc7c9066ee
Create Date: 2024-05-18 16:27:04.857569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '090bd01b3f3c'
down_revision: Union[str, None] = '7ddc7c9066ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass