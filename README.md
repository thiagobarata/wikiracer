# wikiracer
This program finds the shortest distance (in number of links) from one wikipedia page to another

I chose this project because during high school, whenever I was bored in class, I would hit up a friend and ask them if they wanna play a wikirace
The objective was to start on a page and end up on a target page by clicking a series of links. Whoever arrived at target fastest won the race.

The objective in this program is not only to find the shortest distance, but also do so in just a few seconds. The challenge is that Wikipedia
has over 62 million pages, with each page having potentially hundreds of links. This means that if the shortest path from wikipedia page to another is 6, we would have to find the path in a graph of potentially 
trillions of edges.

Constructing such a graph and finding this shortest path efficiently is the challenge in this project. I hope you find it interesting.



