from fastapi.testclient import TestClient

from app.service import app

client = TestClient(app)

def test_valid_question():
    with client as c:
        response = c.post("/query", json={"question": "How many album have led zeppelin?", "thread_id": "2"})
        print(f"### Response: {response.content}")
        assert response.status_code == 200
        
        print(f"### Response: {response.json()}")
        answer = response.json().get("answer", "")
        print(f"### Answer: {answer}")
        
        assert "14" in answer or "fourteen" in answer
        
        
def test_invalid_question():
    with client as c:
        response = c.post("/query", json={"question": "What is the capital of France?", "thread_id": "2"})
        print(f"### Response: {response.content}")
        assert response.status_code == 200
        
        print(f"### Response: {response.json()}")
        error_message = response.json().get("error_message")
        print(f"### Error Message: {error_message}")
        
        assert error_message
        