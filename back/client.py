import requests
import uuid

if __name__ == "__main__":
    thread_id = str(uuid.uuid4())
    url = "http://localhost:8000/query"

    response = requests.post(url,
                             json={"question": "How many albums does Led Zeppelin have?", 
                                   "thread_id": thread_id})

    print(response.json())  
    