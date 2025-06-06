import os
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

load_dotenv()

def create_azure_sql_agent():
    
    connection_string = (
            f"mssql+pyodbc://{os.getenv('AZURE_SQL_USERNAME')}:{os.getenv('AZURE_SQL_PASSWORD')}@"
            f"{os.getenv('AZURE_SQL_SERVER')}/{os.getenv('AZURE_SQL_DATABASE')}?"
            "driver=ODBC+Driver+18+for+SQL+Server&"
            "TrustServerCertificate=yes&"
            "Connection Timeout=60&"
            "Encrypt=yes&"
            "MultipleActiveResultSets=true&"
            "ApplicationIntent=ReadWrite"
        )

    # Create SQLDatabase object
    db = SQLDatabase.from_uri(connection_string)

    # Create the LLM (ChatGPT model)
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0
    )

    # Build the SQL Agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        prefix="""You are an agent designed to interact with a SQL Server database.
        Given an input question, create a syntactically correct SQL query to run.
        Unless the user specifies a particular number of results to return,
        limit your query to 10 results. Order the results in descending order.
        
        IMPORTANT: 
        1. First, create and execute the SQL query to get the data
        2. Then, format the results in a natural, easy-to-read way
        3. Use square brackets [ ] for table and column names in your SQL
        4. Example of good response format:
           "Here are the results:
           - Downtown branch has 5 accounts
           - Uptown branch has 3 accounts
           - Midtown branch has 2 accounts"
        5. DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        6. DO NOT show the SQL query in your response
        7. Make the response conversational and easy to understand
        
        Before generating a query:
        1. First check what tables are available using sql_db_list_tables
        2. Check which columns are available in each table and then make a decision on what to do
        3. Then check the schema of relevant tables using sql_db_schema
        4. Use the correct table and column names in your query
        5. Format the results in a natural, readable way

        Tables:
        -BankAccounts (used for bank account data)
        -members (use this for any questions regarding members and profit)
        
        Remember: Return the results in natural language, making it easy for users to understand the data.
""",
    )

    return agent

if __name__ == "__main__":
    agent = create_azure_sql_agent()
    while True:
        user_input = input("\nAsk a question about your database (or 'quit'): ")
        if user_input.lower() == "quit":
            break
        try:
            response = agent.run(user_input)
            print("\nAnswer:\n", response)
        except Exception as e:
            print("Error:", str(e))
