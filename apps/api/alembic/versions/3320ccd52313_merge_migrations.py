"""merge migrations

Revision ID: 3320ccd52313
Revises: 0001, 571cffb33f0a
Create Date: 2025-10-06 12:15:54.448887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3320ccd52313'
down_revision: Union[str, Sequence[str], None] = ('0001', '571cffb33f0a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
