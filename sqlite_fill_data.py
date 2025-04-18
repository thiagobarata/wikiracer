import sqlite3
import sqlite_fill_data_helper as db_helper
# Connecting to the database
with sqlite3.connect('all_wikipedia_pages.db') as conn:

    # Creating a cursor object so we can execute commads
    curs = conn.cursor()
    """
    curs.execute("CREATE INDEX IF NOT EXISTS idx_pages_page_id ON pages(page_id)")
    curs.execute("CREATE INDEX IF NOT EXISTS idx_pagelinks_pl_from ON pagelinks(pl_from)")
    curs.execute("CREATE INDEX IF NOT EXISTS idx_pagelinks_pl_to ON pagelinks(pl_to)")
    conn.commit()
    """
    # Enable Write-Ahead Logging
    #curs.execute("PRAGMA journal_mode = WAL;")

    #Creating custom tables
    #db_helper.createPagesTable(curs,conn)
    #db_helper.createPageLinksTable(curs,conn)

    #Inserting Pagelinks into their table
    #db_helper.parseAndExecuteAllPageInserts("dump_files/enwiki-20250320-page.sql",curs,conn)

    #Inserting Pages into their table
    #db_helper.parseAndExecuteAllPageLinkInserts("dump_files/enwiki-20250320-pagelinks.sql",curs,conn)






