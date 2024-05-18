"""empty message

Revision ID: e7d8c49f50c8
Revises: 3f91e86420e7
Create Date: 2024-05-18 05:28:02.554244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7d8c49f50c8'
down_revision: Union[str, None] = '3f91e86420e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shop', sa.Column('featured', sa.Boolean(), server_default='False', nullable=False))
    op.add_column('shop', sa.Column('date_added', sa.Date(), server_default='2024-05-18', nullable=False))
    op.create_unique_constraint(None, 'shop', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shop', type_='unique')
    op.drop_column('shop', 'date_added')
    op.drop_column('shop', 'featured')
    # ### end Alembic commands ###
