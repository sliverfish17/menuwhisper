"""add user_feedback table

Revision ID: 56564863460e
Revises: dcf136e41319
Create Date: 2024-12-21 12:55:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '56564863460e'
down_revision = 'dcf136e41319'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_feedback table
    op.create_table('user_feedback',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('menu_item_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('liked', sa.Boolean(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('review_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop user_feedback table
    op.drop_table('user_feedback')