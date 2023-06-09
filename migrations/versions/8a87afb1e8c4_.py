"""empty message

Revision ID: 8a87afb1e8c4
Revises: 13be17f9c8d9
Create Date: 2020-09-05 19:23:41.693181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a87afb1e8c4'
down_revision = '13be17f9c8d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('state_id', sa.Integer(), nullable=True))
    op.drop_column('cities', 'state')
    op.add_column('vehicles', sa.Column('company_mail', sa.String(length=100), nullable=True))
    op.drop_column('vehicles', 'company_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_email', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('vehicles', 'company_mail')
    op.add_column('cities', sa.Column('state', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('cities', 'state_id')
    # ### end Alembic commands ###
