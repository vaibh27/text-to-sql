from typing import Optional, List, Dict, Any
from .openai_utils import chat_with_model

class Agent:
    """
    A generic agent to interact with language models and optional tools.
    """
    def __init__(
        self,
        name: str,
        description: str,
        prompt: str,
        memory: List[Dict[str, str]] =[],
        tool: Optional[Any] = None,
        sys_prompt: Optional[str] = None,
        llm: str = "gpt-4o",
    ):
        """
        Initialize an Agent with optional tool support.

        :param name: Name of the agent
        :param description: Description of the agent's purpose
        :param prompt: Initial prompt for the agent
        :param memory: List of memory items to be used by the agent
        :param tool: Optional tool to be used by the agent (e.g., SQLTool, DatabaseTool)
        :param sys_prompt: Optional system-level prompt
        :param llm: Language model to use (default: gpt-4o)
        """
        self.name = name
        self.description = description
        self.prompt = prompt
        self.tool = tool
        self.sys_prompt = sys_prompt
        self.llm = llm
        self.memory = memory

    def run(self, user_query: str) -> str:
        """
        Send a query to the language model, optionally using a tool.

        :param user_query: User's query to the agent
        :return: Response from the language model
        """
        messages: List[Dict[str, str]] = []

        if self.sys_prompt:
            messages.append({"role": "system", "content": self.sys_prompt})

        if self.memory:
            messages.append({"role": "assistant", "content": "Prev Chat :- "+ str(self.memory)})

        # Use tool if available to enhance context or preprocess query
        if self.tool:
            # Attempt to use tool's method if it has a method for query processing
            try:
                # Check if tool has a method to provide context
                tool_context = self.tool.get_context()
                if tool_context:
                    messages.append({"role":"developer", "content": "TOOL Context :-" + tool_context})
            except AttributeError:
                # Fallback if tool doesn't have a get_context method
                pass

        # Add user query
        messages.append({"role": "user", "content": user_query})

        response =  chat_with_model(messages, model=self.llm)
        # Send messages to the language model
        self.memory.extend([{"role": "user", "content": user_query}, {"role": "assistant", "content": response}])
        return response
