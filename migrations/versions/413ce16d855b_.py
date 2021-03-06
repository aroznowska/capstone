"""empty message

Revision ID: 413ce16d855b
Revises: 18406084b32e
Create Date: 2022-03-09 17:28:07.071565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '413ce16d855b'
down_revision = '18406084b32e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('center', 'created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('center', sa.Column('created', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
