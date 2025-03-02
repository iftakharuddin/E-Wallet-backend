"""empty message

Revision ID: cb81cfef3877
Revises: 
Create Date: 2025-02-28 23:15:34.345669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cb81cfef3877'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('user_type', postgresql.ENUM('NORMAL', 'ADMIN', 'AGENT', name='usertype'), nullable=False),
    sa.Column('registration_no', sa.UUID(), nullable=False),
    sa.Column('mobile_operator', sa.String(length=10), nullable=False),
    sa.Column('otp', sa.String(length=6), nullable=True),
    sa.Column('otp_verified', sa.Boolean(), nullable=False),
    sa.Column('otp_expired_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('registration_no')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=True),
    sa.Column('first_name', sa.String(length=25), nullable=True),
    sa.Column('last_name', sa.String(length=25), nullable=True),
    sa.Column('user_type', postgresql.ENUM('NORMAL', 'ADMIN', 'AGENT', name='usertype'), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('NID_front', sa.String(length=100), nullable=True),
    sa.Column('NID_back', sa.String(length=100), nullable=True),
    sa.Column('photo', sa.String(length=100), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=False),
    sa.Column('income_source', sa.String(length=50), nullable=True),
    sa.Column('monthly_income_amount', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('designation', sa.String(length=25), nullable=True),
    sa.Column('status', sa.Enum('LOCKED', 'INACTIVE', 'ACTIVE', name='status'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    op.drop_table('users')
    op.drop_table('registration')
    # ### end Alembic commands ###
