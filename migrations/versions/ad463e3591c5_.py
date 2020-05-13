"""empty message

Revision ID: ad463e3591c5
Revises: 2c06ec7f8cbe
Create Date: 2020-05-12 18:57:15.884186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad463e3591c5'
down_revision = '2c06ec7f8cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'booking', ['bookingid'])
    op.add_column('booking_time', sa.Column('bid', sa.String(length=6), nullable=True))
    op.create_unique_constraint(None, 'booking_time', ['bookingid'])
    op.create_foreign_key(None, 'booking_time', 'booking', ['bid'], ['bookingid'])
    op.create_unique_constraint(None, 'client', ['bookingid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'client', type_='unique')
    op.drop_constraint(None, 'booking_time', type_='foreignkey')
    op.drop_constraint(None, 'booking_time', type_='unique')
    op.drop_column('booking_time', 'bid')
    op.drop_constraint(None, 'booking', type_='unique')
    # ### end Alembic commands ###
