"""Add brand column to products table

Revision ID: 361541998fc8
Revises: faace2ba43ba
Create Date: 2025-05-07 14:18:36.949261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '361541998fc8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create categories table first
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
    )
    
    # Create products table with FK
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id'), nullable=False),
        sa.Column('brand', sa.String(length=255), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('products')
    op.drop_table('categories')
