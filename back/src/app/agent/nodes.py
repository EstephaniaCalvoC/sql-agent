from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field

from app.domain import Query
from app.agent.states import OverallState, InputState, OutputState
from app.common import logger, db_conn, chat
from app.agent.instructions import *


MAX_ATTEMPTS_DEFAULT = 1
INVALID_QUESTION_ERROR = "The quesiton is not related to the database"
REACH_OUT_MAX_ATTEMPTS_ERROR = "The system reach out the attempts limits before get the information."


def select_relevant_schemas(state: InputState) -> OverallState:
  logger.info('### select_relevant_schemas ###')

  max_attempts = state.get("max_attempts", 0)
  state["max_attempts"] = max_attempts if max_attempts > 0 else MAX_ATTEMPTS_DEFAULT

  tables_names = db_conn.get_usable_table_names()
  question = state["question"]

  instructions = SystemMessage(content=SELECT_RELEVANT_TABLES_INSTRUCTION.format(tables_names=tables_names))
  prompt = [instructions] + [HumanMessage(content=question)]
  structured_chat = chat.with_structured_output(list)

  relevant_tables = structured_chat.invoke(prompt).get('iterable')
  logger.info(f"{relevant_tables = }")

  if not relevant_tables:
    return {"error_message": INVALID_QUESTION_ERROR}

  tables_info = db_conn.get_table_info(relevant_tables)

  return {"tables_info": tables_info, "attempts": 1, **state}


class GenQueryResponse(BaseModel):
  statement: str = Field(description="Query stament to be run later in the DB")
  reasoning: str = Field(description="Reasoning used to define the query")


def generate_query(state: OverallState) -> OverallState:
  logger.info("### generate_query ###")

  question = state["question"]
  tables_info = state["tables_info"]
  queries = state.get("queries")

  # Gen query
  instructions = (GENERATE_QUERY_INSTRUCTIONS.format(info=tables_info)
  if not queries
  else FIX_QUERY_INSTRUCTIONS.format(info=tables_info, error_info=queries[-1].error_info))

  generator_prompt = ([SystemMessage(content=instructions)] + [HumanMessage(content=question)])
  generator = chat.with_structured_output(GenQueryResponse)
  gen_response = generator.invoke(generator_prompt)

  # Check query
  checker_prompt = (
      [SystemMessage(content=QUERY_CHECK_INSTRUCTION)] +
      [AIMessage(content=f"SQLite query: {gen_response.statement}\nReasoning: {gen_response.reasoning}")]
      )
  checker = chat.with_structured_output(GenQueryResponse)
  checker_response = checker.invoke(checker_prompt)

  was_corrected = gen_response.statement != checker_response.statement

  final_reasoning = (gen_response.reasoning  +
                     "" if not was_corrected else f"First: {gen_response.reasoning}\nCorrection: {checker_response.reasoning}")

  query = Query(statement=checker_response.statement, reasoning=final_reasoning)
  logger.info(query.info)

  return {"queries": [query]}


def excute_query(state: OverallState) -> OverallState:
  logger.info("### excute_query ###")

  attempts = state["attempts"]
  max_attempts = state["max_attempts"]

  logger.info(f"Attempt {attempts} of {max_attempts}")

  query = state["queries"][-1]

  try:
    query.result = db_conn.run(query.statement)

  except Exception as e:
    query.error = str(e)
    query.is_valid= False

    logger.info(query.error_info)

    if attempts >= max_attempts:
      logger.info(f"Reach out max attempts")
      return {"error_message": REACH_OUT_MAX_ATTEMPTS_ERROR}

  return {"attempts": 1}


def gen_answer(state: OverallState) -> OutputState:
  logger.info("### gen_answer ###")

  if error_message := state.get("error_message"):
    return {"error_message": error_message}

  query = state["queries"][-1]

  generate_answer_instruction = GENERATE_ANSWER_INSTRUCTION.format(query_info= query.info)

  prompt = (
      [SystemMessage(content=generate_answer_instruction)] +
      [HumanMessage(content=state["question"])]
      )

  response = chat.invoke(prompt)

  return {"answer": response.content}


nodes = {
  "select_relevant_schemas": select_relevant_schemas,
  "generate_query": generate_query,
  "excute_query": excute_query,
  "gen_answer": gen_answer
}
