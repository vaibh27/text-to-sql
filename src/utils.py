from pathlib import Path
from .openai_utils import chat_with_model

def generate_erd(
    tables: dict,
    output_file: str = "erd.md"
) -> None:
    """
    Generate an Entity-Relationship Diagram (ERD) in Mermaid markdown format
    based on the provided tables description and write it to a file.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a database expert. You are given a description of database tables "
                "including columns, types, primary and foreign keys. "
                "Generate an Entity-Relationship Diagram in Mermaid markdown format."
            ),
        },
        {
            "role": "user",
            "content": f"Generate an ERD for the following schema:\n{tables}",
        },
    ]
    erd_md = chat_with_model(messages)
    path = Path(output_file)
    path.write_text(erd_md)
    print(f"ERD has been written to {path}")
