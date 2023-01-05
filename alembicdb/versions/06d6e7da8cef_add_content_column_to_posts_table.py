"""Add content column to posts Table

Revision ID: 06d6e7da8cef
Revises: f591881ba795
Create Date: 2023-01-04 22:02:04.216127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d6e7da8cef'
down_revision = 'f591881ba795'
branch_labels = None
depends_on = None


# Ad Content Colum to Post Table
def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass