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
        
        IMPORTANT: 
        1. First, create and execute the SQL query to get the data
        2. Then, format the results in a natural, easy-to-read way
        3. Make sure you go through all of the rows in the table
        4. Use square brackets [ ] for table and column names in your SQL
        5. Format your response EXACTLY like this example (including the dashes and spacing):
           "Here are the results:
           - Downtown branch: 5 accounts
           - Uptown branch: 3 accounts
           - Midtown branch: 2 accounts"
        6. DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        7. DO NOT show the SQL query in your response
        8. DO NOT add any text before "Here are the results:"
        9. DO NOT add any text after the last result
        10. DO NOT add any line breaks between results
        11. DO NOT add any additional formatting or special characters
        12. Use a colon (:) to separate the branch name from its value
        13. The results must have commas between them
        14. For profit calculations, use SUM() to get total profits
        15. For counts, use COUNT() to get accurate numbers
        16. Order by greatest to least for counts and sums
        
        Before generating a query:
        1. First check what tables are available using sql_db_list_tables
        2. Check which columns are available in each table and then make a decision on what to do
        3. Then check the schema of relevant tables using sql_db_schema
        4. Use the correct table and column names in your query
        5. Format the results in a natural, readable way
        6. Verify the query results before formatting the response

        Tables:
        -BankAccounts (used for bank account data)
        -members (use this for any questions regarding members and profit)
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
