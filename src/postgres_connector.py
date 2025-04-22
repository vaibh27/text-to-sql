from typing import Any, Dict, List, Optional, Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging

class SQLAlchemyConnector:
    """
    A simple wrapper around SQLAlchemy engine and session management.
    """
    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
    ):
        self.connection_string = (
            f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.engine = create_engine(self.connection_string, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            self.logger.exception("Session rollback because of exception")
            raise
        finally:
            session.close()

    def fetch(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        as_tuples: bool = False,
    ) -> List:
        """
        Execute a SELECT query and return all results.
        """
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            if as_tuples:
                return [tuple(row) for row in result]
            return [dict(row._mapping) for row in result]

    def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Execute an INSERT/UPDATE/DELETE query.
        """
        with self.get_session() as session:
            session.execute(text(query), params or {})

    def close(self) -> None:
        """
        Dispose of the database engine and its connections.
        """
        self.engine.dispose()
        self.logger.info("Database connection closed")
