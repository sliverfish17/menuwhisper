"""merge normalization fields

Revision ID: c29075254e7c
Revises: 5cf3c04026de, bc8a31605203
Create Date: 2025-10-06 15:32:01.122691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c29075254e7c'
down_revision: Union[str, Sequence[str], None] = ('5cf3c04026de', 'bc8a31605203')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
