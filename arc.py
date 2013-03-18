#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo
import math

import component
import place
import transition
import font
import standard_arrow_head

from numpy import array
from math import pi
from math import atan2
from math import atan
from math import cos
from math import sin
from math import tan

class Arc(component.Component):
    """
    The Arc class is used to characterise an arc and it inherits from the general parent class Component. Via a defined GraphicsObject the arc can be placed directly on the referenced surface between two defined positions.
    """

    LINE_TYPE_ARC_LOWER = 0
    LINE_TYPE_ARC_UPPER = 1
    LINE_TYPE_STRAIGHT = 2

    _head = standard_arrow_head.StandardArrowHead()

    # update
    def __init__(self):
	""" Constructor of Arc and default values will be initialised. """

        # call constructor of parent class
        super(Arc, self).__init__()

        # 0, 1 (input), 2 (output)
        self._arc_type = 0
        self.__ctr = 0
        self._origin = None
        self._target = None
        self._target_position = None
        self._arrow = None
        self._weight = 1.
        self._line_type = self.LINE_TYPE_STRAIGHT
        self._font_weight = font.Font() #self._get_default_font()
        self._head = standard_arrow_head.StandardArrowHead()

    @property
    def origin(self):
        """ Return origin component (Component-Object). """
        return self._origin

    @property
    def target(self):
        """ Return target component (Component-Object). """
        return self._target

    @property
    def weight(self):
        """ Return weight. """
        return self._weight

    @property
    def font_weight(self):
        """ Return font of the weight (Font-Object). """
        return self._font_weight

    @property
    def line_type(self):
        """ Return line type. """
        return self._line_type
    
    @property
    def target_position(self):
        """ Return target position. """
        return self._target_position

    @origin.setter
    def origin(self, component):
        """ Set origin component (Component-Object). """
        self._origin = component

    @target.setter
    def target(self, component):
        """ Set target component (Component-Object). """
        self._target = component

    @weight.setter
    def weight(self, weight):
        """ Set weight. """
        self._weight = weight

    @font_weight.setter
    def font_weight(self, font):
        """ Set font for the weight (Font-Object). """
        self._font_weight = font

    @line_type.setter
    def line_type(self, t):
        """ Set line type. """
        self._line_type = t	

    @target_position.setter
    def target_position(self, pos):
        """ Set target position. """
        self._target_position = pos

    def draw(self, ctx):
        pos = None
        # check if a target is defined
        if self._target != None and self._target_position == None:
            # check if an origin is defined because drawing an arch without origin is not possible
            if self._origin != None:
                # read the actual position (start- and end-position)
                pos = self.get_positions()
                # check if a start- and end-position could be determined
                if pos != None:
                    # draw the actual arc
                    self._draw_arrow(ctx, pos[0], pos[1])
        else:
	    if self._target_position != None:
	        # read the actual position (start- and end-position)
	        pos = self.get_positions()
	        # draw the actual arc
	        self._draw_arrow(ctx, pos[0], self._target_position)
        ctx.stroke()

    def calculate_control_point(self, start_position, end_position, x_offset, y_offset):
        """ Calculate position of the control point for a quadratic curve which is defined trough a start- and end-position as well as an offset in x- and y-direction in the centre of a straight connection between the start- and end-position.  """

        # calculate differences between the positions
        dx = float(int(end_position[0] - start_position[0]))
        dy = float(int(end_position[1] - start_position[1]))
        # calculate angle between the two positions
        angle = atan2(dy, dx)
        # calculate the position of the control point
        arrow_x0 = int(start_position[0] + dx / 2 + cos(angle + pi / 2) * x_offset)
        arrow_y0 = int(start_position[1] + dy / 2 + sin(angle + pi / 2) * y_offset)
        # return the position of the control point
        return arrow_x0, arrow_y0
        
    def get_positions(self):
        """ Calculate the true start- and end-position of the line according to the defined origin and target component. """

        # initial positions
        pos_origin = [0, 0]
        pos_target = [0, 0]
        try:
	    alpha = 0
	    x_q = 0
	    y_q = 0
	    if self._target != None:
                # calculate angle between the two components
                alpha = atan2(self._target.position[1] - self._origin.position[1], self._target.position[0] - self._origin.position[0])
		# calculate position of the control point
                x_q, y_q = self.calculate_control_point(self._origin.position, self._target.position, 45, 45)
	    else:
		alpha = atan2(self._target_position[1] - self._origin.position[1], self._target_position[0] - self._origin.position[0])

            # check if the origin component is a place
            if type(self._origin) == place.Place:
                # check the line type of the arc
                if self._line_type == self.LINE_TYPE_ARC_LOWER or self._line_type == self.LINE_TYPE_ARC_UPPER:
                    # calculate start-position of the place (on the circle)
                    pos_origin = self.get_position_place(self._origin, [x_q, y_q], alpha, True, False)
                else:
                    # calculate start-position of the place (on the circle)
                    pos_origin = self.get_position_place(self._origin, None, alpha, True, True)
		if self._target != None:
                    # calculate end-position of the transition
                    pos_target = self.get_position_transition(self._target, self._origin.position, alpha, False)
		else:
		    pos_target = self._target_position

            else:
		if self._target != None:
                    # check the line type of the arc
                    if self._line_type == self.LINE_TYPE_ARC_LOWER or self._line_type == self.LINE_TYPE_ARC_UPPER:
                        # calculate end-position of the place (on the circle)
                        pos_target = self.get_position_place(self._target, [x_q, y_q], alpha, False, False)
                    else:
                        # calculate end-position of the place (on the circle)
                        pos_target = self.get_position_place(self._target, None, alpha, False, True)
		    # calculate start-position of the transition
                    pos_origin = self.get_position_transition(self._origin, self._target.position, alpha, True)
		else:
		    pos_target = self._target_position
                    # calculate start-position of the transition
                    pos_origin = self.get_position_transition(self._origin, self._target_position, alpha, True)
        except IndexError:
            pos_origin = [0, 0]
            pos_target = [0, 0]

        # return true positions
        return (pos_origin, pos_target)

    def get_position_place(self, component, control_point, alpha, is_origin, is_straight_line):
        """ Calculate the true position on the circle for a connection with an arc. The component defines the type and delivers the needed information about the place, control_point defines the control point position, alpha is the angle between the two components, is_origin is TRUE if the place is the origin of the arc and is_straight_line is TRUE when the connection should be a straight one. """

        # initial position
        pos = [0, 0]
        # check the if the component is really a place
        if type(component) == place.Place:
            # check the line type
            if not is_straight_line:
                # calculate the offset values for each dimension to determine the true connection point
                new_alpha = atan2(control_point[1] - component.position[1], control_point[0] - component.position[0])
                dx = component.radius * cos(new_alpha)
                dy = component.radius * sin(new_alpha)
                # adapt the component position
                if is_origin:
                    pos = [component.position[0] + dx, component.position[1] + dy]
                else:
                    pos = [component.position[0] + dx, component.position[1] + dy]
            else:
                # calculate the offset values for each dimension to determine the true connection point
                dx = component.radius * cos(alpha)
                dy = component.radius * sin(alpha)
                # adapt the component position
                if is_origin:
                    pos = [component.position[0] + dx, component.position[1] + dy]
                else:
                    pos = [component.position[0] - dx, component.position[1] - dy]
    
        # return the true position where the arc should be connected
        return pos

    def get_position_transition(self, component, position, alpha, is_origin):
        """ Calculate the true position on a transition for a connection with an arc. The component defines the type and delivers the needed information about the place, position defines the position of the other component, alpha is the angle between the two components and is_origin is TRUE if the transition is the origin of the arc. """

        # initial position
        pos = [0, 0]
        # check the if the component is really a transition
        if type(component) == transition.Transition:
            # calculate the distance between the possible connection points
            dx = int(component.dimension[0] / 2)
            d = component.dimension[1] / 9
            dy = 0

            # determine the type of connection and determine the y-offset
            if self._target != None:
                if self._line_type == self.LINE_TYPE_ARC_LOWER and self._target.is_equal(component):
                    dy = 2*d
                if self._line_type == self.LINE_TYPE_ARC_UPPER and self._target.is_equal(component):
                    dy = -2*d
                if self._line_type == self.LINE_TYPE_ARC_LOWER and not self._target.is_equal(component):
                    dy = d
                if self._line_type == self.LINE_TYPE_ARC_UPPER and not self._target.is_equal(component):
                    dy = -d
                if self._line_type == self.LINE_TYPE_STRAIGHT:
                    dy = 0

            # check if a position is defined
            if position != None:
                if position[0] < component.position[0]:
                    dx *= -1
                else:
                    dy *= -1
            # determine the true position where the arc needs to be connected to
            pos = [component.position[0] + dx, component.position[1] + dy]

        # return the true position where the arc should be connected to
        return pos

    def clone(self):
        """ Duplication of the current place and the duplicate will be returned. """
        # duplicate
        comp = Arc()
        # general component properties
        comp.key = self.key
        comp.label = self.label
        comp.description = self.description
        comp.x_offset = self.x_offset
        comp.y_offset = self.y_offset
        comp.font_label = self.font_label.clone()
        comp.font_description = self.font_description.clone()
        comp.position = copy.deepcopy(self.position)
        comp.rgb_edge = copy.deepcopy(self.rgb_edge)
        comp.rgb_fill = copy.deepcopy(self.rgb_fill)
        comp.count_inputs = self.count_inputs
        comp.count_outputs = self.count_outputs
        # arc specific properties
        comp.line_type = self.line_type

        comp.weight = self.weight
        comp.origin = self.origin.clone()
        comp.target = self.target.clone()
        # return the duplicate
        return comp

    def _draw_arrow(self, ctx, pos_from, pos_to):
        """ Draw the arrow onto the surface referenced by the GraphicsContext from the start- to the end-position. """

        # set the basic colour for the arc
        ctx.set_source_rgb(*self._edge)

        # set the properties for a transparent arc
        r = 0
        g = 0
        b = 0
        if self._edge[0] != 0:
            r = 1
        if self._edge[1] != 0:
            g = 1
        if self._edge[2] != 0:
            b = 1
        ctx.set_source_rgba(r, g, b, 0.60)
        ctx.move_to(pos_from[0], pos_from[1])
        
        # check if the arc should be a straight connection
        if self._line_type == self.LINE_TYPE_STRAIGHT:

            # trigonometric calculations to determine the start- and end-positions
            angle = atan2(pos_to[1] - pos_from[1], pos_to[0] - pos_from[0])

	    #print "LINE", pos_to[0], pos_to[1]

            ctx.line_to(pos_to[0], pos_to[1])
            ctx.stroke()

            # calculate position for the label of the arc
            dx = int((pos_to[0] - pos_from[0]) / 2)
            dy = int((pos_to[1] - pos_from[1]) / 2)
            deg_angle = 180 * angle / pi
            if (deg_angle <= -170 or deg_angle >= 170) or (deg_angle >= -10 and deg_angle <= 10):
                dy -= 6
            elif (deg_angle <= 100 and deg_angle >= 80) or (deg_angle <= -100 and deg_angle >= -80):
                dx += 6
            else:
                dx += 6
                dy += 6

            # check if a label needs to be added
            if self._weight != 1:
                # add a label to the arc
                self._add_text_no_adjustment(ctx, [pos_from[0] + dx, pos_from[1] + dy], self._font_label, str(int(self._weight)))

        # check if the arc should be a curved connection
        if self._line_type == self.LINE_TYPE_ARC_LOWER or self._line_type == self.LINE_TYPE_ARC_UPPER:
            # calculate control point for the quadratic curve
            x_q, y_q = self.calculate_control_point(pos_from, pos_to, 45, 45)
            # calculate the angle between the end-position and the control point
            angle = atan2(y_q - pos_to[1], x_q - pos_to[0]) + pi
            # draw curve
            ctx.curve_to(pos_from[0], pos_from[1], x_q, y_q, pos_to[0], pos_to[1])
            ctx.stroke()
            # check if a label needs to be added
            if self._weight != 1:
                # calculate label position for the quadratic curve
                x_q, y_q = self.calculate_control_point(pos_from, pos_to, 10, 10)
                self._add_text(ctx, [x_q, y_q], self._font_label, str(int(self._weight)))

        # set the properties for the standard arrow head
        self._head.length = 10
        self._head.width = 0.4
        self._head.angle = angle
        self._head.position = pos_to
        self._head.color = self._edge
        self._head.draw(ctx)

        ctx.stroke()
