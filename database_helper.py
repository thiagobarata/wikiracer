import sqlite3

# Helper functions to interact with sqlite db

# Link snippet will be Denis_Matiola if the page is Denis Matiola because that's how wikipedia represents titles

def titleToID(link_snippet, curs):

    command_string = """ SELECT `page_id` 
    FROM `pages`
    WHERE `page_title` = ?
    
    """

    curs.execute(command_string, (link_snippet,))
    result = curs.fetchone()

    return result[0] if result else None # If nothing is found return none

def IDToTitle(id, curs):

    command_string = """ SELECT `page_title` 
    FROM `pages`
    WHERE `page_id` = ?
    
    """

    curs.execute(command_string, (id,))
    result = curs.fetchone()

    return result[0] if result else None # If nothing is found return none

def getAllLinksInPage(id, curs):
    
    command_string = """ SELECT `pl_to` 
    FROM `pagelinks`
    WHERE `pl_from` = ?
    
    """

    curs.execute(command_string, (id,))
    result = curs.fetchall()

    return result






