"""add few more columns to post table

Revision ID: 80dc24dc43f7
Revises: 9dd48fd79c02
Create Date: 2025-09-03 23:32:41.382025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80dc24dc43f7'
down_revision: Union[str, Sequence[str], None] = '9dd48fd79c02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column(
                'published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
