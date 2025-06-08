# SQL Chatbot with LangChain and Azure SQL Database

## Query Your Database with Natural Language

This project is an interactive AI-powered SQL chatbot built using LangChain, an LLM, Azure SQL Database, and Streamlit. It allows users to query relational data in natural language and get accurate, structured responses

## Demo:
![azuresqlchatbotgif](https://github.com/user-attachments/assets/391e5b29-8e00-457a-80eb-61f4f124009f)


## Tools Used:
- Langchain
- Azure SQL Database
- Streamlit
- OpenAI

### Set Up

1. Clone the repository:
```bash
git clone https://github.com/Mzubac125/langchain_azure_sql_chatbot.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Input Credentials
You will need an OpenAI (or other LLM of choice) API key, and this information for your Azure Database Connection
- AZURE_SQL_SERVER
- AZURE_SQL_DATABASE
- AZURE_SQL_USERNAME
- AZURE_SQL_PASSWORD

4. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

