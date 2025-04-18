from collections import deque
import database_helper as db_helper
import sqlite3




# Creates graph where nodes are a webpage and an edge is a link from one webpage to another dynamically then finds shortest path

def reconstruct_path(nodesToPrev, start_id, target_id,curs):
    if target_id not in nodesToPrev:
        return ("No Path Found", -1)

    path_ids = []
    current = target_id
    counter = 0  # Number of clicks

    while current is not None:
        path_ids.append(current)
        current = nodesToPrev[current]
        if current is not None:
            counter += 1

    path_ids.reverse()
    path_titles = [db_helper.IDToTitle(pid,curs) for pid in path_ids]
    path_str = " -> ".join(path_titles)

    return (path_str, counter)




def find_shortest_path(start_link_snippet, target_link_snippet, max_layer, curs):
    visited = set()
    nodesToPrev = {}
    nodesToLayer = {}
    queue = deque()

    startNodeID = db_helper.titleToID(start_link_snippet,curs)
    endNodeID = db_helper.titleToID(target_link_snippet,curs)



    if startNodeID is None or endNodeID is None:
        return ("Start or target page not found", -1)

    queue.append(startNodeID)
    visited.add(startNodeID)
    nodesToPrev[startNodeID] = None
    nodesToLayer[startNodeID] = 0

    while queue:
        current = queue.popleft()
        edges = db_helper.getAllLinksInPage(current,curs)
        neighbors = [edge[0] for edge in edges]  # Unpack from tuples like (123,)

        for neighbor in neighbors:
            if neighbor not in visited:
                new_layer = nodesToLayer[current] + 1
                if new_layer <= max_layer:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    nodesToPrev[neighbor] = current
                    nodesToLayer[neighbor] = new_layer

                    if neighbor == endNodeID:
                        return reconstruct_path(nodesToPrev, startNodeID, endNodeID,curs)

    return ("No Path Found", -1)


if __name__ =="__main__":

    with sqlite3.connect('all_wikipedia_pages.db') as conn:
        curs = conn.cursor()

        shortest_path = find_shortest_path("Cake","Seed", 5,curs)
        print(shortest_path)









    
    

