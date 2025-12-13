# Data Model for 004-backend-chatkit-integrate

## Entities

### User

-   **Description**: Represents a user interacting with the chat system.
-   **Attributes**:
    -   `id`: string (Unique identifier for the user, derived from the API path)

### Message

-   **Description**: Represents a single message within a conversation.
-   **Attributes**:
    -   `id`: (Assumed from constitution: integer, primary key)
    -   `conversation_id`: (Assumed from constitution: integer, foreign key)
    -   `user_id`: string (Foreign key to User entity)
    -   `role`: enum (user/assistant - indicates sender)
    -   `content`: string (The actual text of the message)
    -   `timestamp`: datetime (When the message was created/sent)

### Conversation

-   **Description**: Represents an ongoing chat session between a user and the AI.
-   **Attributes**:
    -   `id`: (Assumed from constitution: integer, primary key)
    -   `user_id`: string (Foreign key to User entity)
    -   `created_at`: timestamp
    -   `updated_at`: timestamp

## Relationships

-   A `User` can have multiple `Conversations`.
-   A `Conversation` belongs to one `User`.
-   A `Conversation` contains multiple `Messages`.
-   A `Message` belongs to one `Conversation` and one `User`.

## Validation Rules (derived from Functional Requirements and Constitution)

-   `Message.content` MUST NOT be empty.
-   `Message.role` MUST be either 'user' or 'assistant'.
-   `User.id` MUST be present in the API path for chat interactions.
