"""empty message

Revision ID: 8f84a2bbdb1b
Revises: 3176be20566f
Create Date: 2024-03-31 21:28:09.384251

"""
from alembic import op
import sqlalchemy as sa
import model

# revision identifiers, used by Alembic.
revision = '8f84a2bbdb1b'
down_revision = '3176be20566f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_mod', model.ISODateTime(length=19), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_mod')

    # ### end Alembic commands ###
