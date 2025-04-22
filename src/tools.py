from dataclasses import dataclass
import logging
from .postgres_connector import SQLAlchemyConnector
from .utils import generate_erd
from typing import List, Dict, Optional

@dataclass
class DBConfig:
    dbname: str
    user: str
    password: str
    host: str = "localhost"
    port: str = "5432"

class SQLTool:
    """
    Tool for interacting with a PostgreSQL database and generating ERDs.
    """
    def __init__(self, config: DBConfig, erd_file: str = "erd.md"):
        self.config = config
        self.db = SQLAlchemyConnector(
            dbname=config.dbname,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.erd_file = erd_file
        self._initialize()
    def _load_erd(self) -> Optional[str]:
        """
        Load ERD from a file if it exists.

        :return: ERD content or None if file doesn't exist
        """
        try:
            with open(self.erd_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.warning(f"ERD file {self.erd_file} not found.")
            return None

    def get_context(self) -> Optional[str]:
        """
        Provide general context about the database schema.

        :return: ERD or list of tables as context
        """
        # First try to return ERD
        if self.erd:
            return f"Database Entity-Relationship Diagram:\n{self.erd}"

        # Fallback to table names
        try:
            tables = self.fetch_table_names()
            return f"Available tables: {', '.join(tables)}"
        except Exception as e:
            self.logger.error(f"Error getting database context: {e}")
            return None


    def fetch_table_names(self) -> List[str]:
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              AND table_schema NOT IN ('pg_catalog', 'information_schema')
        """
        rows = self.db.fetch(query)
        return [row["table_name"] for row in rows]

    def fetch_table_details(self, table_names: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch column and constraint details for given tables.
        """
        query = f"""
            SELECT
                cols.table_name,
                cols.column_name,
                cols.data_type,
                cols.is_nullable,
                tc.constraint_type,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.columns AS cols
            LEFT JOIN information_schema.key_column_usage AS kcu
              ON cols.table_schema = kcu.table_schema
              AND cols.table_name = kcu.table_name
              AND cols.column_name = kcu.column_name
            LEFT JOIN information_schema.table_constraints AS tc
              ON kcu.constraint_schema = tc.constraint_schema
              AND kcu.constraint_name = tc.constraint_name
            LEFT JOIN information_schema.constraint_column_usage AS ccu
              ON tc.constraint_schema = ccu.constraint_schema
              AND tc.constraint_name = ccu.constraint_name
            WHERE cols.table_schema = 'public'
              AND cols.table_name = ANY(:tables)
            ORDER BY cols.table_name;
        """
        rows = self.db.fetch(query, params={"tables": table_names})
        details: Dict[str, List[Dict]] = {}
        for row in rows:
            details.setdefault(row["table_name"], []).append(row)
        return details

    def _initialize(self) -> None:
        """
        Fetch schema information and generate the ERD markdown file.
        """
        self.erd = self._load_erd()

        if self.erd:
            print("ERD Loaded")
        else:
            self.connect()
            table_names = self.fetch_table_names()
            self.logger.info(f"Found tables: {table_names}")
            details = self.fetch_table_details(table_names)
            generate_erd(details, output_file=self.erd_file)
            # Reload ERD after generation
            self.erd = self._load_erd()
