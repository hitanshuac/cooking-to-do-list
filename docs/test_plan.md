# Universal Test Plan

**Target Framework:** Pytest
**Application:** Micro AI Cooking Planner

## Context
Based on `05_TICKETS.md`, the MVP is marked as completed, but we need to ensure the existing features are covered by robust tests. Future tickets (Recipe Links, PDF Export) will be tested once implemented.

## Test Cases

### 1. test_app_compiles (Unit)
- **Setup:** None
- **Action:** Run `py_compile.compile('app.py')`
- **Assertion:** The application file contains valid Python syntax and compiles without exception.

### 2. test_pydantic_schemas (Unit)
- **Setup:** Create a mock dictionary representing a valid AI JSON response.
- **Action:** Instantiate the `CookingToDoList` model with `model_validate_json()` or `model_validate()`.
- **Assertion:** The model parses correctly without validation errors.

### 3. test_budget_feasibility_logic (Unit)
- **Setup:** Mock an expensive meal plan and a low user budget.
- **Action:** Validate `BudgetFeasibility.is_feasible`.
- **Assertion:** Ensure the schema correctly represents a `False` boolean for feasibility when cost > budget.

### 4. test_ui_sidebar_inputs (Integration / Streamlit)
- **Setup:** Use `streamlit.testing` (Streamlit 1.28+) AppTest framework.
- **Action:** Initialize `AppTest.from_file("app.py").run()`.
- **Assertion:** Verify sidebar widgets (Daily Schedule, Budget, Dietary Needs) load successfully and default to expected values.

### 5. test_missing_api_key_fails_safely (Integration)
- **Setup:** Temporarily remove `GEMINI_API_KEY` from environment variables.
- **Action:** Run the Streamlit AppTest framework.
- **Assertion:** Verify `st.error` renders the missing API key message and the app stops (`st.stop()`).
