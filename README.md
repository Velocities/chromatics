# Chromatics

## Mathematical Background/Basis
In a branch of Mathematics known as Combinatorics, graphs involve two main building blocks:
- Vertices
- Edges

Vertices are the points on a graph and we use edges to connect them.
The rules for constructing proper graphs are as follows:
1. All vertices have a color
2. Connected vertices must each have colors that are distinct from one another

Due to the general simplicity behind the ruleset for graphs, it can be relatively easy
to calculate the number of possible color combinations when given a number of colors.
However, this process can become tricky upon inclusion of vertices with multiple connections
and loops/cycles. Fortunately, there is an algorithm known as the Reduction algorithm that
allows us to streamline this procedure. Here is how it works:
1. Pick an edge on the given graph
2. Make two new graphs that are a copy of the given graph
- One of the graphs will have the picked edge removed
- The other graph will have both vertices on the ends of the edge "merged", where they
are pushed towards one another (until the edge is removed) and all vertices that each are connected to will be connected
to the new "merged" vertex
3. Calculate all possible color combinations for each of the two new graphs
4. Subtract the merged graph's calculation from the removed graph's calculation and you have your result for the original graph

If either or both of the two new graphs are still too complicated, we can repeat this process for those graphs and even subsequent
ones until we finally reach definite calculations.


## Program interactive GUI implementation
The python program algorithm.py uses the **tkinter** module to create a graphical interface for the user to interact with.
Upon running the program, the user can click on empty space in the **canvas** to create a new vertex. In order to connect two
vertices via an edge, the user can click on a vertex and it will highlight red. Then the user just needs to click on any other
vertex and an edge will be created that connects the two vertices.
## Program algorithm implementation
The reduction algorithm process is done in the python algorithm file using recursion and can be done for many complicated graphs.
For its base cases, it checks for trees and complete graphs.
1. A tree is a graph that has no loops/cycles and each vertex has at least one connection
2. A complete graph is a graph where every vertex is connected to every other vertex

In order to check if two vertices are connected, the program uses operator overloading for checking equality via x, y coordinate pairs (coordinates instead?).
