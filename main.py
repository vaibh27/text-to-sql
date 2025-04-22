from src.agent import Agent
from src.tools import SQLTool, DBConfig

def main():
    # Initialize the database configuration
    db_config = DBConfig(
        dbname="dvdrental",
        user="postgres",
        password="postgres"
    )

    # Create the SQL tool
    sql_tool = SQLTool(config=db_config)
    memory = []

    # Create an agent with the tool
    agent = Agent(
        name="DatabaseAnalyst",
        description="Helps analyze database schema and data",
        prompt="You are an expert database analyst... ** Always be helpful and polite and give response as per the context only, don't fill any irrelevant information.",
        memory=memory,
        tool=sql_tool
    )

    print("Database Analyst Agent is ready. Type 'exit' to quit.")

    while True:
        # Get user input
        user_query = input("\nEnter your query: ")

        # Check if user wants to exit
        if user_query.lower() == 'exit':
            print("Exiting Database Analyst Agent. Goodbye!")
            break

        # Run the agent with the user's query
        if user_query:
            response = agent.run(user_query)
            print("\nResponse:")
            print(response)

if __name__ == "__main__":
    main()
