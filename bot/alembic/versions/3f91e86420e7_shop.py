"""shop

Revision ID: 3f91e86420e7
Revises: a418029bd5a5
Create Date: 2024-05-17 05:12:30.631969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f91e86420e7'
down_revision: Union[str, None] = 'a418029bd5a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('cards', sa.Column('cost', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'ownedcards', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ownedcards', type_='unique')
    op.drop_column('cards', 'cost')
    op.drop_table('shop')
    # ### end Alembic commands ###