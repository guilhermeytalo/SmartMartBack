"""Make category_id non-nullable

Revision ID: 61ad3cb4292e
Revises: 361541998fc8
Create Date: 2025-05-08 11:15:02.678869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '61ad3cb4292e'
down_revision: Union[str, None] = '361541998fc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('products', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)


def downgrade() -> None:
    op.alter_column('products', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
