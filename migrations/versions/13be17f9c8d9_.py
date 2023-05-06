"""empty message

Revision ID: 13be17f9c8d9
Revises: 
Create Date: 2020-08-30 17:27:20.139711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13be17f9c8d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_email', sa.String(length=100), nullable=True))
    op.drop_column('vehicles', 'company_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_name', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('vehicles', 'company_email')
    # ### end Alembic commands ###
