"""empty message

Revision ID: a22b910ce87a
Revises: 9c211d20dc93
Create Date: 2020-09-13 16:27:22.808382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22b910ce87a'
down_revision = '9c211d20dc93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('owners', sa.Column('city', sa.String(length=80), nullable=True))
    op.add_column('owners', sa.Column('state', sa.String(length=80), nullable=True))
    op.drop_constraint('owners_city_id_fkey', 'owners', type_='foreignkey')
    op.drop_constraint('owners_state_id_fkey', 'owners', type_='foreignkey')
    op.drop_column('owners', 'city_id')
    op.drop_column('owners', 'state_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('owners', sa.Column('state_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('owners', sa.Column('city_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('owners_state_id_fkey', 'owners', 'states_tbl', ['state_id'], ['id'])
    op.create_foreign_key('owners_city_id_fkey', 'owners', 'cities', ['city_id'], ['id'])
    op.drop_column('owners', 'state')
    op.drop_column('owners', 'city')
    # ### end Alembic commands ###
