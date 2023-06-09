"""empty message

Revision ID: 135cca6e14f8
Revises: 0d517e3e7cf9
Create Date: 2020-09-19 14:39:23.359306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135cca6e14f8'
down_revision = '0d517e3e7cf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image_model', sa.Column('image', sa.LargeBinary(), nullable=True))
    op.drop_column('image_model', 'img')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image_model', sa.Column('img', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('image_model', 'image')
    # ### end Alembic commands ###
