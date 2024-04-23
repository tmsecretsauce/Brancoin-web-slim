"""empty message

Revision ID: 06b3d18f24b9
Revises: 8a7c3ea56cdb
Create Date: 2024-04-22 22:50:24.997894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06b3d18f24b9'
down_revision: Union[str, None] = '8a7c3ea56cdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('jackpot', 'guild')
    pass


def downgrade() -> None:
    op.rename_table('guild', 'jackpot')
    pass
