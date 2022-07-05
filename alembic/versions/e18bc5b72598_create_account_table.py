"""create Account table

Revision ID: e18bc5b72598
Revises: 
Create Date: 2022-07-04 16:15:35.979237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e18bc5b72598'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('hash_password', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), default=True),
        sa.Column('token', sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('accounts')
