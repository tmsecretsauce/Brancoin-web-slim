"""pack desc

Revision ID: 115ddf43f463
Revises: 1a28535d39fb
Create Date: 2024-05-18 18:30:03.355306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '115ddf43f463'
down_revision: Union[str, None] = '1a28535d39fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booster_pack', sa.Column('desc', sa.String(), server_default='', nullable=False))
    op.create_unique_constraint(None, 'cards', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cards', type_='unique')
    op.drop_column('booster_pack', 'desc')
    # ### end Alembic commands ###
