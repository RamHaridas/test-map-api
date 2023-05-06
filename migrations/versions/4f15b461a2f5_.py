"""empty message

Revision ID: 4f15b461a2f5
Revises: 3e29688f0856
Create Date: 2020-10-05 12:10:34.602670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f15b461a2f5'
down_revision = '3e29688f0856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('owners', sa.Column('address_proof', sa.LargeBinary(), nullable=True))
    op.add_column('owners', sa.Column('address_proof_filename', sa.String(), nullable=True))
    op.add_column('owners', sa.Column('pan_file', sa.LargeBinary(), nullable=True))
    op.add_column('owners', sa.Column('pan_filename', sa.String(), nullable=True))
    op.drop_column('owners', 'pan_image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('owners', sa.Column('pan_image', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('owners', 'pan_filename')
    op.drop_column('owners', 'pan_file')
    op.drop_column('owners', 'address_proof_filename')
    op.drop_column('owners', 'address_proof')
    # ### end Alembic commands ###
