"""initial

Revision ID: 64b65df25441
Revises: 
Create Date: 2024-10-07 04:23:18.319659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.database.models import *
from app.database.enums import *
from sqlalchemy.orm import Session
from datetime import datetime, UTC


# revision identifiers, used by Alembic.
revision: str = '64b65df25441'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('telegram_username', sa.String(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'guest', 'member', name='role'), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('auto_pay', sa.Boolean(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=True)
    op.create_table('telegram_messages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('sender_id', sa.Uuid(), nullable=False),
    sa.Column('recipient_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tickets',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('holder_id', sa.Uuid(), nullable=False),
    sa.Column('opening_date', sa.DateTime(), nullable=False),
    sa.Column('closing_date', sa.DateTime(), nullable=False),
    sa.Column('is_open', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['holder_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('type', sa.Enum('refund', 'replenishment', 'withdrawal', name='transaction_type'), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('active_periods',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('transaction_id', sa.Uuid(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_messages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('type', sa.Enum('from_admin', 'from_user', name='message_ticket_type'), nullable=False),
    sa.Column('ticket_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    bind = op.get_bind()
    session = Session(bind=bind)

    default_users = [
        User(telegram_id=0, telegram_username="Admin", balance=0, role=Role.admin, active=True, auto_pay=False, created_date=datetime.now(UTC))
    ]

    session.add_all(default_users)
    session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket_messages')
    op.drop_table('active_periods')
    op.drop_table('transactions')
    op.drop_table('tickets')
    op.drop_table('telegram_messages')
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_table('users')

    op.execute('DROP TYPE role')
    op.execute('DROP TYPE message_ticket_type')
    op.execute('DROP TYPE transaction_type')
    # ### end Alembic commands ###
