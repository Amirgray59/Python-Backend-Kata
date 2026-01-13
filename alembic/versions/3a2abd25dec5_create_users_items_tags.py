
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3a2abd25dec5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False, unique=True),
    )

    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('sell_in', sa.Integer(), nullable=False),
        sa.Column('quality', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        'ix_items_owner_id',
        'items',
        'users',
        ['owner_id'],
        ['id'],
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    )


def downgrade():
    op.drop_table('tags')
    op.drop_table('items')
    op.drop_table('users')
