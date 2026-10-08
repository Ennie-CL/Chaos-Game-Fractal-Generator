import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import patches


class Polygon:

    def __init__(self, sides, n, r):        
        # arry of vertices

        if sides == 4:          # checks if its a square
            vert = np.array([   # vertices to display the square
                [0., 0.],
                [0., 1.],
                [1., 1.],
                [1., 0.],
                [0., 0.],
                ])
            self.poly = Path(vert)
            self.vert = np.array([  # vertices of the square
                [0., 0.],
                [0., 1.],
                [1., 1.],
                [1., 0.],
                ])
        elif sides ==3:         # checks if its a triangle
            vert = np.array([   # vertices to display the triangle
                [0., 0.],
                [1., 0.],
                [0.5, np.sqrt(3)/2],
                [0., 0.],
                ])
            self.poly = Path(vert)
            self.vert = np.array([  # vertices of the triangle
                [0., 0.],
                [1., 0.],
                [0.5, np.sqrt(3)/2],
                ])
        self.n = n  
        self.r = r

    def calc_distance(self, A, B):  
    # helper function to calculate the point at r fraction between 2 points
        P = A + self.r * (B - A)

        return P

    def random_starting_point(self):
    # Generate a random point inside the polygon.
        while True:
            point = np.random.random(2)

            if self.poly.contains_point(point):
                return point


    def plot(self): # runs the normal random chaos game and displays it
        ax = plt.axes()

        patch = patches.PathPatch(self.poly, fc="none", ec="blue")  # creates the outline of the polygon
        ax.add_patch(patch)

        starting_point = self.random_starting_point()   # Generate a random starting point inside the polygon

        x = np.empty(self.n)    # creates empty array to store the points
        y = np.empty(self.n)

        for i in range(self.n):

            rand_vert = np.random.randint(0, len(self.vert))    # picks one of the vertices
            new_point = self.calc_distance(starting_point, self.vert[rand_vert])    # calcuate the distance between the point and the vertex

            x[i] = new_point[0] # stores the cordinates in the array
            y[i] = new_point[1]
            starting_point = new_point  # make the new point the starting point

        plt.plot(x, y, 'bo', ms=0.3)    # plots generated points, without joining them


        plt.axis("scaled")  # Keep the x and y axis scales equal
        plt.show()


    def read_sequence(self, filename):
        # reads a DNA sequence from a text file and returns it as a
        # single string of bases (strips newlines etc.)
        with open(filename, 'r') as f:
            sequence = f.read()

        sequence = sequence.replace("\n", "")
        sequence = sequence.replace(" ", "")

        return sequence


    def plot_dna(self, sequence):   # runs the chaos game using DNA sequence and displays it
        
        
        dna_vertices = {# Map each DNA base to an index in self.vert
            
            "A": 0,     # A = bottom-left
            "C": 1,     # C = top-left
            "G": 2,     # G = top-right
            "T": 3      # T = bottom-right
        }

        ax = plt.axes()
        
        patch = patches.PathPatch(self.poly, fc="none", ec="blue")  # creates the outline of the polygon
        ax.add_patch(patch)

        starting_point = self.random_starting_point()   # Generate a random starting point inside the polygon

        x = np.empty(len(sequence)) # creates empty array to store the points
        y = np.empty(len(sequence))

        for i, base in enumerate(sequence):
            if base not in dna_vertices:    # Ignore any character that is not A, C, G, or T
                continue

            vertex = dna_vertices[base] # Find the vertex associated with the current base
            new_point = self.calc_distance(starting_point, self.vert[vertex])   #calcuate the distance between the point and the vertex


            x[i] = new_point[0] # stores the cordinates in the array
            y[i] = new_point[1]
            starting_point = new_point

        plt.plot(x, y, 'bo', ms=0.1)    # plots generated points, without joining them

        plt.axis("scaled")  # Keep the x and y axis scales equal
        plt.show()



# Ask the user for the simulation settings
sides = int(input("Enter number of sides the polygon has: "))
n = int(input("Enter number of iterations N: "))
r = float(input("Enter the fraction of the distance r: "))

# Create the polygon and chaos-game object
my_poly = Polygon(sides, n, r,)   


# Run the normal chaos-game simulation
my_poly.plot()

# Uncomment the following lines to run the DNA simulation
#sequence = my_poly.read_sequence("HumanY_data.txt")
#print(len(sequence), "bases read")
#my_poly.plot_dna(sequence)
