"""Initial migration for AI-Native Book + RAG Chatbot Platform

Revision ID: 001_initial
Revises: 
Create Date: 2025-12-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('profile_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('technical_background', sa.String(length=20), nullable=True),
        sa.Column('hardware_specs', sa.String(length=20), nullable=True),
        sa.Column('language_preference', sa.String(length=10), server_default='en', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('profile_id'),
        sa.UniqueConstraint('user_id')
    )

    # Add check constraints for user_profiles
    op.create_check_constraint(
        'ck_technical_background',
        'user_profiles',
        "technical_background IN ('beginner', 'intermediate', 'advanced')"
    )
    op.create_check_constraint(
        'ck_hardware_specs',
        'user_profiles',
        "hardware_specs IN ('low-end', 'mid-range', 'high-end')"
    )

    # Create personalization_preferences table
    op.create_table(
        'personalization_preferences',
        sa.Column('pref_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=100), nullable=True),
        sa.Column('content_level', sa.String(length=20), nullable=True),
        sa.Column('examples_preference', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('pref_id')
    )

    # Add check constraints for personalization_preferences
    op.create_check_constraint(
        'ck_content_level',
        'personalization_preferences',
        "content_level IN ('simplified', 'detailed', 'technical')"
    )
    op.create_check_constraint(
        'ck_examples_preference',
        'personalization_preferences',
        "examples_preference IN ('practical', 'theoretical')"
    )

    # Create book_content table
    op.create_table(
        'book_content',
        sa.Column('content_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('slug', sa.String(length=500), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('order_index', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['book_content.content_id'], ),
        sa.PrimaryKeyConstraint('content_id'),
        sa.UniqueConstraint('slug')
    )

    # Create chat_sessions table
    op.create_table(
        'chat_sessions',
        sa.Column('session_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('session_id')
    )

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('message_id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_type', sa.String(length=10), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('context_reference', sa.String(length=100), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.session_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('message_id')
    )

    # Add check constraint for chat_messages
    op.create_check_constraint(
        'ck_sender_type',
        'chat_messages',
        "sender_type IN ('user', 'assistant')"
    )

    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_book_content_slug', 'book_content', ['slug'])
    op.create_index('ix_book_content_type', 'book_content', ['content_type'])
    op.create_index('ix_chat_sessions_user', 'chat_sessions', ['user_id'])
    op.create_index('ix_chat_messages_session', 'chat_messages', ['session_id'])
    op.create_index('ix_chat_messages_timestamp', 'chat_messages', ['timestamp'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_chat_messages_timestamp', table_name='chat_messages')
    op.drop_index('ix_chat_messages_session', table_name='chat_messages')
    op.drop_index('ix_chat_sessions_user', table_name='chat_sessions')
    op.drop_index('ix_book_content_type', table_name='book_content')
    op.drop_index('ix_book_content_slug', table_name='book_content')
    op.drop_index('ix_users_email', table_name='users')

    # Drop tables in reverse order
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('book_content')
    op.drop_table('personalization_preferences')
    
    # Drop check constraints before dropping user_profiles table
    op.drop_constraint('ck_examples_preference', 'personalization_preferences', type_='check')
    op.drop_constraint('ck_content_level', 'personalization_preferences', type_='check')
    
    op.drop_table('user_profiles')
    op.drop_constraint('ck_technical_background', 'user_profiles', type_='check')
    op.drop_constraint('ck_hardware_specs', 'user_profiles', type_='check')
    
    op.drop_table('users')