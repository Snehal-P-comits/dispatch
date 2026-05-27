# This file sets up the database connection and session management for the application using SQLAlchemy.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./dispatch.db"
#DATABASE_URL is the connection string that tells SQLAlchemy how to connect to the database.

#engine is SQLAlchemy’s connection bridge to the database.
# It manages the connection pool and provides a way to execute SQL statements.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    #SQLite normally restricts threads. FastAPI can use multiple threads.
    #This setting avoids thread restriction issues.
)

# A session is a temporary conversation with the database.
# You use sessions to interact with the db, such as querying data or committing changes.
# sessionmaker is an object that generates new Session objects when called.
#its done using sessionmaker function which is a factory for creating new Session objects.
SessionLocal = sessionmaker(
    autoflush=False, #Prevents automatic DB flushing before explicit commits.
    # flush is the process of synchronizing the in-memory state of the session with the database.
    autocommit=False,#You manually decide when DB changes are saved.
    # commit is the process of saving changes to the database permanently.
    bind=engine
    #binds the session to the engine, so it knows which database to connect to when you use the session.
)

# get_db is a generator function that provides a database session to the application.
# It creates a new session, yields it for use, and ensures that the session is closed after use,
# even if an error occurs.
def get_db():
    # Create a new database session
    db = SessionLocal()

    # Yield the session to the caller, allowing them to use it for database operations.
    try:
        #why yield instead of return? Because we want to ensure that the session is properly closed after use
        yield db

    #finally block is used to ensure that the session is closed after use, even if an error occurs.
    finally:
        db.close()