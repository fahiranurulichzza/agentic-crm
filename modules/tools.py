from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from crewai.tools import tool
import re


db = SQLDatabase.from_uri("sqlite:///data/superstore.db")


@tool("list_tables")
def list_tables() -> str:
    """Lists all tables in the SQLite database."""
    return ListSQLDatabaseTool(db=db).invoke("")


@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Returns the schema and sample rows for specified tables.

    Args:
        tables (str): A string containing table names, either comma-separated or a single table name.
               Must contain only alphanumeric characters, underscores, and commas.
               Example: "table1" or "table1,table2"

    Returns:
        str: The schema and sample rows for the specified tables.

    Raises:
        ValueError: If the input contains invalid characters or empty table names.
    """
    if not tables or not tables.strip():
        return "Error: Table names cannot be empty."

    # Validate table names format
    if not re.match(r'^[a-zA-Z0-9_,]+$', tables):
        return "Error: Invalid table name format. Use alphanumeric characters and underscores only."

    # Split and clean table names
    table_list = [t.strip() for t in tables.split(",") if t.strip()]
    if not table_list:
        return "Error: No valid table names provided."

    try:
        tool = InfoSQLDatabaseTool(db=db)
        result = tool.invoke(tables)
        return result if result else "No schema information found for the specified tables."
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"


@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """
    Executes a provided SQL query and returns the results.

    Args:
        sql_query {str}: A valid SQL query string. Must be a SELECT query for safety.
                   Example: "SELECT * FROM table1 WHERE column1 = 'value'"

    Returns:
        str: The results of the SQL query execution.

    Raises:
        ValueError: If the query is empty or contains potentially dangerous operations.
    """
    # Input validation
    if not sql_query or not sql_query.strip():
        return "Error: SQL query cannot be empty."

    # Basic SQL injection prevention
    unsafe_keywords = ['drop ', 'delete ',
                       'update ', 'insert ', 'alter ', 'truncate ']
    if any(keyword in sql_query.lower() for keyword in unsafe_keywords):
        return "Error: Only SELECT queries are allowed for safety."

    try:
        sql_query = sql_query.replace('\\"', '"')

        # Execute the query
        tool = QuerySQLDataBaseTool(db=db)
        result = tool.invoke(sql_query)
        return result if result else "Query executed successfully but returned no results."
    except Exception as e:
        return f"Error executing SQL query: {str(e)}"
