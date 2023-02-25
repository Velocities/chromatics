import tkinter as tk

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, a) -> bool:
        return (self.x, self.y) == (a.x, a.y)
    
    def draw(self, canvas):
        r = 10
        if self.selected:
            outline = "red"
        else:
            outline = "black"
        canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, outline=outline, fill="white")
        
    def contains(self, x, y):
        r = 10
        return (x-self.x)**2 + (y-self.y)**2 < r**2

# Algorithms to be implemented into canvasusage.py for finding chromatic polynomial

# SELF Note:
# The functions currently present are our "base cases", where we always know what the result will be
# Next time, we need to figure out how to work our way down to these base cases via our Reduction Algorithm

# Note: It is assumed that when we run this function, we are dealing with a
# root, whose child node has one/two children (and so on for THOSE children)
answer = None
def tree_polynomial(k: int, vertex_count: int) -> int:
    """
    Returns the chromatic polynomial for a particular tree
    """
    result = k * ((k-1)**(vertex_count-1))
    return result

# Note: It is assumed that when we run this function, we are ALWAYS
# dealing with a complete graph (as shown in documentation)
def complete_graph_polynomial(k: int, vertex_count: int) -> int:
    """
    Returns the chromatic polynomial for a complete graph
    """
    from math import factorial
    # If there aren't enough colors to compose the complete graph,
    # we know that there isn't any possible chromatic polynomial (so we return 0)
    if k < vertex_count:
        return 0
    result = factorial(k)/factorial(k-vertex_count)
    return int(result)

# (Consider reusing vertex-edge comparison code for modularity)
def vertex_degrees(vertex_list: list[Vertex], edge_list: list[tuple]) -> list[int]:
    """
    Returns a list of ints, indicating the number of edges corresponding to each vertex in vertex_list
    """
    result = []
    # Iterate through a list of vertex objects/instances
    for i in vertex_list:
        current = 0
        # Iterate through a list of edges (which contains tuples of the two connected vertex objects)
        for j in edge_list:
            # Compare the x,y coordinates of the current vertex with the x,y coordinates of both sides of the edge
            # (if either of them are the same x,y coordinate pairing, we increment the degree counter)
            if (i.x, i.y) == (j[0].x, j[0].y) or (i.x, i.y) == (j[1].x, j[1].y):
                current += 1
        result.append(current)
    return result

# A standalone implementation of the breadth-first search algorithm that checks if a given graph is connected or not
def is_connected_graph(vertices: list[Vertex], edges: list[tuple[Vertex]]) -> bool:
    """
    A function that determines if a graph represented by a list of vertices and a list of edges is connected.
    """
    # Create a set containing all the vertices
    unvisited = set(vertices)
    # Create a queue to keep track of the vertices to visit
    queue = []
    # Start by visiting the first vertex
    queue.append(vertices[0])
    # Add the first vertex to the visited set
    unvisited.remove(vertices[0])
    while len(queue) > 0:
        # Take the next vertex to visit from the queue
        current = queue.pop(0)
        # Check all the edges of the current vertex
        for v1, v2 in edges:
            # If an edge connects to a vertex that hasn't been visited yet
            if (current == v1 and v2 in unvisited) or (current == v2 and v1 in unvisited):
                # Add it to the queue to visit
                queue.append(v1 if current == v2 else v2)
                # Remove it from the unvisited set
                unvisited.remove(v1 if current == v2 else v2)
    # If there are no more unvisited vertices, the graph is connected
    return len(unvisited) == 0

# Has been tested and (*seems*) to work
def is_tree(vertex_list: list[Vertex], edge_list: list[tuple[Vertex]]) -> bool:
    """
    Returns a true or false value, determining if a graph is a tree or not
    """
    # The graph can't be a tree if it isn't connected, so we can potentially stop here
    if not is_connected_graph(vertex_list, edge_list):
        return False
    for i in range(len(edge_list)):
        copy = list(edge_list)
        copy.pop(i)
        # If the graph is still connected after we remove an edge, then we don't have a real tree!
        if is_connected_graph(vertex_list, copy):
            return False
    # If we have reached this point, we have determined that any 
    # edge can be removed and will result in a disconnected graph
    return True

def is_complete_graph(vertex_list: list[Vertex], edge_list: list[tuple[Vertex]]) -> bool:
    """
    Returns a true or false value, indicating if a graph is a complete graph or not
    """
    polynomial_degrees = vertex_degrees(vertex_list, edge_list)
    if polynomial_degrees[0] == (len(vertex_list) - 1) and len(set(polynomial_degrees)) == 1:
        return True
    return False

# Has been tested at a base level
def are_connected_vertices(v1: Vertex, v2: Vertex, edge_list: list[tuple[Vertex]]) -> bool:
    """
    Returns a true or false value, indicating if two vertices are connected via an edge or not
    """
    if ((v1, v2) in edge_list) or ((v2, v1) in edge_list):
        return True
    #for edge in edge_list:
    #    # Check if the coordinates of both ends of an edge are the coordinates of the two vertices
    #    if (v1.x, v1.y) == (edge[0].x, edge[0].y) and (v2.x, v2.y) == (edge[1].x, edge[1].y):
    #        return True
    #    elif (v2.x, v2.y) == (edge[0].x, edge[0].y) and (v1.x, v1.y) == (edge[1].x, edge[1].y):
    #        return True
    # If we reach this point, we know that none of the edges involve the coordinates of both vertices
    # (in other words, the vertices are not connected via an edge)
    return False

def remove_edge(v1: Vertex, v2: Vertex, edge_list: list[tuple[Vertex]]) -> None:
    """
    Removes an edge that connects two specified vertices
    Note: Must be done on two vertices that are known to be connected (no exceptions)
    """
    curr_index = 0
    for edge in edge_list:
        if (v1.x, v1.y) == (edge[0].x, edge[0].y) and (v2.x, v2.y) == (edge[1].x, edge[1].y):
            edge_list.pop(curr_index)
            break
        elif (v2.x, v2.y) == (edge[0].x, edge[0].y) and (v1.x, v1.y) == (edge[1].x, edge[1].y):
            edge_list.pop(curr_index)
            break
        curr_index += 1
            
#algorithm(graph G) {
#    
#    int remove;
#    int merge;
#
#    // base case
#    if (G is Tree or Complete) {
#        return Chromatic Polynomial;
#    }
#    // Breakdown ----
#    // remove 
#    int remove = algorithm(removeEdge(G));
#    
#    // merge 
#    int merge = algorithm(mergeVert(G));
#    return (remove - merge); // chromatic polynomial
#}
#
#// where removeEdge(Graph G); and mergeVert(Graph G) are separate methods.
def algorithm(vertex_list: list[Vertex], edge_list: list[tuple[Vertex]], color_count) -> int:
    degrees = vertex_degrees(vertex_list, edge_list)
    non_connected_graph_result = 0
    if max(degrees) == 0:
        return 5**(len(degrees))
    empty_degrees = degrees.count(0)
    for i in range(empty_degrees):
        empty_vert_index = degrees.index(0)
        vertex_list.pop(empty_vert_index)
        degrees.remove(0)
        non_connected_graph_result += 1
    if non_connected_graph_result > 0:
        empty_multiplier = color_count**non_connected_graph_result
    else:
        empty_multiplier = 1
    if is_tree(vertex_list, edge_list):
        return empty_multiplier * tree_polynomial(color_count, len(vertex_list))
    elif is_complete_graph(vertex_list, edge_list):
        return empty_multiplier * complete_graph_polynomial(color_count, len(vertex_list))
    highest_index = degrees.index(max(degrees))
    # This variable stores the vertex object that has the highest degree
    highest = vertex_list[highest_index]
    # This variable ensures we keep checking from the highest values to lower values
    # so we find the connected vertex that has the next highest degree
    finding_next_highest = True
    if degrees.count(max(degrees)) > 1:
        next_highest_degree = max(degrees)
    else:
        next_highest_degree = max(degrees) - 1
    removed_edge_list = list(edge_list)
    # This loop finds the degree with the next highest vertex that's connected to the vertex with the highest degree
    while finding_next_highest:
        for curr_index in range(len(degrees)):
            # This condition checks if we reached the index of a vertex with the next highest degree
            # and ensures that we aren't on the same vertex as the one we found that has the absolute highest degree
            if degrees[curr_index] == next_highest_degree and curr_index != highest_index:
                next_highest_test = vertex_list[curr_index]
                # Test here
                if are_connected_vertices(highest, next_highest_test, edge_list):
                    finding_next_highest = False
                    # Stores the vertex object that has the next highest degree (connected to the vertex with the highest degree)
                    next_highest = next_highest_test
                    remove_edge(highest, next_highest, removed_edge_list)
                    break
        if finding_next_highest:
            next_highest_degree -= 1
    #print(max(degrees))
    #print(next_highest_degree)
    # We need to remove the edge that connects the two vertices with the highest degrees
    r_copied_vlist = list(vertex_list)
    r_copied_elist = list(removed_edge_list)
    remove = algorithm(r_copied_vlist, r_copied_elist, color_count)
    #print(remove)
    # 1. Look for two vertices with the highest degrees
    # 2. If one of them has less connections, merge that one onto the other one
    #     - Else, just merge one onto the other
    # Note: Check for non-mutual connections; any non-mutual connections will be added 
    #       onto the one that is the destination of the merge, if not already connected to that
    # Here we are checking if one of the 2 vertices we are merging has a higher degree than the other
    # Merge the one with less connections onto the other
    for edge in removed_edge_list:
        # If we find a connection that next_highest has with a vertex that highest
        # has a mutual connection with, we remove that mutual connection from next_highest
        if next_highest == edge[0]:
            # Note: This has been tested in a standalone test on an online IDE by Programiz
            #       and proved successful in removing the correct edge (consider further implementation in priorly developed code)
            if ((edge[1], highest) in removed_edge_list) or ((highest, edge[1]) in removed_edge_list):
                removed_edge_list.remove(edge)
            # If the connection is not mutual, we must add the connection to highest
            else:
                removed_edge_list.append((highest, edge[1]))
                removed_edge_list.remove(edge)
        elif next_highest == edge[1]:
            if ((edge[0], highest) in removed_edge_list) or ((highest, edge[0]) in removed_edge_list):
                removed_edge_list.remove(edge)
            # If the connection is not mutual, we must add the connection to highest
            else:
                removed_edge_list.append((highest, edge[0]))
                removed_edge_list.remove(edge)
    vertex_list.remove(next_highest)
    m_copied_vlist = list(vertex_list)
    m_copied_elist = list(removed_edge_list)
    merge = algorithm(m_copied_vlist, m_copied_elist, color_count)
    #print(f"Removed portion: {type(remove)}")
    #print(f"Merged portion: {type(merge)}")
    return empty_multiplier * (remove - merge)

class Graph:
    graphtype = ""
    def __init__(self) -> None:
        self.vertices = []
        self.edges = []
        # List where each element corresponds to an element in self.vertices,
        # indicating how many edges each vertex has
        self.degree = []
        
    
    def add_vertex(self, x, y) -> None:
        self.vertices.append(Vertex(x, y))
    
    # self.edges[0][0].x
    def add_edge(self, v1, v2):
        self.edges.append((v1, v2))
    
    # Create an edge after two vertices are consecutively clicked
    def draw(self, canvas):
        for v in self.vertices:
            v.draw(canvas)
        for (v1, v2) in self.edges:
            canvas.create_line(v1.x, v1.y, v2.x, v2.y)
            
    def vertex_at(self, x, y):
        for v in self.vertices:
            if v.contains(x, y):
                return v
        return None

class App:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        self.graph = Graph()
        self.selected_vertex = None
        self.first_click = None
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Create a reset button
        self.reset_button = tk.Button(master, text="Reset")
        self.calculate_button = tk.Button(master, text="Calculate")
        self.reset_button.pack()
        self.calculate_button.pack()
        self.reset_button.bind("<Button-1>", self.reset)
        self.calculate_button.bind("<Button-1>", self.calculate)
        
    def on_click(self, event):
        x, y = event.x, event.y
        vertex = self.graph.vertex_at(x, y)
        # If this if statement returns True, then we know the user has selected a vertex and is trying to create an edge
        if vertex is not None:
            vertex.selected = not vertex.selected
            if self.first_click is None:
                self.first_click = vertex
            else:
                self.graph.add_edge(self.first_click, vertex)
                self.first_click = None
        else:
            self.graph.add_vertex(x, y)
        self.graph.draw(self.canvas)
        
    # Reset button (used to clear the Canvas)
    def reset(self, event):
        # Clear the canvas
        self.canvas.delete("all")
        # Reset the graph
        self.graph = Graph()
        self.first_click = None
    
    # Calculate button (experimental)
    def calculate(self, event):
        copy_of_vertices = list(self.graph.vertices)
        copy_of_edges = list(self.graph.edges)
        x = algorithm(copy_of_vertices, copy_of_edges, 5)
        print(x)

root = tk.Tk()
root.title("Chromatic Polynomial")
app = App(root)
# Make the window appear
root.mainloop()