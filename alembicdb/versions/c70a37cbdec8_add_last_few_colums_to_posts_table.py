"""Add last few Colums to Posts Table

Revision ID: c70a37cbdec8
Revises: 98d57de9aead
Create Date: 2023-01-04 22:32:34.871540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c70a37cbdec8'
down_revision = '98d57de9aead'
branch_labels = None
depends_on = None


# Add last few Colums to Posts Table
def upgrade() :
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False,  server_default="TRUE"),)

    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "create_at")
    pass

