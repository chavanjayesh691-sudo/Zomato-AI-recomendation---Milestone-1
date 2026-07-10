# Phase-wise Implementation Plan

## Project Goal
Build an AI-powered restaurant recommendation system that accepts user preferences, filters a real Zomato dataset, uses an LLM to rank and explain recommendations, and displays results in a user-friendly format.

This plan is derived from the requirements in [context.md](context.md) and the proposed architecture in [architecture.md](architecture.md).

---

## Phase 0 - Project Setup and Foundation

### Objectives
- Create the project structure for a clean, modular implementation.
- Set up the Python environment and required dependencies.
- Define the initial configuration for dataset access, budget tiers, and LLM settings.

### Tasks
- Create folders for data, services, models, UI, and tests.
- Add dependency files such as requirements.txt.
- Create environment configuration for:
  - Hugging Face dataset name
  - Groq API key
  - Groq model name
  - default ranking limits and budget thresholds
- Set up a basic app skeleton using Streamlit for the milestone demo.

### Deliverables
- Working project scaffold
- Configured environment template
- Basic app entry point

---

## Phase 1 - Data Ingestion and Preprocessing

### Objectives
- Load the Zomato dataset from Hugging Face.
- Clean and normalize restaurant data into a usable internal schema.
- Prepare the dataset for filtering and ranking.

### Tasks
- Load the dataset using the Hugging Face datasets library.
- Map raw fields such as restaurant name, city, cuisines, rating, and cost into standardized fields.
- Normalize values such as:
  - location names to lowercase aliases
  - cuisine names into consistent formats
  - rating values into numeric floats
  - cost values into a comparable numeric format
- Handle missing or malformed values gracefully.
- Build an in-memory or cached repository for quick access.

### Deliverables
- Data loader module
- Preprocessing pipeline
- Normalized restaurant dataset ready for filtering

---

## Phase 2 - Filtering and Candidate Preparation

### Objectives
- Apply deterministic filtering based on user preferences before involving the LLM.
- Create a compact candidate set that is relevant and cost-effective to send to the model.

### Tasks
- Implement a filter service that supports:
  - location filtering
  - cuisine filtering
  - minimum rating filtering
  - budget-tier filtering
  - optional free-text preference matching
- Rank the filtered results by relevance using a rule-based approach.
- Limit the number of candidates passed to the LLM to keep prompts efficient.
- Return metadata about the number of matches and applied filters.

### Deliverables
- Filter service
- Candidate ranking logic
- Structured filtered restaurant list

---

## Phase 3 - LLM Prompting and Recommendation Logic

### Objectives
- Use an LLM to rank and explain restaurant recommendations based on the filtered candidate list.
- Ensure recommendations are grounded in the provided dataset and not fabricated.

### Tasks
- Build a prompt template that includes:
  - user preferences
  - candidate restaurant details
  - task instructions for ranking and explanation
  - strict output structure for parsing
- Integrate the Groq API client.
- Parse the LLM response into a structured recommendation format.
- Validate that returned restaurant IDs belong to the filtered candidate set.
- Add fallback logic that uses rule-based ranking if the LLM call fails or returns invalid output.

### Deliverables
- Prompt builder module
- LLM integration layer
- Fallback ranking engine
- Structured recommendation output

---

## Phase 4 - Backend API and Orchestration Service

### Objectives
- Build a clean backend API / service layer to expose the recommendation pipeline cleanly to frontend applications.
- Orchestrate data ingestion, filtering, candidate ranking, and LLM reasoning into unified, high-performance API endpoints.
- Ensure type-safe, validated request/response contracts with structured error handling and rule-based fallback support.

### Tasks
- Create backend service endpoints / API layer (e.g., REST API / FastAPI or structured service controller) supporting:
  - Recommendation search endpoint accepting structured user preferences:
    - `location` (city/locality)
    - `budget_tier` ($ to $$$$)
    - `cuisines` (list or free-text)
    - `min_rating` (numeric threshold)
    - `dietary_preferences` or free-text search prompt
    - `top_k` limit
  - Metadata / filter options endpoint (available locations, cuisine list, price range distributions).
- Validate all incoming requests and outgoing recommendation payloads using Pydantic schemas.
- Orchestrate the end-to-end flow:
  1. Query dataset cache via Filter Service.
  2. Prepare top candidate set.
  3. Invoke Groq LLM Prompting service for ranking and explanations.
  4. Automatically fall back to rule-based ranking if Groq API is unavailable or returns malformed data.
- Implement structured error handling, logging, and health check/status endpoints.

### Deliverables
- Backend API & Service Orchestrator module
- Validated request & response Pydantic schemas (`RecommendationRequest`, `RecommendationResponse`, `RestaurantCard`)
- End-to-end backend recommendation workflow with fallback resilience

---

## Phase 5 - High-Quality Frontend Web Application

### Objectives
- Design and build a visually stunning, responsive, and intuitive web application that delivers a premium user experience.
- Implement modern, rich aesthetics (harmonious curated color palettes, elegant typography, glassmorphism cards, micro-animations) so users are impressed at first glance.
- Connect seamlessly to the Phase 4 Backend API to render interactive preference controls and AI-powered recommendations.

### Tasks
- **Design System & Aesthetics**:
  - Implement a polished, modern visual theme with curated colors (warm culinary/restaurant accents, sleek dark/light styling, and crisp typography).
  - Add smooth micro-animations, card hover states, and responsive layouts across desktop and mobile screen sizes.
- **Interactive Preference Controls**:
  - Build intuitive search and filter controls:
    - Location selector with quick suggestions
    - Interactive budget tier pills/badges (`$` / `$$` / `$$$` / `$$$$`)
    - Cuisine tag selector / chip input
    - Minimum rating interactive slider
    - Natural language preference box for custom dining desires (e.g., *"rooftop seating with romantic ambience"*)
- **Recommendation Showcase & AI Explanation Display**:
  - Design high-impact restaurant recommendation cards featuring:
    - Restaurant name, cuisine tags, location, and rating badge with stars
    - Cost estimate per two people
    - **AI Explanation Banner**: Dedicated, styled insight panel highlighting why the LLM recommended this restaurant based on user preferences
- **State Management & UX Polish**:
  - Add skeleton/shimmer loading animations while candidates are filtered and ranked by the LLM.
  - Implement informative empty-state screens and clear error notifications with actionable tips.

### Deliverables
- High-Quality Frontend Web Application
- Interactive Preference & Filter Panel
- Premium Restaurant Cards with AI Explanation highlights
- Polished UX with loading animations and error recovery

---

## Phase 6 - Testing, Validation, and Refinement

### Objectives
- Validate the backend API and frontend application end to end.
- Ensure correctness, robustness, and a smooth, impressive demo experience.

### Tasks
- Write unit and integration tests for data preprocessing, filtering, API endpoints, and fallback ranking.
- Test the full recommendation pipeline with diverse user inputs and edge cases.
- Validate that the LLM output matches the expected Pydantic schemas.
- Test resilience and failure scenarios:
  - no matching restaurants for restrictive filters
  - invalid LLM response or timeout
  - Groq API outage (verifying seamless UI fallback rendering)
- Refine prompts, ranking weights, and UI responsiveness based on end-to-end testing.

### Deliverables
- Comprehensive automated & manual test suite
- Verified end-to-end recommendation pipeline
- Highly polished, production-ready demo behavior

---

## Phase 7 - Documentation and Demo Readiness

### Objectives
- Prepare the project for presentation, demo showcase, and reviewer handoff.
- Provide clear setup instructions and architecture documentation.

### Tasks
- Write a comprehensive `README.md` with step-by-step setup, environment variable configuration, and execution instructions.
- Document the architecture, backend/frontend interaction, and LLM prompting strategy.
- Prepare curated sample inputs and expected outputs for demo scenarios.
- Capture polished screenshots or short walkthrough notes showcasing the high-quality frontend UI.

### Deliverables
- Project documentation and setup guide
- Demo-ready application package
- Final milestone handoff deliverables

---

## Suggested Execution Order
1. Set up the project structure and environment.
2. Implement data ingestion and preprocessing.
3. Build deterministic filtering and ranking logic.
4. Implement the Backend API and orchestration service with LLM & fallback integration.
5. Build the High-Quality Frontend Web Application with rich aesthetics and interactive controls.
6. Test, validate, and refine the end-to-end system.
7. Prepare final documentation and demo presentation.

---

## Definition of Done
The milestone is complete when:
- Users can enter restaurant preferences through a polished, high-quality frontend web application.
- The backend API cleanly orchestrates dataset filtering, candidate preparation, and LLM reasoning.
- Relevant restaurant candidates are accurately filtered and ranked.
- The web interface displays premium recommendation cards with restaurant name, cuisine, rating, cost, and AI-generated explanations.
- The system works reliably even if the LLM is unavailable by falling back to deterministic rule-based ranking.
