"""Add role and is_approved columns

Revision ID: c7d7bb6b926f
Revises: 
Create Date: 2025-04-27 08:05:01.922469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7d7bb6b926f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.Enum('GUEST', 'USER', 'ORG_DEPUTY', 'ORG_LEADER', 'ADMIN_OBSERVER', 'CHIEF_OBSERVER_DEPUTY', 'CHIEF_OBSERVER', 'CURATOR', 'CHIEF_ADMIN_DEPUTY', 'CHIEF_ADMIN', 'SITE_SUPPORT', 'SITE_DEVELOPER', 'SITE_FOUNDER', name='userrole'), nullable=True))
    op.add_column('users', sa.Column('is_approved', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_approved')
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
