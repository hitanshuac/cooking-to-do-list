import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field

# B. Security & API Setup
# Load env variables locally
load_dotenv()

# Setup Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")


# A. Pydantic Schemas
class Meal(BaseModel):
    name: str = Field(..., description="Name of the meal")
    prep_time: str = Field(..., description="Estimated preparation and cooking time")
    instructions: str = Field(..., description="Short cooking instructions or recipe link")


class MealPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal


class Substitution(BaseModel):
    original_item: str = Field(..., description="The expensive or rare original item")
    substitute: str = Field(..., description="The cheaper or more common substitute")
    reason: str = Field(..., description="Reason for the substitution")


class BudgetFeasibility(BaseModel):
    estimated_cost: float = Field(..., description="Estimated total cost of the groceries")
    is_feasible: bool = Field(..., description="Whether the plan is within the provided budget")
    reasoning: str = Field(..., description="Reasoning behind the budget feasibility")


class CookingToDoList(BaseModel):
    meals: MealPlan
    grocery_list: list[str] = Field(..., description="Comprehensive list of ingredients needed")
    substitutions: list[Substitution] = Field(..., description="Suggested substitutions for expensive or rare items")
    budget_feasibility: BudgetFeasibility


# App Config
st.set_page_config(page_title="Micro AI Cooking Planner", page_icon="🍳", layout="wide")

if not api_key:
    st.error("Gemini API Key is missing. Please set GEMINI_API_KEY in your environment variables or .env file.")
    st.stop()

# Initialize GenAI Client
client = genai.Client(api_key=api_key)

# C. UI - Input Section (Sidebar)
with st.sidebar:
    st.header("📅 Your Day's Details")
    schedule = st.text_area("Daily Schedule", placeholder="e.g. Work 9-5, gym at 6pm, 30 mins to cook dinner.")
    budget = st.number_input("Budget ($)", min_value=1.0, value=20.0, step=1.0)
    dietary_needs = st.text_input("Dietary Needs / Preferences", placeholder="e.g. Vegetarian, High Protein, No Dairy")

    generate_btn = st.button("Generate My Day", type="primary")

# Initialize Session State
if "plan" not in st.session_state:
    st.session_state.plan = None
if "checklist" not in st.session_state:
    st.session_state.checklist = []

# D. AI Logic (Middleware Replacement)
if generate_btn:
    if not schedule:
        st.warning("Please provide your daily schedule to generate a relevant plan.")
    else:
        with st.spinner("Planning your meals and generating grocery list..."):
            prompt = f"""
            Create a detailed cooking plan and grocery list based on the following:
            - Daily Schedule: {schedule}
            - Budget: ${budget}
            - Dietary Needs: {dietary_needs}
            
            Provide a realistic meal plan (Breakfast, Lunch, Dinner) matching the schedule and dietary needs.
            Include a comprehensive grocery list.
            Identify any potentially expensive or rare items in the grocery list and provide cheaper/common substitutions.
            Evaluate if the plan is feasible within the given budget.
            """

            max_retries = 3
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    # Use Gemini 2.5 Flash for high-speed deterministic JSON output
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=CookingToDoList,
                            system_instruction="You are a Senior Chef and Budget Meal Planner AI. You must output strict JSON.",
                        ),
                    )

                    # Parse JSON string using the Pydantic schema
                    result = CookingToDoList.model_validate_json(response.text)

                    # Store in session state to prevent re-triggering API
                    st.session_state.plan = result

                    # Initialize interactive grocery list
                    st.session_state.checklist = [{"item": item, "done": False} for item in result.grocery_list]

                    break  # Success, exit retry loop

                except APIError as e:
                    error_code = getattr(e, "code", 500)
                    if error_code == 429 or error_code >= 500:
                        if attempt < max_retries - 1:
                            st.toast(f"API high traffic (Error {error_code}). Retrying in {retry_delay}s...", icon="⚠️")
                            time.sleep(retry_delay)
                            retry_delay *= 2
                        else:
                            st.error(
                                f"Failed after {max_retries} attempts due to high traffic or rate limits. Please try again later."
                            )
                    else:
                        st.error(f"Google API Error: {e.message}")
                        break
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    break

# E. UI - Results Section (Main Page)
if st.session_state.plan:
    plan = st.session_state.plan

    st.title("🍽️ Your Daily Cooking Plan")

    # Budget Check
    if plan.budget_feasibility.is_feasible:
        st.success(
            f"**Budget Feasible!** Estimated Cost: **${plan.budget_feasibility.estimated_cost:.2f}**\n\n{plan.budget_feasibility.reasoning}"
        )
    else:
        st.warning(
            f"**Budget Warning!** Estimated Cost: **${plan.budget_feasibility.estimated_cost:.2f}**\n\n{plan.budget_feasibility.reasoning}"
        )

    st.divider()

    # Layout Main Plan and Grocery List
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🍱 Meal Plan")

        # Breakfast
        st.subheader("🌅 Breakfast")
        st.markdown(f"**{plan.meals.breakfast.name}** (Prep: {plan.meals.breakfast.prep_time})")
        st.write(plan.meals.breakfast.instructions)

        # Lunch
        st.subheader("☀️ Lunch")
        st.markdown(f"**{plan.meals.lunch.name}** (Prep: {plan.meals.lunch.prep_time})")
        st.write(plan.meals.lunch.instructions)

        # Dinner
        st.subheader("🌙 Dinner")
        st.markdown(f"**{plan.meals.dinner.name}** (Prep: {plan.meals.dinner.prep_time})")
        st.write(plan.meals.dinner.instructions)

        # Substitutions
        if plan.substitutions:
            st.write("")
            with st.expander("🔄 Substitutions for Expensive/Rare Items"):
                for sub in plan.substitutions:
                    st.markdown(f"- **{sub.original_item}** ➡️ **{sub.substitute}**\n  *Reason: {sub.reason}*")

    with col2:
        st.header("🛒 Grocery To-Do List")
        st.write("Check off items as you gather them:")

        # Interactive Grocery List
        for idx, entry in enumerate(st.session_state.checklist):
            # Apply markdown strikethrough if done
            label = f"~~{entry['item']}~~" if entry["done"] else entry["item"]

            is_checked = st.checkbox(label, value=entry["done"], key=f"check_{idx}")
            # Update state and rerun if changed
            if is_checked != entry["done"]:
                st.session_state.checklist[idx]["done"] = is_checked
                st.rerun()

else:
    st.info("👈 Enter your schedule and budget in the sidebar and click 'Generate My Day' to get started!")
