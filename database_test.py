import database_helper as db_helper
import sqlite3

with sqlite3.connect('all_wikipedia_pages.db') as conn:

    # Creating a cursor object so we can execute commads
    curs = conn.cursor()
    curs.execute("PRAGMA journal_mode = WAL;")


    """
    curs.execute("SELECT COUNT(*) FROM pages")
    print("pages:", curs.fetchone()[0])

    curs.execute("SELECT COUNT(*) FROM pagelinks")
    print("pagelinks:", curs.fetchone()[0])

    curs.execute("SELECT * FROM pages WHERE page_id = ?", (10,))
    result = curs.fetchone()
    print(result)

    


    curs.execute("SELECT * FROM pages LIMIT 5")
    print("Sample pages:", curs.fetchall())

    curs.execute("SELECT * FROM pagelinks LIMIT 5")
    print("Sample pagelinks:", curs.fetchall())

    """

    db_helper.titleToID("AccessibleComputing",curs)
    db_helper.IDToTitle(10,curs)
    #db_helper.getAllLinksInPage(10,curs)