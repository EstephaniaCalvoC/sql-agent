import uuid
import requests

from client.common import logger


class SQLAgentClient:
    def __init__(self, base_url: str="http://localhost:8000") -> None:
        logger.info("Start Client")
        self.base_url = base_url

    def query(self, question: str) -> str:
        thread_id = str(uuid.uuid4())
        logger.info(f"Ask question: {question} with thread_id: {thread_id}")
        response = requests.post(f"{self.base_url}/query", json={"question": question, "thread_id": thread_id})
        raw_response = response.json()
        
        if response.status_code != 200:
            logger.error(f"Error from server: {raw_response}")
            raise Exception(f"Ups, something went wrong: {raw_response}")
        
        return {"answer": raw_response.get('answer'), "error_message": raw_response.get('error_message')}
