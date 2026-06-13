# Technical Architecture Document (TAD)

## 1. System Context
The Micro AI Cooking Planner is a standalone, single-node web application designed to be deployed ephemerally on Hugging Face Spaces. It interacts exclusively with the Google Gemini API to generate intelligence.

## 2. Component Architecture
- **Streamlit Frontend/Server:** Handles routing, rendering the UI, and managing the session state (interactive checkboxes).
- **AI Middleware (google-genai):** Acts as the intelligence layer, executing prompts and returning deterministic JSON data.
- **Schema Validator (Pydantic):** Ensures the AI's output is structurally sound and directly parsable into Python objects.

## 3. Data Flow / State Management
1. User enters data into Streamlit sidebar widgets.
2. App constructs a prompt and calls `client.models.generate_content` (Gemini 2.5 Flash).
3. The prompt explicitly requires the `CookingToDoList` Pydantic schema in the `response_schema` config.
4. Gemini returns the JSON string. Pydantic validates it via `model_validate_json`.
5. The parsed data is stored in `st.session_state.plan`.
6. The interactive grocery list is tracked in `st.session_state.checklist` to allow stateful UI updates without re-triggering the LLM.

## 4. Efficiency: Optimal Resource Usage
*Aligned with the Hack2Skill "Efficiency – optimal use of resources" Evaluation Parameter:*
- **Compute Efficiency:** By leveraging `gemini-2.5-flash` alongside strict `Pydantic` schema enforcement, we prevent the LLM from hallucinating conversational filler. The output is pure JSON, reducing token generation time and network latency.
- **Memory Efficiency:** No permanent database is used to keep the repository <10MB. State is managed ephemerally via Streamlit Session State.
```python
# Session State Structure (Zero-Disk Footprint)
st.session_state.plan: CookingToDoList
st.session_state.checklist: list[dict] # [{"item": str, "done": bool}]
```

## 5. Technology Stack
- **Frontend/Backend:** Streamlit (Python)
- **AI/LLM:** Google GenAI API (`gemini-2.5-flash`)
- **Data Validation:** Pydantic
- **Infrastructure:** Hugging Face Spaces (Streamlit SDK)
