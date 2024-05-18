"""empty message

Revision ID: 39eeab4c8549
Revises: 5226129d64c2
Create Date: 2024-04-02 11:23:55.099706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39eeab4c8549'
down_revision = '5226129d64c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processed_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('layer', sa.Integer(), nullable=True))
        batch_op.drop_column('img_url')
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processed_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), nullable=True))
        batch_op.add_column(sa.Column('img_url', sa.VARCHAR(length=80), nullable=True))
        batch_op.drop_column('layer')

    # ### end Alembic commands ###