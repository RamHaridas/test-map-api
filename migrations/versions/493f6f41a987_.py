"""empty message

Revision ID: 493f6f41a987
Revises: 8a87afb1e8c4
Create Date: 2020-09-05 19:24:29.537285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '493f6f41a987'
down_revision = '8a87afb1e8c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cities', 'state')
    op.add_column('vehicles', sa.Column('company_mail', sa.String(length=100), nullable=True))
    op.drop_column('vehicles', 'company_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_email', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('vehicles', 'company_mail')
    op.add_column('cities', sa.Column('state', sa.VARCHAR(length=100), nullable=True))
    # ### end Alembic commands ###
