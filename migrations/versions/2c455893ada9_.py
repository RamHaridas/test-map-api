"""empty message

Revision ID: 2c455893ada9
Revises: 0356d1ae60e9
Create Date: 2020-09-06 18:13:43.789314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c455893ada9'
down_revision = '0356d1ae60e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cities', 'state_id')
    op.add_column('vehicles', sa.Column('company_mail', sa.String(length=100), nullable=True))
    op.drop_column('vehicles', 'company_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_email', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('vehicles', 'company_mail')
    op.add_column('cities', sa.Column('state_id', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
