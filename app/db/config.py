#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            forename TEXT NOT NULL,
            surname    TEXT NOT NULL,
            username    TEXT NOT NULL,
            pwdHash    TEXT NOT NULL,
            isAdmin    BOOLEAN NOT NULL DEFAULT 0
        )
    """

    SEED_DATA = """INSERT INTO users (forename, surname, username, pwdHash, isAdmin)
VALUES ("Test", "User", "test", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252", 1)
"""

class MessageTable:

    NAME = "messages"

    SCHEMA = """
        CREATE TABLE messages (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            title    TEXT NOT NULL,
            body     TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """

    SEED_DATA = """INSERT INTO messages (user_id, title, body )
VALUES (1, "Test message", "This is a test message.")
    """
    
class ReplyTable:

    NAME = "replies"

    SCHEMA = """
        CREATE TABLE replies (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            body     TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES users(id)
            FOREIGN KEY(message_id) REFERENCES messages(id)
        )
    """

    SEED_DATA = """INSERT INTO replies (user_id, message_id , body )
VALUES (1, 1, "This is a test reply.")
    """



#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable, MessageTable, ReplyTable
    # Add more tables here...
]

