import os
import py_compile

from streamlit.testing.v1 import AppTest

# Set dummy key so app.py doesn't sys.exit on import during standard pytest collection
os.environ["GEMINI_API_KEY"] = "dummy_for_testing"

# Import schemas directly from the single-file app
from app import BudgetFeasibility, CookingToDoList


def test_app_compiles():
    """Test Case 1: Ensure application compiles syntactically without errors."""
    py_compile.compile("app.py", doraise=True)
    assert True


def test_pydantic_schemas():
    """Test Case 2: Ensure Pydantic schema parses valid JSON successfully."""
    valid_json = """
    {
      "meals": {
        "breakfast": {
          "name": "Oatmeal",
          "prep_time": "10 mins",
          "instructions": "Boil oats."
        },
        "lunch": {
          "name": "Salad",
          "prep_time": "5 mins",
          "instructions": "Mix greens."
        },
        "dinner": {
          "name": "Pasta",
          "prep_time": "20 mins",
          "instructions": "Boil pasta."
        }
      },
      "grocery_list": ["Oats", "Greens", "Pasta"],
      "substitutions": [
        {
          "original_item": "Truffle Oil",
          "substitute": "Olive Oil",
          "reason": "Cheaper"
        }
      ],
      "budget_feasibility": {
        "estimated_cost": 15.50,
        "is_feasible": true,
        "reasoning": "Under $20 budget."
      }
    }
    """
    # Should not raise a ValidationError
    parsed_plan = CookingToDoList.model_validate_json(valid_json)
    assert parsed_plan.budget_feasibility.is_feasible is True
    assert len(parsed_plan.grocery_list) == 3


def test_budget_feasibility_logic():
    """Test Case 3: Validate negative budget feasibility parsing."""
    invalid_budget_json = """
    {
      "estimated_cost": 50.00,
      "is_feasible": false,
      "reasoning": "Exceeds $20 budget."
    }
    """
    feasibility = BudgetFeasibility.model_validate_json(invalid_budget_json)
    assert feasibility.is_feasible is False
    assert feasibility.estimated_cost == 50.00


def test_ui_sidebar_inputs():
    """Test Case 4: AppTest to verify Streamlit sidebar widgets load correctly."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    # Check default budget value (index 0 of number_input)
    assert at.number_input[0].value == 20.0
    # Check button exists
    assert at.button[0].label == "Generate My Day"


def test_missing_api_key_fails_safely(monkeypatch):
    """Test Case 5: Ensure application fails safely with st.error if no API key is present."""
    # Temporarily remove key and prevent dotenv from reloading it
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    import dotenv

    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)

    at = AppTest.from_file("app.py").run()

    # It shouldn't crash with an unhandled exception (stack trace)
    # It should stop gracefully via st.stop() and render an error
    assert not at.exception
    assert len(at.error) > 0
    assert "Gemini API Key is missing" in at.error[0].value
