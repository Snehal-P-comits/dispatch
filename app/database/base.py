# This file defines the base class for SQLAlchemy models using the Declarative system.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

'''
SQLAlchemy models need a common parent class to function properly and to allow SQLAlchemy to manage the database schema and interactions.
The Base class defined here serves as that common parent class for all models in the application.
By inheriting from this Base class, each model
This file defines that base class using SQLAlchemy's Declarative system.
All models in the application will inherit from this Base class,
allowing them to be recognized as SQLAlchemy models and enabling features like table creation and querying.

That Base comes from this file.

This allows SQLAlchemy to:
    track tables,
    generate schemas,
    create relationships,
    create DB metadata.

'''