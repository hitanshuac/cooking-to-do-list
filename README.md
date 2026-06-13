# Micro AI Cooking Planner

An interactive, AI-driven micro-app designed to generate a highly personalized daily cooking to-do list.

## 🚀 Live Demo
You can access the live, deployed web application here:
**[https://huggingface.co/spaces/HitanshuAC/Micro-Cooking-Planner](https://huggingface.co/spaces/HitanshuAC/Micro-Cooking-Planner)**

## 🎯 Chosen Vertical
**Productivity & Lifestyle (AI Cooking Planner)**

This application targets the intersection of personal health, time management, and financial budgeting by generating a feasible, easy-to-follow daily meal plan based on the user's specific constraints.

## 🧠 Approach and Logic
The solution is built using a lightweight, deterministic architecture tailored for speed and strict output generation:
1. **Frontend / State Management**: Built entirely with `Streamlit`. It leverages `st.session_state` to maintain the reactive status of the generated grocery checklist without needing to recall the LLM on every UI interaction.
2. **AI Middleware**: Powered by the official `google-genai` SDK and the `gemini-2.5-flash` model for high-speed inference.
3. **Structured Outputs**: Instead of relying on raw text parsing, the app uses `Pydantic` schemas injected directly into the Gemini `response_schema`. This guarantees a 100% deterministic JSON structure containing the meals, grocery list, substitutions, and budget feasibility.

## ⚙️ How the Solution Works
1. **Input Phase**: The user provides their daily schedule, budget, and specific dietary needs via the sidebar.
2. **Generation Phase**: On clicking "Generate My Day", the app constructs a prompt and passes it to Gemini along with the strictly defined `CookingToDoList` schema.
3. **Validation & Budgeting Phase**: Gemini acts as a "Senior Chef & Budget Planner", calculating the estimated cost of groceries, validating it against the user's budget, and identifying rare/expensive items to suggest cheaper alternatives.
4. **Execution Phase**: The returned JSON is parsed directly into the UI. The user is presented with their meal plan, budget feasibility alert, substitution recommendations, and a fully interactive grocery to-do list (with strikethrough logic when items are checked off).

## 🛠️ Assumptions Made
- **Ephemeral Architecture**: To strictly adhere to the <10MB repository limit, no local or cloud SQL databases are used. Data is handled ephemerally via in-memory Session State.
- **API Availability**: It is assumed the deployment environment (e.g., Hugging Face Spaces) has a valid `GEMINI_API_KEY` injected via environment variables or Secrets.
- **Ingredient Availability**: The model assumes standard, regional availability of substitutions suggested.
