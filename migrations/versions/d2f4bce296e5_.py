"""empty message

Revision ID: d2f4bce296e5
Revises: a2a8ec8c8477
Create Date: 2020-09-14 09:10:01.296500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2f4bce296e5'
down_revision = 'a2a8ec8c8477'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle_tbl', sa.Column('name', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle_tbl', 'name')
    # ### end Alembic commands ###
