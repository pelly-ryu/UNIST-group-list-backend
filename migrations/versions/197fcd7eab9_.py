"""empty message

Revision ID: 197fcd7eab9
Revises: 461efb886fa
Create Date: 2018-02-26 18:13:24.897821

"""

# revision identifiers, used by Alembic.
revision = '197fcd7eab9'
down_revision = '461efb886fa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('club_club', sa.Column('contact', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('club_club', 'contact')
    ### end Alembic commands ###