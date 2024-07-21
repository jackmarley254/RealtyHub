"""Initial migration.

Revision ID: 6f86809c64a6
Revises: d2fd2e63a8af
Create Date: 2024-07-06 21:56:18.340887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f86809c64a6'
down_revision = 'd2fd2e63a8af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('properties')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('properties',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=200), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('property_type', sa.VARCHAR(length=200), nullable=False),
    sa.Column('property_status', sa.VARCHAR(length=200), nullable=False),
    sa.Column('bathrooms', sa.INTEGER(), nullable=False),
    sa.Column('bedrooms', sa.INTEGER(), nullable=False),
    sa.Column('size', sa.INTEGER(), nullable=False),
    sa.Column('available_from', sa.DATETIME(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=128), nullable=False),
    sa.Column('image_file', sa.VARCHAR(length=128), nullable=False),
    sa.Column('location', sa.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.Column('property_id', sa.INTEGER(), nullable=True),
    sa.Column('message', sa.TEXT(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
