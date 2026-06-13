# Frontend Specification Document

## 1. Design System & Theming
- **Framework:** Streamlit Native UI Components.
- **Color Palette:** Inherits Streamlit's default system theme. Automatically supports Light/Dark mode toggles to respect user OS preferences.
- **Typography:** Streamlit default sans-serif (Inter/Roboto) for high legibility.
- **Micro-Interactions:** 
  - Markdown strikethrough (~~item~~) applied dynamically when a grocery checklist item is toggled, giving clear visual feedback.
  - Spinner animation (`st.spinner`) during LLM inference to prevent UI freezing and user confusion.

## 2. Global State Management
State is managed exclusively via `st.session_state`. 
- Re-renders are triggered automatically by Streamlit when `st.checkbox` values change.
- The `plan` object is cached in state to ensure UI interactions do not cause redundant, expensive API calls.

## 3. Core Layouts & Routing
- Single Page Application (SPA).
- **Sidebar:** Used for Data Input (Schedule, Budget, Dietary Needs) and the Primary Action Button ("Generate My Day").
- **Main View:** Used for Data Presentation.
  - Top: Budget Feasibility Alerts using distinct semantic colors (`st.success` / `st.warning`).
  - Columns Layout: 
    - Left Column (Ratio 2): Meal Plan details and Substitutions Expander.
    - Right Column (Ratio 1): Interactive Grocery To-Do List.

## 4. API Contracts
- No traditional REST API is exposed to the frontend. Streamlit directly bridges the Python backend logic and the browser-based frontend via WebSockets.

## 5. Accessibility (a11y) & Inclusive Design
*Aligned with the Hack2Skill "Accessibility – inclusive and usable design" Evaluation Parameter:*
- **Semantic HTML:** Streamlit compiles Python widgets directly into semantic HTML5, ensuring screen readers can parse the application correctly.
- **High Contrast Context:** Alerts and warnings use high-contrast foreground/background colors (Success/Warning banners) to ensure visibility for visually impaired users.
- **Responsive Layouts:** The dual-column layout automatically collapses into a highly readable vertical single-column stack on mobile devices.
- **Simple Interactions:** Uses standard HTML checkboxes (`st.checkbox`) instead of custom Javascript implementations, guaranteeing compatibility with native accessibility tooling.
