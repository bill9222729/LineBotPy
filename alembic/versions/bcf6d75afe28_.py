"""empty message

Revision ID: bcf6d75afe28
Revises: c72c22a5237b
Create Date: 2020-06-10 11:09:13.122500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf6d75afe28'
down_revision = 'c72c22a5237b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('book_time', sa.DateTime(), nullable=True),
    sa.Column('is_confirm', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    # ### end Alembic commands ###