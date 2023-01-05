"""Add foreign_key to Posts Table

Revision ID: 98d57de9aead
Revises: 44e42e61809f
Create Date: 2023-01-04 22:25:25.108625

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = '98d57de9aead'
down_revision = '44e42e61809f'
branch_labels = None
depends_on = None


# Adding the forain_key for the posts table
def upgrade():
    op.add_column("posts", sa.Column("owner_id", UUID(as_uuid=True), nullable=False))

    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
