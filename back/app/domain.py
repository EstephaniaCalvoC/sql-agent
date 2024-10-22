from pydantic import BaseModel, Field


class Query(BaseModel):
  statement: str = Field(description="SQL query statment")
  reasoning: str = Field(description="Reasoning behind the query defination")
  is_valid: bool = Field(True, description="Indicates if the statment is sintatically valid")
  result: str = Field("", description="Query result")
  error: str = Field("", description="Error message if exists")

  @property
  def info(self) -> str:
    return (f"SQL query:\n{self.statement}\n\n"
    f"The reasoning you used to create that query was:\n{self.reasoning}\n\n"
    f"And this is the result you get:\n{self.result}")

  @property
  def error_info(self) -> str:
    return(f"Wrong SQL query:\n{self.statement}\n\n"
    f"The reasoning you used to create that query was:\n{self.reasoning}\n\n"
    f"And this is the error you got when excuted it: {self.error}")
