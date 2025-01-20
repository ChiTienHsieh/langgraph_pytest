import pytest
import json
import os
from typing import List, Dict, Any
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain import hub

# Import the classes and functions from the notebook
from src.plan_and_execute import (
    Plan,
    Response,
    Act,
    planner_prompt,
    replanner_prompt,
    execute_step,
    plan_step,
    replan_step,
    should_end,
)

# Create fixtures directory if it doesn't exist
FIXTURES_DIR = Path("tests/fixtures")
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture
def sample_inputs() -> Dict[str, Any]:
    """Load sample inputs from JSON file."""
    input_path = FIXTURES_DIR / "sample_inputs.json"
    if not input_path.exists():
        # Create sample inputs if they don't exist
        sample_data = {
            "basic_query": {
                "input": "What is the capital of France?",
                "expected_plan_steps": ["Search for the capital of France", 
                                      "Return the answer"]
            },
            "complex_query": {
                "input": "Who won the 2024 Taiwan election and what are their main policies?",
                "expected_plan_steps": [
                    "Search for the winner of the 2024 Taiwan presidential election",
                    "Search for the main policies of the winning candidate",
                    "Combine the information and provide a comprehensive answer"
                ]
            }
        }
        input_path.write_text(json.dumps(sample_data, indent=2))
    
    return json.loads(input_path.read_text())

@pytest.fixture
def tools():
    """Create tools fixture."""
    return [TavilySearchResults(max_results=3)]

@pytest.fixture
def llm():
    """Create LLM fixture."""
    return ChatOpenAI(model="gpt-4o-mini-2024-07-18")

@pytest.fixture
def agent_executor(llm, tools):
    """Create agent executor fixture."""
    prompt = hub.pull("ih/ih-react-agent-executor")
    return create_react_agent(llm, tools, state_modifier=prompt)

def test_plan_step(llm, sample_inputs, caplog):
    """Test the planning step."""
    # Create initial state
    state = {
        "input": sample_inputs["basic_query"]["input"],
        "plan": [],
        "past_steps": [],
        "response": ""
    }
    
    # Run plan step
    result = pytest.mark.asyncio(plan_step(state))
    
    # Log the LLM output
    print("LLM Output (Plan):", result)
    
    # Assertions
    assert isinstance(result, dict)
    assert "plan" in result
    assert isinstance(result["plan"], list)
    assert len(result["plan"]) > 0
    assert all(isinstance(step, str) for step in result["plan"])

def test_execute_step(agent_executor, sample_inputs, caplog):
    """Test the execution step."""
    # Create initial state with a plan
    state = {
        "input": sample_inputs["basic_query"]["input"],
        "plan": ["Search for the capital of France"],
        "past_steps": [],
        "response": ""
    }
    
    # Run execute step
    result = pytest.mark.asyncio(execute_step(state))
    
    # Log the LLM output
    print("LLM Output (Execute):", result)
    
    # Assertions
    assert isinstance(result, dict)
    assert "past_steps" in result
    assert isinstance(result["past_steps"], list)
    assert len(result["past_steps"]) == 1
    assert isinstance(result["past_steps"][0], tuple)
    assert len(result["past_steps"][0]) == 2

def test_replan_step(llm, sample_inputs, caplog):
    """Test the replanning step."""
    # Create initial state with past steps
    state = {
        "input": sample_inputs["complex_query"]["input"],
        "plan": ["Search for the winner of the 2024 Taiwan presidential election"],
        "past_steps": [
            ("Search for the winner of the 2024 Taiwan presidential election", 
             "Lai Ching-te won the 2024 Taiwan presidential election")
        ],
        "response": ""
    }
    
    # Run replan step
    result = pytest.mark.asyncio(replan_step(state))
    
    # Log the LLM output
    print("LLM Output (Replan):", result)
    
    # Assertions
    assert isinstance(result, dict)
    assert ("plan" in result) != ("response" in result)  # XOR - either plan or response, not both
    if "plan" in result:
        assert isinstance(result["plan"], list)
        assert len(result["plan"]) > 0
        assert all(isinstance(step, str) for step in result["plan"])
    else:
        assert isinstance(result["response"], str)
        assert len(result["response"]) > 0

def test_should_end():
    """Test the should_end function."""
    # Test with response present
    state_with_response = {
        "input": "test",
        "plan": [],
        "past_steps": [],
        "response": "This is a response"
    }
    assert should_end(state_with_response) == "END"
    
    # Test with no response
    state_without_response = {
        "input": "test",
        "plan": [],
        "past_steps": [],
        "response": ""
    }
    assert should_end(state_without_response) == "agent"
