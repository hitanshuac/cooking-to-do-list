# Feature Ticket List

*Agents must execute these tickets sequentially. Do not move to a new ticket until the previous one is fully verified.*

## 🎟️ TICKET-001: Build MVP Application
- **Description:** Implement the core Streamlit application utilizing Gemini 2.5 Flash and Pydantic for structured cooking plans.
- **Status:** **[COMPLETED]**
- **Acceptance Criteria:**
  - [x] Streamlit UI renders correctly.
  - [x] Gemini API generates valid JSON.
  - [x] Interactive checklist works without re-triggering API.
- **Technical Constraints:** Must be strictly under 10MB. Zero hardcoded keys.

## 🎟️ TICKET-002: Code Quality, Testing & Validation
- **Description:** Fulfill the Hack2Skill "Testing – validation of functionality" requirement by validating code integrity and schema generation.
- **Status:** **[COMPLETED]**
- **Acceptance Criteria:**
  - [x] Application compiles cleanly via `python -m py_compile app.py` with zero syntax errors.
  - [x] Pydantic schemas correctly marshal output preventing runtime exceptions.
  - [x] Error handling is actively configured for missing API keys.
- **Technical Constraints:** Ensures zero application crashes during judges' evaluation.

## 🎟️ TICKET-003: Add Recipe Link Integration (Future)
- **Description:** Enhance the `instructions` field in the `Meal` schema to query a search engine or provide a direct web link to a relevant recipe.
- **Status:** [TODO]
- **Acceptance Criteria:**
  - [ ] Generated meals contain a clickable markdown URL.
  - [ ] Links are verified to be active (non-404).

## 🎟️ TICKET-004: Export to PDF (Future)
- **Description:** Allow the user to export their daily meal plan and grocery list as a formatted PDF document.
- **Status:** [TODO]
- **Acceptance Criteria:**
  - [ ] "Export to PDF" button added to UI.
  - [ ] Downloadable file respects the layout of the generated plan.
