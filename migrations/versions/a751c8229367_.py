"""empty message

Revision ID: a751c8229367
Revises: 47fee9d06e22
Create Date: 2020-09-06 18:28:43.577802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a751c8229367'
down_revision = '47fee9d06e22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_mail', sa.String(length=100), nullable=True))
    op.drop_column('vehicles', 'company_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('company_email', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('vehicles', 'company_mail')
    # ### end Alembic commands ###