import sqlite3
import re

def createPagesTable(db_path):
    #Connecting to the database
    with sqlite3.connect(db_path) as conn:

        # Creating cursor to execute commands
        curs = conn.cursor()


        commandString = """
        CREATE TABLE IF NOT EXISTS pages(
        page_id INTEGER PRIMARY KEY,
        page_title TEXT UNIQUE
        );

        """

        curs.execute(commandString)
        print("Created 'pages' table.")


def createPageLinksTable(db_path):
     #Connecting to the database
    with sqlite3.connect(db_path) as conn:

        # Creating cursor to execute commands
        curs = conn.cursor()


        commandString = """
        CREATE TABLE IF NOT EXISTS pagelinks(
        pl_from INTEGER,
        pl_to Integer,
        PRIMARY KEY (pl_from, pl_to)
        );

        """

        curs.execute(commandString)
        print("Created 'pagelinks' table.")

# This function used regular expressions to convert a tuple that looks like this (123,0,56) to (123,56)

def deleteNamespaceFromTuples(line):
    matches = re.findall(r'\((\d+),\d+,(\d+)\)', line)
    return matches

def parseAndExecuteAllInserts(db_path,dump_source_db):
    #Connecting to the database
    with sqlite3.connect(db_path) as conn:

        # Creating cursor to execute commands
        curs = conn.cursor()




