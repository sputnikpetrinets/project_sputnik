#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo
import math

import place
import transition
import arc
import inhibitory_arrow_head
import arrow_head

from math import pi
from math import atan2
from math import atan
from math import cos
from math import sin
from math import tan

class InhibitoryArc(arc.Arc):

    _head = inhibitory_arrow_head.InhibitoryArrowHead()

    def __init__(self):
        super(InhibitoryArc, self).__init__()
        self._head = inhibitory_arrow_head.InhibitoryArrowHead()

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
                x_q, y_q = self.calculate_control_point(self._origin.position, self._target.position, 75, 75)
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

    def get_position_place(self, component, offset, alpha, is_origin, is_straight_line):
        """ Calculate the true position on the circle for a connection with an arc. The component defines the type and delivers the needed information about the place, control_point defines the control point position, alpha is the angle between the two components, is_origin is TRUE if the place is the origin of the arc and is_straight_line is TRUE when the connection should be a straight one. """

        # initial position
        pos = [0, 0]
        # check the if the component is really a place
        if type(component) == place.Place:
            # calculate the offset (head)
            radius_offset = 2 * self._head.radius
            if is_origin:
                radius_offset = 0
            
            if not is_straight_line: 
                # calculate the offset values for each dimension to determine the true connection point
                new_alpha = atan2(offset[1] - component.position[1], offset[0] - component.position[0])
                dx = (component.radius + radius_offset) * cos(new_alpha)
                dy = (component.radius + radius_offset) * sin(new_alpha)
                # adapt the component position
                if is_origin:
                    pos = [component.position[0] + dx, component.position[1] + dy]
                else:
                    pos = [component.position[0] + dx, component.position[1] + dy]
            else:
                # calculate the offset values for each dimension to determine the true connection point
                dx = (component.radius + radius_offset) * cos(alpha)
                dy = (component.radius + radius_offset) * sin(alpha)
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
            dx = int(component.dimension[0] / 2) + self._head.radius
            dy = 0
            d = component.dimension[1] / 9

            # determine the type of connection and determine the y-offset
            if self._target != None:
                if self._target.is_equal(component):
                    dy = 4*d
                else:
                    dy = 3*d
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
        comp = InhibitoryArc()
        # general arc/component properties
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
        comp.line_type = self.line_type
        # inhibitory arc specific properties
        comp.weight = self.weight
        comp.origin = self.origin.clone()
        comp.target = self.target.clone()
        # return duplicate
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
            ctx.line_to(pos_to[0], pos_to[1])
            ctx.stroke()

            # calculate positions for the label of the arc
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
            x_q, y_q = self.calculate_control_point(pos_from, pos_to, 95, 95)
            # calculate the angle between the end-position and the control point
            angle = atan2(y_q - pos_to[1], x_q - pos_to[0]) + pi
            # draw curve
            x2 = pos_to[0]
            if pos_to[0] < pos_from[0]:
                x2 += self._head.radius
            else:
                x2 -= self._head.radius
            y2 = pos_to[1]
            ctx.curve_to(pos_from[0], pos_from[1], x_q, y_q, x2, y2)
            ctx.stroke()
            # check if a label needs to be added
            if self._weight != 1:
                # calculate label position for the quadratic curve
                x_q, y_q = self.calculate_control_point(pos_from, pos_to, 55, 55)
                self._add_text(ctx, [x_q, y_q], self._font_label, str(int(self._weight)))

            ctx.move_to(*pos_to)

        # set the properties for the inhibitory arrow head
        self._head.length = 8
        self._head.angle = angle
        self._head.position = pos_to
        self._head.color = self._edge
        self._head.draw(ctx)

        ctx.stroke()

