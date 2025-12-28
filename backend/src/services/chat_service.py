from typing import List, Optional
from uuid import UUID
from ..models.content_models import (
    ChatSessionCreate, ChatSessionUpdate, ChatSessionResponse,
    ChatMessageCreate, ChatMessageUpdate, ChatMessageResponse
)
from ..utils.logging import log_function_call
from datetime import datetime
from uuid import uuid4


class ChatService:
    """
    Service class to manage chat session and message operations
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, we'll use an in-memory store
        self.sessions = {}
        self.messages = {}
    
    @log_function_call
    async def create_session(self, session: ChatSessionCreate) -> ChatSessionResponse:
        """
        Creates a new chat session
        """
        session_id = uuid4()
        now = datetime.now()
        
        session_response = ChatSessionResponse(
            session_id=session_id,
            user_id=session.user_id,
            created_at=now,
            updated_at=now
        )
        
        self.sessions[session_id] = session_response
        return session_response
    
    @log_function_call
    async def get_session(self, session_id: UUID) -> Optional[ChatSessionResponse]:
        """
        Retrieves a chat session by its ID
        """
        return self.sessions.get(session_id)
    
    @log_function_call
    async def update_session(self, session_id: UUID, session_update: ChatSessionUpdate) -> Optional[ChatSessionResponse]:
        """
        Updates a chat session
        """
        if session_id not in self.sessions:
            return None
        
        existing_session = self.sessions[session_id]
        update_data = session_update.dict(exclude_unset=True)
        
        # Create updated session
        updated_session = existing_session.copy(update=update_data)
        updated_session.updated_at = datetime.now()
        
        self.sessions[session_id] = updated_session
        return updated_session
    
    @log_function_call
    async def create_message(self, message: ChatMessageCreate) -> ChatMessageResponse:
        """
        Creates a new chat message
        """
        message_id = uuid4()
        now = datetime.now()
        
        message_response = ChatMessageResponse(
            message_id=message_id,
            session_id=message.session_id,
            sender_type=message.sender_type,
            content=message.content,
            context_reference=message.context_reference,
            timestamp=now
        )
        
        # Verify session exists
        if message.session_id not in self.sessions:
            raise ValueError(f"Session with ID {message.session_id} does not exist")
        
        # Add message to the session
        if message.session_id not in self.messages:
            self.messages[message.session_id] = []
        self.messages[message.session_id].append(message_response)
        
        return message_response
    
    @log_function_call
    async def get_message(self, message_id: UUID) -> Optional[ChatMessageResponse]:
        """
        Retrieves a chat message by its ID
        """
        for message_list in self.messages.values():
            for message in message_list:
                if message.message_id == message_id:
                    return message
        return None
    
    @log_function_call
    async def get_session_messages(self, session_id: UUID) -> List[ChatMessageResponse]:
        """
        Retrieves all messages for a specific session
        """
        return self.messages.get(session_id, [])
    
    @log_function_call
    async def update_message(self, message_id: UUID, message_update: ChatMessageUpdate) -> Optional[ChatMessageResponse]:
        """
        Updates a chat message
        """
        for session_id, message_list in self.messages.items():
            for i, message in enumerate(message_list):
                if message.message_id == message_id:
                    update_data = message_update.dict(exclude_unset=True)
                    # Create updated message
                    updated_message = message.copy(update=update_data)
                    self.messages[session_id][i] = updated_message
                    return updated_message
        return None