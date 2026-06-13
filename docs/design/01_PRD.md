# Product Requirements Document (PRD)

**Project Name:** Micro AI Cooking Planner
**Date:** 2026-06-13
**Status:** Approved

## 1. Objective
To build a lightning-fast, highly accurate AI micro-app that takes a user's daily schedule, budget, and dietary restrictions, and produces a concrete, realistic cooking to-do list. This solves the problem of "decision fatigue" when planning daily meals on a strict budget and tight timeline.

## 2. Target Audience / Personas
- **Persona 1 (The Busy Professional):** Needs quick, feasible recipes that fit precisely into limited time slots between work and personal life. Values speed and interactive checklists.
- **Persona 2 (The Budget-Conscious Student):** Needs to maximize a small grocery budget. Highly values AI-driven substitutions for expensive or rare ingredients.

## 3. Core Features (MVP)
*Must-have features for the first release.*
1. **Interactive UI:** Input fields for Schedule, Budget, and Diet, combined with a reactive generated Grocery Checklist.
2. **Deterministic AI Outputs:** Reliable generation of Breakfast, Lunch, and Dinner plans using structured JSON schemas.
3. **Budget Feasibility Engine:** AI calculates estimated costs, flags budget warnings, and offers cheaper substitutions.

## 4. Competition Constraints (Strict Non-Goals)
*Explicitly listing constraints required by the Hack2Skill rules that we must strictly follow:*
- **10 MB Size Limit:** The repository size must be strictly less than 10 MB. Complex relational databases (SQL) and large assets are forbidden.
- **Public Repository:** The GitHub repository must be public.
- **Single Branch:** The repository should contain only one branch.
- **No External Authentication Systems:** To keep the footprint small, no heavy auth frameworks will be used.

## 5. Success Metrics (Aligned with Hack2Skill Evaluation)
*How we measure success, directly mapped to the Hack2Skill Evaluation Focus Areas:*
- **Code Quality:** Code must be highly typed (Pydantic), strictly modular, and heavily documented for readability and maintainability.
- **Security:** Zero hardcoded API keys. 100% ephemeral data state to prevent accidental leakage in a public repository.
- **Efficiency:** The app generates the complete plan rapidly by enforcing strict Gemini Structured JSON Outputs, minimizing token wastage and maximizing resource usage.
- **Testing:** Zero runtime exceptions. Pydantic guarantees valid Python objects, and the code compiles cleanly.
- **Accessibility:** Uses native Streamlit semantic HTML elements, ensuring inclusive, high-contrast, and usable design.
