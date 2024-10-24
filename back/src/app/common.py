import logging
import requests
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI


load_dotenv(override=True)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('sql_agent.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logger.info("Start SQL Agent")

def get_db():
    url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
    response = requests.get(url)

    if response.status_code == 200:
        with open("Chinook.db", "wb") as file:
            file.write(response.content)
        logger.info("File downloaded and saved as Chinook.db")
    else:
        logger.error(f"Failed to download the file. Status code: {response.status_code}")
    
    
# TODO: Consider to use the custom_table_info parammeter to pass the tables info
# If the table schemas doesn't doesn't change frequently it could be stored as a chaché
# In other case it could be generated as part of the agent setup. This is important
# the model need to now better the tables contents before select the relevant tables.
# For example, the table Eployes has the colum role but the model will don't now wiht roles
# it need to use to make a filter.

get_db()
db_conn = SQLDatabase.from_uri("sqlite:///Chinook.db", lazy_table_reflection=True)
chat = ChatOpenAI(model="gpt-4o-mini", temperature=0)
