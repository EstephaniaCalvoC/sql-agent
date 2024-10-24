import operator
from typing_extensions import TypedDict
from typing import Annotated, List

from app.domain import Query


class InputState(TypedDict):
  question: str
  max_attempts: int


class OutputState(TypedDict):
  answer: str
  error_message: str


class OverallState(TypedDict):
  question: str
  max_attempts: int
  attempts: Annotated[int, operator.add]
  answer: str
  error_message: str
  tables_info: str
  resoning: str
  queries: Annotated[List[Query], operator.add]
  