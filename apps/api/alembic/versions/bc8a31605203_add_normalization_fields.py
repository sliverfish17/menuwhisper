"""add normalization fields

Revision ID: bc8a31605203
Revises: 3320ccd52313
Create Date: 2024-12-21 12:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc8a31605203'
down_revision = '3320ccd52313'
branch_labels = None
depends_on = None


def upgrade():
    # Add normalization fields to menu_items
    op.add_column('menu_items', sa.Column('title_norm', sa.String(), nullable=True))
    op.add_column('menu_items', sa.Column('description_norm', sa.Text(), nullable=True))


def downgrade():
    # Remove normalization fields from menu_items
    op.drop_column('menu_items', 'description_norm')
    op.drop_column('menu_items', 'title_norm')