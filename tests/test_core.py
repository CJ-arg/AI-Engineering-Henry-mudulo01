import pytest 
from src.run_query import run_legal_query

def test_run_legal_query_format():
    """Test to verify that the AI ​​responsehas the correct JSON format and legal fields."""
    test_question = "MIvecino me tira basura al patio todos los días"
    result = run_legal_query(test_question)
    
    assert "error" not in result, f"API error: {result.get('error')}"

    data = result.get("data")
    assert data is not None

    requiered_fields = ["answer", "branch", "specialist", "actions"]
    for field in requiered_fields:
        assert field in data, f"Missing required field: {field}"

    assert result["metrics"]["total_tokens"] > 0
    assert result["metrics"]["estimated_cost_usd"] >= 0

def test_cost_calculation_logic():
    """
    Simple test to verify that the cost calculation is not negative   
    """
    from src.run_query import calculate_cost
    cost = calculate_cost(100, 50)
    assert cost > 0
    assert isinstance(cost, float)    