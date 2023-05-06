"""empty message

Revision ID: 48e86d40a587
Revises: 78fd6f8105a3
Create Date: 2020-09-20 08:49:51.199973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e86d40a587'
down_revision = '78fd6f8105a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image_model', sa.Column('filename', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('image_model', 'filename')
    # ### end Alembic commands ###