import sqlite3
import re

def createPagesTable(curs,conn):
        commandString = """
        CREATE TABLE IF NOT EXISTS pages(
        page_id INTEGER,
        page_title TEXT
        );

        """

        curs.execute(commandString)
        conn.commit()
        print("Created 'pages' table.")


def createPageLinksTable(curs,conn):
        commandString = """
        CREATE TABLE IF NOT EXISTS pagelinks(
        pl_from INTEGER,
        pl_to Integer
        );

        """

        curs.execute(commandString)
        conn.commit()
        print("Created 'pagelinks' table.")

# This function uses regular expressions to convert a tuple that looks like this (123,0,56) to (123,56) only if its a main page (page links version)

def pageLinksExtractIfMainPage(tupleStr):
    match = re.match(r'\((\d+),(\d+),(\d+)\)', tupleStr)
    if match and int(match.group(2)) == 0:
        return (match.group(1), match.group(3))
    return None

# This function uses regular expressions to convert a tuple that looks like this (123,0,title,...) to (123,title) only if its a main page (page version)

def pageExtractIfMainPage(tupleStr):
    # Match the first 3 fields: page_id, namespace, page_title
    match = re.match(r"\((\d+),(\d+),'([^']*)'", tupleStr)
    if match and int(match.group(2)) == 0:
        page_id = int(match.group(1))
        page_title = match.group(3)  # keep underscores
        return (page_id, page_title)
    return None

# This function takes an insert statement string and actually inserts into sqlite db (pagelink table)
def processPageLinkInsert(insert_stmt, curs):
    tracker = 0
    values_match = re.search(r'VALUES\s*(.+?);$', insert_stmt, re.IGNORECASE)
    if not values_match:
        return 0

    values_str = values_match.group(1)
    tuples = re.findall(r'\([^)]+\)', values_str)

    for t in tuples:
        result = pageLinksExtractIfMainPage(t)
        if result:
            try:
                curs.execute("INSERT OR IGNORE INTO pagelinks(pl_from, pl_to) VALUES (?, ?);", result)
                tracker += 1
            except sqlite3.Error as e:
                print(f"SQLite error: {e} with tuple {t}")

    return tracker


# This function takes an insert statement string and actually inserts into sqlite db (uses bunching) (pagelink table)
def processPageLinkInsertMany(insert_stmt, curs, batch_size=5000):
    tracker = 0
    values_match = re.search(r'VALUES\s*(.+?);$', insert_stmt, re.IGNORECASE)
    if not values_match:
        return 0

    values_str = values_match.group(1)
    tuples = re.findall(r'\([^)]+\)', values_str)

    batch = []
    for t in tuples:
        result = pageLinksExtractIfMainPage(t)
        if result:
            batch.append(result)
            if len(batch) >= batch_size:
                curs.executemany("INSERT OR IGNORE INTO pagelinks(pl_from, pl_to) VALUES (?, ?);", batch)
                tracker += len(batch)
                batch.clear()
    
    if batch:
        curs.executemany("INSERT OR IGNORE INTO pagelinks(pl_from, pl_to) VALUES (?, ?);", batch)
        tracker += len(batch)
    
    return tracker



# This function takes an insert statement string and actually inserts into sqlite db (page table)
def processPageInsert(insert_stmt, curs):
    tracker = 0
    values_match = re.search(r'VALUES\s*(.+?);$', insert_stmt, re.IGNORECASE)
    if not values_match:
        return 0

    values_str = values_match.group(1)
    tuples = re.findall(r'\([^)]+\)', values_str)

    for t in tuples:
        result = pageExtractIfMainPage(t)
        if result:
            try:
                curs.execute("INSERT OR IGNORE INTO pages(page_id, page_title) VALUES (?, ?);", result)
                tracker += 1
            except sqlite3.Error as e:
                print(f"SQLite error: {e} with tuple {t}")

    return tracker


# This function takes an insert statement string and actually inserts into sqlite db. Uses Batching (page table)
def processPageInsertMany(insert_stmt, curs, batch_size=5000):
    tracker = 0
    values_match = re.search(r'VALUES\s*(.+?);$', insert_stmt, re.IGNORECASE)
    if not values_match:
        return 0

    values_str = values_match.group(1)
    tuples = re.findall(r'\([^)]+\)', values_str)

    batch = []
    for t in tuples:
        result = pageExtractIfMainPage(t)
        if result:
            batch.append(result)
            if len(batch) >= batch_size:
                curs.executemany("INSERT OR IGNORE INTO pages(page_id, page_title) VALUES (?, ?);", batch)
                tracker += len(batch)
                batch.clear()
    
    if batch:
        curs.executemany("INSERT OR IGNORE INTO pages(page_id, page_title) VALUES (?, ?);", batch)
        tracker += len(batch)

    return tracker


# This function takes an insert statement string and actually inserts into sqlite db (page table)

# Main function for Parsing Pagelinks
def parseAndExecuteAllPageLinkInserts(dump_source_db, curs, conn):
    progressTracker = 0
    thresh = 1000000
    print("Starting pagelink inserts")

    with open(dump_source_db, 'r', encoding='utf-8') as f:
        insert_buffer = ""

        for line in f:
            line = line.strip()

            if not insert_buffer and line.startswith('INSERT INTO'):
                insert_buffer = line
                if line.endswith(';'):
                    progressTracker += processPageLinkInsert(insert_buffer, curs)
                    insert_buffer = ""
            elif insert_buffer:
                insert_buffer += ' ' + line
                if line.endswith(';'):
                    progressTracker += processPageLinkInsert(insert_buffer, curs)
                    insert_buffer = ""

            if progressTracker >= thresh:
                print("Inserted", progressTracker, "pagelinks.")
                thresh += 1000000
                conn.commit()


        print("Done inserting pagelinks.")
        print("Total pagelinks inserted:", progressTracker)


# Main function for parsing and inserting into the pages table
def parseAndExecuteAllPageInserts(dump_source_db, curs, conn):
    progressTracker = 0
    thresh = 1000000
    print("Starting page inserts")
    with open(dump_source_db, 'r', encoding='utf-8') as f:

        insert_buffer = ""
        for line in f:
            line = line.strip()

            if not insert_buffer and line.startswith('INSERT INTO'):
                insert_buffer = line
                if line.endswith(';'):
                    progressTracker+=processPageInsert(insert_buffer, curs)
                    insert_buffer = ""
            elif insert_buffer:
                insert_buffer += ' ' + line
                if line.endswith(';'):
                    progressTracker+=processPageInsert(insert_buffer, curs)
                    insert_buffer = ""
            
            if progressTracker >= thresh:
                print("inserted",progressTracker,"elements.")
                conn.commit()
                thresh+=1000000
            

        print("Done inserting pages.")
        print("Total pages inserted:", progressTracker)

