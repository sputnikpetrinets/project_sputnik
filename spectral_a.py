#!/usr/bin/python
#model imports
#import petri_net_data
import numpy as np
import math
import random as r
import Tkinter as tk
#display imports
#import pygtk
#import gtk
#import matplotlib.pyplot as plt

class Spectral(object):
    '''Class to create coordinates from the solution to the
    Laplacaian eigenvector algorithm'''
    
    def __init__(self):
        """Init method, sets default window properties"""
        self.__width  = 1000
        self.__height = 1000
        self.__border = 20
        self.__d_radius = 60
        self.__pre_arcs = None
        self.__post_arcs = None
        self.__test_arcs = None
        self.__inhib_arcs = None
        self.__places = None
        self.__transitions = None


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
    def d_radius(self):
        """Getter for size of displacement radius."""
        return self.__d_radius

    @d_radius.setter
    def d_radius(self, value):
        """Setter for size of displacement radius."""
        self.__d_radius = value

    @property
    def places(self):
        """Setter for places variable."""
        return self.__places

    @places.setter
    def places(self, places):
        """Setter for places variable."""
        self.__places = places

    @property
    def adjacency(self):
        """Setter for places variable."""
        return self.__adjacency

    @adjacency.setter
    def adjacency(self, adjacency):
        """Setter for places variable."""
        self.__adjacency = adjacency

    @property
    def degree(self):
        """Setter for places variable."""
        return self.__degree

    @degree.setter
    def degree(self, degree):
        """Setter for places variable."""
        self.__degree = degree

    @property
    def laplacian(self):
        """Setter for places variable."""
        return self.__laplacian

    @laplacian.setter
    def laplacian(self, laplacian):
        """Setter for places variable."""
        self.__laplacian = laplacian






    def get_petri_net(self):
        """Get variables from petri net object and set
        class variables"""
        try:
            if not self.__petri_net.stoichiometry.pre_arcs.any():
                self.__pre_arcs_t = 0
                print "Error: pre arcs are null"
            else:
                self.__pre_arcs = np.asarray(self.__petri_net.stoichiometry.pre_arcs)
                self.__pre_arcs_t = 1
        except AttributeError:
            self.__pre_arcs_t = 0
            print "Error: pre arcs are null"

        try:
            if not self.__petri_net.stoichiometry.post_arcs.any():
                self.__post_arcs_t = 0
                print "Error: post arcs are null"
            else:
                self.__post_arcs = np.asarray(self.__petri_net.stoichiometry.post_arcs)
                self.__post_arcs_t = 1
        except AttributeError:
            self.__post_arcs_t = 0
            print "Error: post arcs are null"

        try:
            if not self.__petri_net.test_arcs.any():
                self.__test_arcs_t = 0
            else:
                self.__test_arcs = np.asarray(self.__petri_net.test_arcs)
                self.__test_arcs_t = 1
        except AttributeError:
            self.__test_arcs_t = 0

        try:
            if not self.__petri_net.inhibitory_arcs.any():
                self.__inhib_arcs_t = 0
            else:
                self.__inhib_arcs = np.asarray(self.__petri_net.inhibitory_arcs)
                self.__inhib_arcs_t = 1
        except AttributeError:
            self.__inhib_arcs_t = 0
        
        try:
            if not self.__petri_net.places.any():
                self.__places_t = 0
                print "Error: Places are null"
            else:
                self.__places = np.asarray(self.__petri_net.places)
                self.__places_t = 1
        except AttributeError:
            self.__places_t = 0
            print "Error: Places are null"
        except TypeError:
            try:
                if not self.__petri_net.places:
                    self.__places_t = 0
                    print "Error: Places are null"
                else:
                    self.__places = np.asarray(self.__petri_net.places)
                    self.__places_t = 1
            except ValueError:
                self.__places_t = 1
                self.__places = np.asarray(self.__petri_net.places)


        try:
            if not self.__petri_net.transitions.any():
                self.__transitions_t = 0
                print "Error: transitions are null"
            else:
                self.__transitions = np.asarray(self.__petri_net.transitions)
                self.__transitions_t = 1
        except AttributeError:
            self.__transitions_t = 0
            print "Error: transitions are null"
        except TypeError:
            try:
                if not self.__petri_net.transitions:
                    self.__transitions_t = 0
                    print "Error: transitions are null"
                else:
                    self.__transitions_t = 1
                    self.__transitions = np.asarray(self.__petri_net.transitions)
            except ValueError:
                self.__transitions_t = 1
                self.__transitions = np.asarray(self.__petri_net.transitions)


    def calculate(self):
        """Generates matrices and runs algorithm"""
        A = self.calculate_adjacency()
        self.__adjacency = A
        D = self.calculate_degree(A)
        laplacian = self.calculate_laplacian(D,A)
        cluster = 1
        coordinates = self.calculate_eigenvectors(laplacian,cluster)
        self.node_positions = coordinates
        return coordinates

    def calculate_adjacency(self):
        """Calculate adjacency matrix"""
        total = np.zeros(self.__pre_arcs.shape)
        if self.__pre_arcs_t == 1:
            total = total+self.__pre_arcs
        if self.__post_arcs_t == 1:
            total = total+self.__post_arcs
        if self.__test_arcs_t == 1:
            total = total+self.__test_arcs
        if self.__inhib_arcs_t == 1:
            total = total+self.__inhib_arcs
        rows,cols = total.shape
        X = rows+cols
        A = np.zeros((X,X))
        A[cols:rows+cols,0:cols] = total
        total_t = np.transpose(total)
        A[0:cols,cols:rows+cols] = total_t
        row = 0
        #set all non zero values to one to remove weightings
        for i in A:
            col =0
            for j in i:
                if j >0:
                    A[row,col] = 1
                col+=1
            row+=1
        return A

    def calculate_degree(self,A):
        """Create degree matrix from adjacency matrix """
        D = np.zeros((len(A),len(A)))
        for i in range(len(A)):
            D[i][i] = A[i].sum()
        return D

    def calculate_laplacian(self,D,A):
        """Create laplacian by subtracting adjacency matrix from degree matrix"""
        laplacian = D-A
        return laplacian

    def calculate_eigenvectors(self,laplacian,cluster):
        '''Calculates position vectors for each vertex ki
        [v1(i),v2(i)] using the ith component of vector vk'''
        l_rows,l_columns = laplacian.shape
        eigenvalues,eigenvectors = np.linalg.eigh(laplacian)
        i = eigenvalues.argsort()   
        eigenvalues = eigenvalues[i]
        eigenvectors = eigenvectors[:,i]
        count = 0
        x_pos = []
        y_pos = []
        for i in range(0,l_rows):
            x_pos.append(eigenvectors[:,1][count])
            y_pos.append(eigenvectors[:,2][count])
            count+=1
        vectors = np.array([x_pos,y_pos])
        count = 0
        coordinates = {}
        #get max vectors for scaling
        x_max = max(abs(vectors[0]))
        y_max = max(abs(vectors[1]))
        #create scale factor taking window size and border into account
        x_scale = math.floor(((self.__width/2)-self.__border/2)/(x_max))
        y_scale = math.floor(((self.__height/2)-self.__border/2)/(y_max))

        names = np.append(self.__places,self.__transitions)
        xy_list = []

        #processes each vector in turn
        for i in vectors[1]:
            #scales vector value to window
            x = vectors[0,count]*x_scale
            y = vectors[1,count]*y_scale
            count+=1
            #converts to closest int for coordinates
            x_mod = int(round(x))
            y_mod = int(round(y))
            #fixes coordinate system
            x_norm = x_mod+(self.__width/2)
            y_norm = (self.__height/2)-y_mod
            xy = (x_norm,y_norm)
            xy_list.append(xy)
        if cluster == 1:
            num_clusters = 0
            loop_token = -1
            cluster_found = 0
            while 1:

                #find cluster of nodes within d_radius distance
                xl = []
                yl = []
                i_c = 0
                max_cluster = {}
                for i in xy_list:
                    repel_dict = {}
                    j_c = 0
                    x1 = i[0]
                    y1 = i[1]
                    for j in xy_list:
                        if i_c != j_c:
                            x2 = j[0]
                            y2 = j[1]
                            distance = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                            #add this j to the repel dict as it is too close to i
                            if distance < self.__d_radius:
                                repel_dict[j_c] = (x2,y2)
                                cluster_found = 1
                        j_c +=1

                    #calculate the centroid of this cluster
                    if len(repel_dict) != 0:
                        if loop_token == -1:
                            num_clusters+=1
                        repel_dict[i_c] = (x1,y1)
                        x_total = 0
                        y_total = 0
                        for k in repel_dict.keys():
                            x_total += repel_dict[k][0]
                            y_total += repel_dict[k][1]
                        number =  len(repel_dict)
                        centroid = (x_total/number,y_total/number)
                        #identify which cluster has the most elements
                        if len(repel_dict) > len(max_cluster):
                            max_cluster = repel_dict
                            max_centroid = centroid

                        #centroid coordinate list###testing 
                        xl.append(centroid[0])
                        yl.append(centroid[1])
                    i_c+=1
                if cluster_found ==0:
                    break

                #displace points in cluster out from centroid
                for k in max_cluster.keys():
                    x1 = max_cluster[k][0]
                    y1 = max_cluster[k][1]
                    x2 = max_centroid[0]
                    y2 = max_centroid[1]
                    x_dis = x1-x2
                    y_dis = y1-y2
                    distance = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                    if distance ==0:
                        i = r.randrange(-2,2)
                        j = r.randrange(-2,2)
                        x1 = x1+60*i
                        y1 = y1+60*j
                    else:
                        scale = (distance+30)/(distance)#+0.001)
                        if x_dis <0:
                            x1 = x2 + (x_dis*scale)
                        else:
                            x1 = x2 + (x_dis*scale)
                        if y_dis <0:
                            y1 = y2 + (y_dis*scale)
                        else:
                            y1 = y2 + (y_dis*scale)
                    x1 = round(x1)
                    y1 = round(y1)

                    #ensure nodes are in drawing area
                    if x1 > self.__width-self.__border:
                        x1 = self.__width-self.__border
                    if x1 < self.__border:
                        x1 = self.__border
                    if y1 > self.__height-self.__border:
                        y1 = self.__height-self.__border
                    if y1 < self.__border:
                        y1 = self.__border
                    xy = (round(x1),round(y1))
                    xy_list[k] = xy
                loop_token = 0
                num_clusters -=1
                if num_clusters ==0:
                    break
        count = 0
        x_temp = []
        y_temp = []
        for i in xy_list:
                x_temp.append(i[0])
                y_temp.append(i[1])
                coordinates[names[count]] = i
                count+=1       
#        print
#        print "Coordinate dict",coordinates
        return coordinates

    def render_graph(self):
        self.__degree = self.calculate_degree(self.__adjacency)
        self.__laplacian = self.calculate_laplacian(self.__degree,self.__adjacency)
        cluster = 0
        self.__node_positions = self.calculate_eigenvectors(self.__laplacian,cluster)
        window = tk.Tk()
        canvas = tk.Canvas(window, width=self.__width, height=self.__height, bg='white')
        canvas.pack()
        row = 0
        for i in self.__places:
            col = 0
            for j in self.__places: 
                if self.__adjacency[row,col] == 1:
                    #draw line from coordinates of point i to coordinates of point j
                    x1 = self.__node_positions[i][0]
                    y1 = self.__node_positions[i][1]
                    x2 = self.__node_positions[j][0]
                    y2 = self.__node_positions[j][1]
                    canvas.create_line(x1, y1, x2, y2, tags='line') 
                col+=1
            row+=1
        window.mainloop()
