# Data Model: AI-Native Unified Book + RAG Chatbot Platform

## User Entity
- **user_id**: UUID (Primary Key)
- **email**: String (Unique, Required)
- **password_hash**: String (Required)
- **created_at**: DateTime (Required)
- **updated_at**: DateTime (Required)
- **is_active**: Boolean (Default: true)

**Validation**: Email format validation, password strength requirements
**Relationships**: One-to-One with UserProfile

## UserProfile Entity
- **profile_id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to User)
- **first_name**: String (Optional)
- **last_name**: String (Optional)
- **technical_background**: String (Optional, e.g., "beginner", "intermediate", "advanced")
- **hardware_specs**: String (Optional, e.g., "low-end", "mid-range", "high-end")
- **language_preference**: String (Optional, Default: "en")
- **created_at**: DateTime (Required)
- **updated_at**: DateTime (Required)

**Validation**: Technical background must be from predefined enum
**Relationships**: One-to-One with User, One-to-Many with PersonalizationPreferences

## PersonalizationPreferences Entity
- **pref_id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to User)
- **chapter_id**: String (Optional, reference to book content)
- **content_level**: String (Optional, e.g., "simplified", "detailed", "technical")
- **examples_preference**: String (Optional, e.g., "practical", "theoretical")
- **created_at**: DateTime (Required)
- **updated_at**: DateTime (Required)

**Validation**: Content level must be from predefined enum
**Relationships**: Many-to-One with User

## BookContent Entity
- **content_id**: UUID (Primary Key)
- **title**: String (Required)
- **slug**: String (Required, Unique)
- **content**: Text (Required)
- **content_type**: String (Required, e.g., "chapter", "section", "appendix")
- **parent_id**: UUID (Optional, Self-Reference)
- **order_index**: Integer (Required)
- **created_at**: DateTime (Required)
- **updated_at**: DateTime (Required)

**Validation**: Unique constraint on slug
**Relationships**: Self-referencing for hierarchy

## ChatSession Entity
- **session_id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to User, Optional for anonymous sessions)
- **created_at**: DateTime (Required)
- **updated_at**: DateTime (Required)

**Relationships**: One-to-Many with ChatMessages

## ChatMessage Entity
- **message_id**: UUID (Primary Key)
- **session_id**: UUID (Foreign Key to ChatSession)
- **sender_type**: String (Required, e.g., "user", "assistant")
- **content**: Text (Required)
- **context_reference**: String (Optional, reference to book content)
- **timestamp**: DateTime (Required)

**Relationships**: Many-to-One with ChatSession

## VectorEmbedding Entity (for Qdrant)
- **content_id**: String (Primary Key for Qdrant)
- **text_content**: String (Required)
- **embedding_vector**: Array<Float> (Required, dimension based on embedding model)
- **metadata**: JSON (Required, including book section, importance score, etc.)

**Validation**: Consistent embedding dimensions
**Relationships**: Corresponds to BookContent entities