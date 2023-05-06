"""empty message

Revision ID: 9cdb9dbfb7f2
Revises: aa1a1697b7bc
Create Date: 2020-09-20 09:12:26.423159

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9cdb9dbfb7f2'
down_revision = 'aa1a1697b7bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('google_image', sa.String(), nullable=True))
    op.add_column('user', sa.Column('image', sa.LargeBinary(), nullable=True))
    op.drop_column('user', 'image_bin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_bin', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('user', 'image')
    op.drop_column('user', 'google_image')
    # ### end Alembic commands ###