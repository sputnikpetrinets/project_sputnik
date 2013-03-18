#!usr/bin/python
#model imports
import petri_net_data
import numpy as np
import random as r
import decimal as d
import math
import spectral_a
import time as t
#display imports
#import pygtk
#import Tkinter as tk
import sys
class ForceDirected(object):
    '''Class to create coordinates for the initial petrinet layout
    and coordinates for the minimum energy layout configuration'''
    def __init__(self):
        self.__width  = 1000
        self.__height = 1000
        self.__border = 20
        self.__center_distance = 10.0
        self.__scaling_factor = 1.0
        self.__zoom_in_border = 1.0
        self.__circle_diameter = 20.0
        self.__iterations = 1

    @property
    def iterations(self):
        """Getter for iterations variable."""
        return self.__iterations

    @iterations.setter
    def iterations(self, i):
        """Setter for iterations variable."""
        self.__iterations = i

    @property
    def petri_net(self):
        """Getter for petri net data object."""
        return self.__petri_net

    @petri_net.setter
    def petri_net(self, p):
        """Setter for petri net data object."""
        self.__petri_net = p

    @property
    def width(self):
        """Getter for width variable."""
        return self.__width

    @width.setter
    def width(self, width):
        """Setter for width variable."""
        self.__width = width

    @property
    def height(self):
        """Getter for height variable."""
        return self.__height

    @height.setter
    def height(self, height):
        """Setter for height variable."""
        self.__height = height

    @property
    def border(self):
        """Getter for border variable."""
        return self.__border

    @border.setter
    def border(self, border):
        """Setter for border variable."""
        self.__border = border

    @property
    def node_positions(self):
        """Getter for node_positions variable."""
        return self.__node_positions

    @node_positions.setter
    def node_positions(self, coordinates):
        """Setter for node_positions variable."""
        self.__node_positions = coordinates

    @property
    def grid_size(self):
        """Getter for width of grid."""
        return self.__grid_size

    @grid_size.setter
    def grid_size(self, value):
        """Setter for width of grid."""
        self.__grid_size = value

    @property
    def places(self):
        """Setter for places variable."""
        return self.__places

    @places.setter
    def places(self, places):
        """Setter for places variable."""
        self.__places = places

    def get_petri_net(self):
        """Gets variables from petri net object and set
        class variables"""
        self.__pre_arcs = np.asarray(self.__petri_net.stoichiometry.pre_arcs)
        self.__post_arcs = np.asarray(self.__petri_net.stoichiometry.post_arcs)
        self.__test_arcs = np.asarray(self.__petri_net.test_arcs)
        self.__inhib_arcs = np.asarray(self.__petri_net.inhibitory_arcs)
        self.__places = np.asarray(self.__petri_net.places)
        self.__transitions = np.asarray(self.__petri_net.transitions)

    def calculate(self):
        """Runs algorithm"""
        start = t.time()
        self.__connected = self.get_connected()
        self.rand_locations()
        coordinates = self.main()
        self.node_positions = coordinates
        return coordinates

    def get_connected(self):
        '''uses the pre post test inhib matrices to determine which
        vertices are connected with edges'''
        total = self.__pre_arcs + self.__post_arcs# + self.__test_arcs + self.__inhib_arcs
        self.__edges = np.nonzero(total)
        connected = []
        lenp = len(self.__places)
        g = 0
        h = 0
        for row in total:
            g = 0
            while g < lenp:
                if (total[h,g] != 0):
                    temp_h = h+1
                    total_g = lenp+temp_h
                    corrected_g = total_g-1
                    pair = []
                    pair = [g,corrected_g]
                    connected.append(pair)
                g+=1
            h+=1
        return connected

    # randomise the initial location of vertices
    def rand_locations(self):
        time_1 = t.time()
        '''Method generates coordinates for initial random positioning'''
        #build graph components
        verticies = np.array([])
        verticies = np.concatenate([self.__places,self.__transitions])
        n_verticies = len(verticies)
        row_0 = [0.0 for i in xrange(n_verticies)]
        #starting with spectral layout rather than true random makes for a better starting point
        s = spectral_a.Spectral()
        s.petri_net = self.__petri_net
        s.get_petri_net()
        coordinates = s.calculate()
        #export positions and velocities
        
        x_pos = [coordinates[key][0] for key in verticies]
        y_pos = [coordinates[key][1] for key in verticies]

        x_dis = [0.0 for i in xrange(len(verticies))]
        y_dis = [0.0 for i in xrange(len(verticies))]

        node_id = [i for i in range(len(verticies))]

        attract_x = [0.0 for i in xrange(len(verticies))]
        attract_y = [0.0 for i in xrange(len(verticies))]
        self.__pos = np.array([row_0, x_pos, y_pos, x_dis, y_dis, node_id, attract_x, attract_y])
        #print self.__pos
        #sys.exit()

        return self.__pos


    def main(self):
        '''Itteratively runs force directed placement algorithm to 
        generate minimum energy layout configuration'''
        #rows of self.__pos are:
        #0  verticies, verticies
        #1  x_pos, x position
        #2  y_pos, y position 
        #3  x_dis, displacement
        #4  y_dis, displacement
        #5  node_id, 
        #6  attract_x, x attraction force
        #7  attract_y y attraction force
        itr_count=1
        dampening_coefficient = 0.5 # testing
        spring_stiffness = 0.3#0.06
        repulsive_strength = 3500.0#3500.0
        overlapped_displacement_dist = 4.0
        time_1 = t.time()
        while itr_count <= self.__iterations:
            #print "iteration:",itr_count
            itr_count +=1
            #calculate the repulsive forces pairwise between nodes
            for vertex_i, val in enumerate(self.__pos[0]):
                self.__pos[3][vertex_i] = 0
                self.__pos[4][vertex_i] = 0
                # get the x and y coordinates for vertex v from the list
                vi_x = self.__pos[1][vertex_i]
                vi_y = self.__pos[2][vertex_i]
                vi_id = self.__pos[5][vertex_i]
                
                # we loop again through all vertices for a pairwise comparison
                for vertex_j, val in enumerate(self.__pos[0]):
                    # get the x and y coordinates for vertex u from the list    
                    vj_x = self.__pos[1][vertex_j]
                    vj_y = self.__pos[2][vertex_j]
                    vj_id = self.__pos[5][vertex_j]
                    # checks if same vertex to prevent self comparison
                    if (vj_id != vi_id):
                        # difference in position of v and u
                        dx = vi_x-vj_x
                        dy = vi_y-vj_y
                        distance = dx*dx + dy*dy
                        if distance !=0:
                            self.__pos[3][vertex_i] = self.__pos[3][vertex_i] + repulsive_strength*dx/distance
                            self.__pos[4][vertex_i] = self.__pos[4][vertex_i] + repulsive_strength*dy/distance
                        else:
                            print "nodes stacked - perturbing"
                            self.__pos[3][vertex_i] = self.__pos[3][vertex_i] + overlapped_displacement
                            self.__pos[4][vertex_i] = self.__pos[4][vertex_i] + overlapped_displacement

                        #calculate attractive forces
                        for pair in self.__connected:
                            # check if vi matches the list
                            if (pair[0] == vertex_i) and (pair[1] == vertex_j):
                                vj_x = self.__pos[1][pair[1]]
                                vj_y = self.__pos[2][pair[1]]
                                dx = vi_x-vj_x
                                dy = vi_y-vj_y
                                distance = dx*dx + dy*dy
                                if distance !=0:
                                    #  calculates vector delta
                                    self.__pos[3][vertex_i] = self.__pos[3][vertex_i] - (dx*spring_stiffness)
                                    self.__pos[4][vertex_i] = self.__pos[4][vertex_i] - (dy*spring_stiffness)
                                else:
                                    #on top of node 
                                    print "stacked nodes"
                                    self.__pos[3][vertex_i] = self.__pos[3][vertex_i] + overlapped_displacement 
                                    self.__pos[4][vertex_i] = self.__pos[4][vertex_i] + overlapped_displacement 

            #set new velocity based on current velocity
            # and the combined attractive/repulsive forces
            #velocity is multiplied by dampening coefficient
            self.__pos[6] = (self.__pos[6] + self.__pos[3])*dampening_coefficient
            self.__pos[7] = (self.__pos[7] + self.__pos[4])*dampening_coefficient
            self.__pos[1] = (self.__pos[1] + self.__pos[6])
            self.__pos[2] = (self.__pos[2] + self.__pos[7])

            #Scale the size of the graph
            #get the minimum x and the maximum x the difference between these is the graph_width
            #devide the self.__width-2*border by graph width to get a factor which is less that 1 if the 
            #graph is bigger than the window or less if it is smaller, multiply all x coordinates by this factor

            #find the difference between the smallest x value and self.__border, call it x_difference
            # add x_difference to all x coordinates and this will centralize the graph in the window
            x_max = max(self.__pos[1])
            x_min = min(self.__pos[1])
            y_max = max(self.__pos[2])
            y_min = min(self.__pos[2])
            
            #find the graph_width and height
            graph_width = x_max - x_min
            graph_height = y_max - y_min
        
            #create scale factor taking window size and border into account
            x_scale = (self.__width - (2*self.__border)) / graph_width
            y_scale = (self.__height - (2*self.__border)) / graph_height
            
            #multiply all x coordinates by x_scale and all y coordinates by y_scale to scale the graph to the window
            self.__pos[1] *= x_scale
            self.__pos[2] *= y_scale

            #find the difference between the smallest x value and self.__border
            x_difference = self.__border-(x_min*x_scale)
            #find the difference between the smallest y value and self.__border
            y_difference = self.__border-(y_min*y_scale)
            
            #shift all x coordinates by x_difference and all y coordinates by y_difference
            self.__pos[1] = self.__pos[1] + x_difference
            self.__pos[2] = self.__pos[2] + y_difference

        coordinates = {}
        names = np.append(self.__places,self.__transitions)
        for i, val in enumerate(self.__pos[0]):
            x = round(self.__pos[1][i])
            y = round(self.__pos[2][i])
            pair = x,y
            coordinates[names[i]] = pair
        return coordinates 
  
if __name__ == "__main__":
    pass
    #Layout()
