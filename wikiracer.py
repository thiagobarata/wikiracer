import http_parser
from collections import deque




# Creates graph where nodes are a webpage and an edge is a link from one webpage to another dynamically then finds shortest path

def reconstruct_path(nodesToPrev, start_link_snippet, target_link_snippet):
    if target_link_snippet not in nodesToPrev:
        return ("No Path Found", -1)

    path = []
    current = target_link_snippet
    counter = 0  # Number of clicks

    while current is not None:
        path.append(current)
        current = nodesToPrev[current]
        if current is not None:
            counter += 1

    path.reverse()
    path_str = " -> ".join(path)

    return (path_str, counter)


    

def find_shortest_path(start_link_snippet, target_link_snippet, max_layer):
    requests = 0
    graph = {} # using adjacency list representation: {link: [edge1,edge2,edge3], link2: [edge,edge,edge]}
    visited = set()
    nodesToPrev = {}
    nodesToLayer = {}
    queue = deque()

    #Putting first node in the queue
    queue.append(start_link_snippet)
    nodesToPrev[start_link_snippet] = None
    nodesToLayer[start_link_snippet] = 0
    visited.add(start_link_snippet)

    while queue:
        current = queue.popleft()
        if current == target_link_snippet:
            print("ENDED CODE, REQUESTS:" ,requests)
            return reconstruct_path(nodesToPrev, start_link_snippet, target_link_snippet)

        # ✅ Restore this part to get the edges
        edges = http_parser.get_links_to_other_pages(current)
        requests = requests+1
        if(requests%500 == 0):
            print("requests:",requests)
        graph[current] = edges

        for edge in edges:
            if edge == target_link_snippet:
                nodesToPrev[edge] = current  # Set parent before returning
                print("ENDED CODE, REQUESTS:" ,requests)
                return reconstruct_path(nodesToPrev, start_link_snippet, target_link_snippet)

            if edge not in visited:
                new_layer = nodesToLayer[current] + 1
                if new_layer <= max_layer:
                    visited.add(edge)
                    queue.append(edge)
                    nodesToPrev[edge] = current
                    nodesToLayer[edge] = new_layer

    return ("No Path Found", -1)

if __name__ =="__main__":
    shortest_path = find_shortest_path("Denis_Matiola","Goal_(sports)", 5)
    print(shortest_path)









    
    

