from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent.graph import get_sql_agent_graph
from app.common import logger
from app.agent.nodes import nodes
from app.agent.routers import routers


class QueryRequest(BaseModel):
    thread_id: str
    question: str
    max_attempts: int = 1
    

app = FastAPI()

sql_agent_graph = get_sql_agent_graph(nodes, routers)


@app.post("/query")
def query_sql_agent(request: QueryRequest):
    try:
        # TODO:Add thread_id as common attribute to all logs
        logger.info(f"Query request: {request}")
        result = sql_agent_graph.invoke({"question": request.question, "max_attempts": request.max_attempts},
                                        {"configurable": {"thread_id": request.thread_id}})
        
        return result
    
    except Exception as e:
        print(f"Error in query_sql_agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
