"""empty message

Revision ID: 79c4486e1505
Revises: aa60c803adc8
Create Date: 2019-12-03 15:05:43.069961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c4486e1505'
down_revision = 'aa60c803adc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cuisines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('AccountsCuisines',
    sa.Column('accounts_id', sa.Integer(), nullable=True),
    sa.Column('cuisines_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['accounts_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['cuisines_id'], ['cuisines.id'], )
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('restaurant', sa.String(length=20), nullable=False),
    sa.Column('content', sa.String(length=120), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('location_long', sa.String(length=120), nullable=True),
    sa.Column('location_lat', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('content')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('AccountsCuisines')
    op.drop_table('cuisines')
    op.drop_table('accounts')
    # ### end Alembic commands ###
