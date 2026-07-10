# AI-Powered Restaurant Recommendation System

This project implements a restaurant recommendation workflow that combines structured restaurant data with LLM-based reasoning.

## Phase 0 Status
The initial scaffold is now in place, including:
- project structure
- dependency configuration
- environment variable template
- basic Streamlit entry point
- initial Pydantic models

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required values.
4. Run the app:
   ```bash
   streamlit run src/ui/app.py
   ```
