"""
Micro AI Cooking Planner.

A simple AI micro-app that helps a user generate a personal cooking to-do list based on their day.
It provides a structured meal planning flow that produces:
- Breakfast/Lunch/Dinner plan
- grocery list
- Substitutions
- budget feasibility logic

This module prioritizes Code Quality, Security, Efficiency, and Accessibility.
"""

import os
import re

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field

# Load env variables locally
load_dotenv()

# Setup Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# 1. Pydantic Schemas (Structured Outputs)
# ==========================================
class Meal(BaseModel):
    """Schema for a single meal."""

    name: str = Field(..., description="Name of the meal")
    prep_time: str = Field(..., description="Estimated preparation and cooking time")
    instructions: str = Field(..., description="Short cooking instructions or recipe link")


class MealPlan(BaseModel):
    """Schema representing Breakfast, Lunch, and Dinner."""

    breakfast: Meal
    lunch: Meal
    dinner: Meal


class Substitution(BaseModel):
    """Schema for ingredient substitutions."""

    original_item: str = Field(..., description="The expensive or rare original item")
    substitute: str = Field(..., description="The cheaper or more common substitute")
    reason: str = Field(..., description="Reason for the substitution")


class BudgetFeasibility(BaseModel):
    """Schema evaluating if the plan fits the budget."""

    estimated_cost: float = Field(..., description="Estimated total cost of the groceries")
    is_feasible: bool = Field(..., description="Whether the plan is within the provided budget")
    reasoning: str = Field(..., description="Reasoning behind the budget feasibility")


class CookingToDoList(BaseModel):
    """Core schema representing the final AI output."""

    meals: MealPlan
    grocery_list: list[str] = Field(..., description="Comprehensive list of ingredients needed")
    substitutions: list[Substitution] = Field(..., description="Suggested substitutions for expensive or rare items")
    budget_feasibility: BudgetFeasibility


# ==========================================
# 2. Security: Input Sanitization
# ==========================================
def sanitize_input(user_input: str) -> str:
    """
    Sanitizes user input to prevent prompt injection and XSS.

    Args:
        user_input: Raw string from the user.

    Returns:
        A sanitized string safe for LLM ingestion.
    """
    if not user_input:
        return ""
    # Strip HTML tags
    sanitized = re.sub(r"<[^>]*>", "", user_input)
    # Remove potentially malicious characters (basic sanitization)
    sanitized = re.sub(r"[{<>}]", "", sanitized)
    # Truncate length to prevent massive token injections
    return sanitized[:500].strip()


# ==========================================
# 3. Efficiency: Caching & API Logic
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def generate_meal_plan(schedule: str, budget: float, dietary_needs: str) -> dict:
    """
    Calls the Gemini API to generate the cooking to-do list.
    Cached for 1 hour to optimize resources and API limits.

    Args:
        schedule: The user's daily schedule.
        budget: The total grocery budget.
        dietary_needs: Specific dietary preferences.

    Returns:
        A dictionary representation of the CookingToDoList schema.
    """
    client = genai.Client(api_key=API_KEY)

    prompt = f"""
    Create a detailed cooking plan and grocery list based on the following:
    - Daily Schedule: {schedule}
    - Budget: ${budget:.2f}
    - Dietary Needs: {dietary_needs}
    
    Provide a realistic meal plan (Breakfast, Lunch, Dinner).
    Include a comprehensive grocery list.
    Identify any potentially expensive or rare items in the grocery list and provide cheaper/common substitutions.
    Evaluate if the plan is feasible within the given budget.
    """

    # We rely on Streamlit's native st.rerun or caching instead of a blocking time.sleep
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CookingToDoList,
                system_instruction="You are a Senior Chef and Budget Meal Planner AI. You must output strict JSON.",
            ),
        )
        return CookingToDoList.model_validate_json(response.text).model_dump()
    except APIError as e:
        error_code = getattr(e, "code", 500)
        raise RuntimeError(f"API Error ({error_code}): {getattr(e, 'message', str(e))}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to generate plan: {e}") from e


# ==========================================
# 4. Accessibility & UI
# ==========================================
def render_sidebar() -> tuple[str, float, str, bool]:
    """Renders the accessible sidebar inputs."""
    with st.sidebar:
        st.header("Your Day's Details")

        schedule_raw = st.text_area(
            "Daily Schedule",
            placeholder="e.g. Work 9-5, gym at 6pm, 30 mins to cook dinner.",
            help="Enter your daily schedule so we can plan meals around your free time.",
        )

        budget_raw = st.number_input(
            "Budget ($)", min_value=1.0, value=20.0, step=1.0, help="Enter your maximum grocery budget in dollars."
        )

        dietary_raw = st.text_input(
            "Dietary Needs / Preferences",
            placeholder="e.g. Vegetarian, High Protein",
            help="Enter any allergies or dietary preferences.",
        )

        generate_btn = st.button("Generate My Day", type="primary", help="Click to generate your meal plan.")

        return schedule_raw, float(budget_raw), dietary_raw, generate_btn


def render_results(plan_dict: dict) -> None:
    """Renders the meal plan and checklist."""
    plan = CookingToDoList.model_validate(plan_dict)

    st.title("Your Daily Cooking Plan")

    if plan.budget_feasibility.is_feasible:
        st.success(
            f"**Budget Feasible!** Estimated Cost: **${plan.budget_feasibility.estimated_cost:.2f}**\n\n"
            f"{plan.budget_feasibility.reasoning}"
        )
    else:
        st.warning(
            f"**Budget Warning!** Estimated Cost: **${plan.budget_feasibility.estimated_cost:.2f}**\n\n"
            f"{plan.budget_feasibility.reasoning}"
        )

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Meal Plan")

        st.subheader("Breakfast")
        st.markdown(f"**{plan.meals.breakfast.name}** (Prep: {plan.meals.breakfast.prep_time})")
        st.write(plan.meals.breakfast.instructions)

        st.subheader("Lunch")
        st.markdown(f"**{plan.meals.lunch.name}** (Prep: {plan.meals.lunch.prep_time})")
        st.write(plan.meals.lunch.instructions)

        st.subheader("Dinner")
        st.markdown(f"**{plan.meals.dinner.name}** (Prep: {plan.meals.dinner.prep_time})")
        st.write(plan.meals.dinner.instructions)

        if plan.substitutions:
            st.write("")
            with st.expander("Substitutions for Expensive/Rare Items"):
                for sub in plan.substitutions:
                    st.markdown(f"- **{sub.original_item}** -> **{sub.substitute}**\n  *Reason: {sub.reason}*")

    with col2:
        st.header("Grocery To-Do List")
        st.write("Check off items as you gather them:")

        # Interactive Grocery List
        for idx, entry in enumerate(st.session_state.checklist):
            label = f"~~{entry['item']}~~" if entry["done"] else entry["item"]

            is_checked = st.checkbox(
                label, value=entry["done"], key=f"check_{idx}", help=f"Mark {entry['item']} as collected"
            )

            if is_checked != entry["done"]:
                st.session_state.checklist[idx]["done"] = is_checked
                st.rerun()


def main() -> None:
    """Main application entrypoint."""
    st.set_page_config(page_title="Micro AI Cooking Planner", layout="wide")

    if not API_KEY:
        st.error("Gemini API Key is missing. Please set GEMINI_API_KEY in your environment variables.")
        st.stop()

    if "plan" not in st.session_state:
        st.session_state.plan = None
    if "checklist" not in st.session_state:
        st.session_state.checklist = []

    schedule_raw, budget, dietary_raw, generate_btn = render_sidebar()

    if generate_btn:
        schedule = sanitize_input(schedule_raw)
        dietary_needs = sanitize_input(dietary_raw)

        if not schedule:
            st.warning("Please provide your daily schedule to generate a relevant plan.")
        else:
            with st.spinner("Planning your meals and generating grocery list..."):
                try:
                    # Using the cached function
                    result_dict = generate_meal_plan(schedule, budget, dietary_needs)
                    st.session_state.plan = result_dict

                    # Refresh checklist items
                    st.session_state.checklist = [
                        {"item": item, "done": False} for item in result_dict.get("grocery_list", [])
                    ]
                except Exception as e:
                    st.error(str(e))

    if st.session_state.plan:
        render_results(st.session_state.plan)
    else:
        st.info("Enter your schedule and budget in the sidebar and click 'Generate My Day' to get started!")


if __name__ == "__main__":
    main()
