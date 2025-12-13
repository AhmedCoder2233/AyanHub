# Research for 004-backend-chatkit-integrate

## Architectural Decisions and Clarifications

### 1. Endpoint Pattern for Chat Functionality

-   **Decision**: Adhere to `POST /api/{user_id}/chat` as per the constitution.
-   **Rationale**: This maintains consistency with the project's established API design principles, ensuring a unified and predictable API surface. Including the `user_id` in the path provides a clear hierarchical structure for user-specific resources.
-   **Alternatives Considered**: Using a top-level `POST /chat` endpoint with `user_id` in the request body was considered for potentially simpler client-side invocation. However, this deviates from the constitutional guideline and could lead to inconsistencies across the API.

### 2. AI Framework for Integration

-   **Decision**: Switch to `OpenAI Agents SDK` for AI integration.
-   **Rationale**: This decision prioritizes alignment with the project's constitution, which explicitly mandates `OpenAI Agents SDK`. Adhering to a single, defined AI framework simplifies maintenance, leverages existing tooling, and potentially consolidates expertise within the team.
-   **Alternatives Considered**: Proceeding with `google-generativeai` (Gemini) was an option, as it was initially implied by the feature description. However, this would have introduced a deviation from the constitution's stated AI framework, potentially leading to a fragmented technology stack and increased complexity in the long run.

### 3. Performance Goals for AI Interactions

-   **Decision**: Target `< 2 seconds p95 latency for AI response`.
-   **Rationale**: A response time under 2 seconds is generally considered good for interactive chat applications, providing a smooth and responsive user experience without noticeable delays. P95 latency ensures that most users (95%) will experience this performance.
-   **Alternatives Considered**: Faster response times (e.g., <1 second) could be targeted but might require more aggressive optimization or higher computational resources, which might not be necessary for the initial phase. Slower response times (e.g., >3 seconds) could degrade the user experience.

### 4. Constraints for Backend Service

-   **Decision**: Target `< 256MB memory usage per instance`.
-   **Rationale**: Setting a memory usage constraint is important for efficient resource utilization, especially in cloud environments where memory consumption directly impacts hosting costs and scalability. 256MB per instance is a common and reasonable starting point for a Python FastAPI service.
-   **Alternatives Considered**: Higher memory limits would increase costs, while lower limits might constrain the service's ability to handle requests efficiently.

### 5. Scale/Scope for Chat Functionality

-   **Decision**: Target `1,000 concurrent users` and `10,000 daily message volume`.
-   **Rationale**: This scale provides a solid foundation for initial deployment and testing, allowing for a significant user base while remaining manageable for a new feature. It represents a typical entry-level to mid-range usage for a web application.
-   **Alternatives Considered**: Higher scales (e.g., 10k+ concurrent users) would require more robust infrastructure and potentially more complex architectural considerations, which might be premature for the initial phase. Lower scales might not provide sufficient real-world testing.
