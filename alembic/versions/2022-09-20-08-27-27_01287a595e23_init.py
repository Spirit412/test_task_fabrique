"""init

Revision ID: 01287a595e23
Revises: 
Create Date: 2022-09-21 21:27:27.565775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '01287a595e23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Т.к. использует ORM SQLAlchemy
    # Реляции в БД настраиваем через модели SQLAlchemy.

    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
        sa.Column('phone_number', sa.String(length=11), nullable=True, unique=True),
        sa.Column('phone_operator_code', sa.String(), nullable=False),
        sa.Column('tag', sa.String(), nullable=False),
        sa.Column('timezone', sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'mailings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
        sa.Column('sending_start_date', sa.DateTime(), nullable=False),  # Начало рассылки'
        sa.Column('sending_end_date', sa.DateTime(), nullable=False),  # Окончание рассылки
        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('client_filter_json', postgresql.JSONB(), default={}),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
        sa.Column('send_status', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        
        sa.Column('mailing_id', sa.Integer(), nullable=True),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'logs_clients',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
        
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('action', sa.Integer(), nullable=False),

        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('data_json', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'logs_mailings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),

        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('action', sa.Integer(), nullable=False),
        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('data_json', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        
        sa.Column('mailing_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'logs_messages',
        sa.Column('id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('action', sa.Integer(), nullable=False),
        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('data_json', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        
        sa.Column('message_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('logs_messages')
    op.drop_table('messages')
    op.drop_table('logs_mailings')
    op.drop_table('logs_clients')
    op.drop_table('mailings')
    op.drop_table('users')
