"""add foreign-key to post table

Revision ID: 9dd48fd79c02
Revises: 03bcf9474325
Create Date: 2025-09-03 23:17:41.414802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dd48fd79c02'
down_revision: Union[str, Sequence[str], None] = '03bcf9474325'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
