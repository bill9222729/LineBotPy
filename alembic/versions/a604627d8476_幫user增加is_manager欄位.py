"""幫USER增加is_manager欄位

Revision ID: a604627d8476
Revises: 20d4f3393114
Create Date: 2020-06-13 04:03:06.497204

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import Boolean

revision = 'a604627d8476'
down_revision = '20d4f3393114'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('is_manager', sa.Boolean(nullable=False, default=False)))


def downgrade():
    op.drop_colum('users', 'is_manager')
