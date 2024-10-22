from typing import Literal

from app.agent.states import OverallState
from app.agent.nodes import INVALID_QUESTION_ERROR


def check_question(state: OverallState) -> Literal["generate_query", "gen_answer"]:
  if state.get("error_message") == INVALID_QUESTION_ERROR:
    return "gen_answer"
  return "generate_query"


def router(state: OverallState) -> Literal["generate_query", "gen_answer"]:
  query = state["queries"][-1]

  return "gen_answer" if query.result else "generate_query"


routers = {
  "check_question": check_question,
  "router": router
}