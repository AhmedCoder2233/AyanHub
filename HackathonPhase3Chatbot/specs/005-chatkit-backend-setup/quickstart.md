# Quickstart Guide: ChatKit Backend Setup

This guide provides a concise overview of the steps required to set up and run the ChatKit backend locally.

## Prerequisites

-   Python 3.8+
-   `git` installed
-   Active internet connection
-   Valid OpenAI API Key
-   Valid Gemini API Key

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/openai/openai-chatkit-advanced-samples.git
    cd openai-chatkit-advanced-samples/examples/customer-support/backend
    ```

2.  **Delete Unnecessary Files:**
    ```bash
    rm meal_preferences.py title_agent.py
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend` directory with your API keys:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

5.  **Run the Backend Server:**
    ```bash
    python main.py
    ```
    The server should start on `http://localhost:8000`.

## Verification

Open your browser and navigate to `http://localhost:8000/docs`. You should see the FastAPI Swagger documentation, confirming the backend is running and its API is accessible.
