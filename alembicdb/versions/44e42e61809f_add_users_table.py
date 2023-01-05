"""Add Users Table

Revision ID: 44e42e61809f
Revises: 06d6e7da8cef
Create Date: 2023-01-04 22:09:04.187209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = '44e42e61809f'
down_revision = '06d6e7da8cef'
branch_labels = None
depends_on = None


# Create the users table. PrimaryKeyConstraint create the primary_key. Other way
def upgrade():
    op.execute('CREATE EXTENSION "uuid-ossp";') 
    op.create_table("users",
        sa.Column("id", UUID(as_uuid=True),server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column("email", sa.String(),nullable=False),
        sa.Column("password", sa.String(),nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"))

    pass


def downgrade():
    op.drop_table("users")
    pass
