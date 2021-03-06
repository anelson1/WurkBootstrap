"""empty message

Revision ID: 534f0bf46acb
Revises: 
Create Date: 2020-05-12 00:59:54.350750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '534f0bf46acb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('personal_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('phonenumber', sa.String(length=128), nullable=True),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('state', sa.String(length=128), nullable=True),
    sa.Column('firstname', sa.String(length=128), nullable=True),
    sa.Column('lastname', sa.String(length=128), nullable=True),
    sa.Column('person', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personal_info')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
