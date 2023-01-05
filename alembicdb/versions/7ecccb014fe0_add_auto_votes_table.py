"""Add Auto Votes Table

Revision ID: 7ecccb014fe0
Revises: c70a37cbdec8
Create Date: 2023-01-04 22:38:58.819605

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ecccb014fe0'
down_revision = 'c70a37cbdec8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_unique_constraint(None, 'posts', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'posts', type_='unique')
    op.drop_table('votes')
    # ### end Alembic commands ###
