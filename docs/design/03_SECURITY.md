# Security & Access Document

> **Alignment Note:** This document specifically addresses the Hack2Skill Evaluation Focus Area: *"Security – safe and responsible implementation."* The architecture is strictly designed to protect API keys in a mandatory Public Repository setting.

## 1. Authentication Strategy
The MVP is a public-facing utility application with no user authentication required. Anyone with the URL can generate a cooking plan.

## 2. Role-Based Access Control (RBAC)
Not applicable for the MVP as there are no admin/user distinctions. 

## 3. Secret Management (Hack2Skill Compliance)
**CRITICAL:** Under no circumstances are API keys to be hardcoded into the repository. Because the rules require a *Public Repository*, leaking keys is an automatic failure.
- **Local Development:** Secrets are managed safely via a local, git-ignored `.env` file using the `python-dotenv` library. The key is retrieved securely via `os.getenv("GEMINI_API_KEY")`.
- **Production (Hugging Face):** Secrets are injected dynamically via the Hugging Face Spaces UI ("Settings > Variables and secrets"). They are never pushed in plaintext.
- **Fail-Safe Mechanism:** If the API key is missing from the environment, the application triggers a safe shutdown (`st.stop()`) and displays an explicit UI error message rather than crashing or exposing a stack trace.

## 4. Data Privacy & Compliance
- The application does not collect, store, or transmit any Personally Identifiable Information (PII). 
- All user inputs (schedule, budget, diet) are ephemeral and wiped securely when the session closes.
- No telemetry or tracking scripts are embedded.

## 5. Network Security
- Application runs on Streamlit's default port (8501) locally.
- In production, it inherits Hugging Face Spaces' SSL/TLS encryption and WAF protections.
