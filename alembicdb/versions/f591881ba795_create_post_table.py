"""Create Post Table

Revision ID: f591881ba795
Revises: 
Create Date: 2023-01-04 21:52:25.708851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = 'f591881ba795'
down_revision = None
branch_labels = None
depends_on = None


# This functin handle the logig to crate a table. 
def upgrade():
  op.create_table('posts', 
  sa.Column('id', UUID(as_uuid=True), nullable=False, server_default=sa.text('uuid_generate_v4()'), primary_key=True), 
  sa.Column('title', sa.String(), nullable=False))

#   op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
  
  pass


  # for create the table we drop thetable
def downgrade():
  op.drop_table('posts')
  pass
