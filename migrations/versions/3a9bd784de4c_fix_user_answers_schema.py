"""fix user_answers schema

Revision ID: 3a9bd784de4c
Revises: 87e77ecd4e33
Create Date: 2026-06-10 11:43:18.661770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a9bd784de4c'
down_revision: Union[str, Sequence[str], None] = '87e77ecd4e33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
