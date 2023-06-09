"""empty message

Revision ID: e981ae3ea5de
Revises: e04f77a5fc77
Create Date: 2020-09-24 11:46:15.853062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e981ae3ea5de'
down_revision = 'e04f77a5fc77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enquiry_tbl', sa.Column('lat_', sa.Float(), nullable=True))
    op.add_column('enquiry_tbl', sa.Column('lon_', sa.Float(), nullable=True))
    op.drop_column('enquiry_tbl', 'lat')
    op.drop_column('enquiry_tbl', 'lon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enquiry_tbl', sa.Column('lon', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('enquiry_tbl', sa.Column('lat', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('enquiry_tbl', 'lon_')
    op.drop_column('enquiry_tbl', 'lat_')
    # ### end Alembic commands ###
