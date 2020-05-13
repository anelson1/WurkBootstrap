"""empty message

Revision ID: a23ed67a4296
Revises: 4d1f50ebd068
Create Date: 2020-05-12 19:00:14.204810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a23ed67a4296'
down_revision = '4d1f50ebd068'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'client', ['bookingid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'client', type_='unique')
    # ### end Alembic commands ###
