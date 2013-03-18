#!/usr/bin/python

import copy

import pygtk
import gtk
import cairo

import font

class Component(object):
    """ Parent class for all components of a petri net that defines common properties. """

    def __init__(self):
        """ Constructor of Component and default values will be initialised. """
        self._label = ""
        self._descr = ""
        self._key = ""

        self._x_offset = 0
        self._y_offset = 0
        
        self._font_label = font.Font() #self.default_font()
        self._font_description = font.Font() #self.default_font()

        self._label_pos = [0., 0.]
        self._pos = [0., 0.]
        self._edge = [0., 0., 0.]
        self._fill = [255., 255., 255.]

        self._ctr_inputs = 0
        self._ctr_outputs = 0
        self._limit = 0
        self._limit_inputs = 0
        self._limit_outputs = 0

    @property
    def key(self):
        """ Return the key. """
        return self._key

    @property
    def label(self):
        """ Return the label. """
        return self._label

    @property
    def description(self):
        """ Return the description. """
        return self._descr

    @property
    def font_label(self):
        """ Return the font of the label (Font-Object). """
        return self._font_label

    @property
    def font_description(self):
        """ Return the font of the description (Font-Object). """
        return self._font_description

    @property
    def position(self):
        """ Return the position (x- and y-position as list). """
        return self._pos

    @property
    def rgb_edge(self):
        """ Return the colour of edges (RGB-list). """
        return self._edge

    @property
    def rgb_fill(self):
        """ Return the colour for filling the component (RGB-list). """
        return self._fill

    @property
    def count_inputs(self):
        """ Return number of inputs. """
        return self._ctr_inputs

    @property
    def count_outputs(self):
        """ Return number of outputs. """
        return self._ctr_outputs

    @property
    def x_offset(self):
        """ Return offset in x-direction. """
        return self._x_offset

    @property
    def y_offset(self):
        """ Return offset in y-direction. """
        return self._y_offset

    @property
    def default_font(self):
        """ Return a default font. """
        self.__def_font = font.Font()
        self.__def_font.font = "Arial"
        self.__def_font.slant = cairo.FONT_SLANT_NORMAL
        self.__def_font.weight = cairo.FONT_WEIGHT_NORMAL
        self.__def_font.size = 15
        return self.__def_font

    @key.setter
    def key(self, key):
        """ Set the key. """
        self._key = key

    @label.setter
    def label(self, label):
        """ Set the label. """
        self._label = label

    @description.setter
    def description(self, description):
        """ Set the description. """
        self._descr = description

    @font_label.setter
    def font_label(self, font):
        """ Set the font of the label (Font-Object). """
        self._font_label = font

    @font_description.setter
    def font_description(self, font):
        """ Set the font of the description (Font-Object). """
        self._font_description = font

    @position.setter
    def position(self, pos):
        """ Set the position (x- and y-position as list). """
        self._pos = pos
        for i in range(len(self._pos)):
            if self._pos[i] < 0:
                self._pos[i] = self._pos[i] * -1

    @rgb_edge.setter
    def rgb_edge(self, color):
        """ Set the colour of edges (RGB-list). """
        self._edge = color

    @rgb_fill.setter
    def rgb_fill(self, color):
        """ Set the colour for filling the component (RGB-list). """
        self._fill = color

    @count_inputs.setter
    def count_inputs(self, count):
        """ Set the number of inputs. """
        self._ctr_inputs = count

    @count_outputs.setter
    def count_outputs(self, count):
        """ Set the number of outputs. """
        self._ctr_outputs = count

    @x_offset.setter
    def x_offset(self, offset):
        """ Set the x-offset. """
        self._x_offset = offset

    @y_offset.setter
    def y_offset(self, offset):
        """ Set the y-offset. """
        self._y_offset = offset

    def zoom(self, factor):
        """ Sale the component by a given factor. """
        pass

    #def get_label_position(self):
    #    return self._label_pos

    #def set_label_position(self, position):
    #    self._label_pos = position

    def increase_input_count(self):
        """ Increase the input counter by 1. """
        self._ctr_inputs += 1
        if self._ctr_inputs > self._limit_inputs:
            self._ctr_inputs = self._limit_inputs

    def decrease_input_count(self):
        """ Decrease the input counter by 1. """
        self._ctr_inputs -= 1
        if self._ctr_inputs < 0:
            self._ctr_inputs = 0

    def increase_output_count(self):
        """ Increase the output counter by 1. """
        self._ctr_outputs += 1
        if self._ctr_outputs > self._limit_outputs:
            self._ctr_outputs = self._limit_outputs
        
    def decrease_output_count(self):
        """ Decrease the output counter by 1. """
        self._ctr_outputs -= 1
        if self._ctr_outputs < 0:
            self._ctr_outputs = 0

    def is_equal(self, component):
        """ Check if the current component is equal with the given one. """
        return self._key == component.key

    def draw(self, ctx = None):
        """ Draw the arrow head onto the defined GraphicsContext ctx. """
        pass

    def clone(self):
        """ Duplication of the current component and the duplicate will be returned. """
        comp = Component()
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
        return comp

    def _add_text(self, ctx, pos, f, text, limit = None):
        """ Add text to the defined GraphicsContext under regarding the estimated width and height of the text. The position is the centre of the text and the style is defined through the font f. """
        # NoneType issue!
        #if f != None:
        # definition of the font style through the font object
        ctx.select_font_face(f.font, f.slant, f.weight)
        # estimate width and height of the text
        xbearing, ybearing, width, height, xadvance, yadvance = ctx.text_extents(str(text))
        # calculate new positions
        new_x = int(pos[0] - width / 2)
        new_y = int(pos[1] + height / 2)
        # check if the positions are valid
        if new_x >= 0 and new_y >= 0:
            # print text
            ctx.move_to(new_x, new_y)
            # NoneType issue!
            #if font != None:
            ctx.set_font_size(f.size)
            ctx.show_text(str(text))

    def _add_text_no_adjustment(self, ctx, pos, f, text, limit = None):
        """ Add text to the defined GraphicsContext without regarding the estimated width and height of the text. The position is the centre of the text and the style is defined through the font f. """
        # definition of the font style through the font object
        ctx.select_font_face(f.font, f.slant, f.weight)
        # print text
        ctx.move_to(pos[0], pos[1])
        ctx.set_font_size(f.size)
        ctx.show_text(str(text))

    def _get_colour(self, r = 0., g = 0., b = 0.):
        """ Convert three single colour channel values into a RGB-list with valid values between 0 and 255. """
        if r < 0 or r > 255:
            r = 0
        if g < 0 or g > 255:
            g = 0
        if b < 0 or b > 255:
            b = 0
        return [r, g, b]
