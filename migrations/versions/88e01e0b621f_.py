"""empty message

Revision ID: 88e01e0b621f
Revises: b5758e8413da
Create Date: 2020-05-13 07:43:00.818178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88e01e0b621f'
down_revision = 'b5758e8413da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('image_link', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'image_link')
    op.drop_column('Artist', 'image_link')
    # ### end Alembic commands ###
