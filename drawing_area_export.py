#!/usr/bin/python

import pygtk
import gtk
import cairo

class DrawingAreaExport(object):
    """ The DrawingAreaExport class is used to exports the content of it into different formats. """

    _drawing_area = None
    _path = None

    def __init__(self):
        # initialises default values
        self._drawing_area = None
        self._path = None

    @property
    def drawing_area(self):
        """ Return drawing area (gtk.DrawingArea-Object). """
        return self._drawing_area

    @property
    def path(self):
        """ Return output path. """
        return self._path

    @drawing_area.setter
    def drawing_area(self, area):
        """ Set drawing area (gtk.DrawingArea-Object). """
        self._drawing_area = area

    @path.setter
    def path(self, p):
        """ Set output path. """
        self._path = p

    def export_as_pdf(self):
        """ Export the content shown in the drawing area as PDF. """
        # check if a path is defined
        if self._path != None:
            # read width and height
            width = self._drawing_area.get_allocation()[2]
            height = self._drawing_area.get_allocation()[3]
            # get GraphicsContext
            ctx = self._drawing_area.window.cairo_create()
            # create surface and export the created surface
            drawable_surface = ctx.get_target()
            surface = cairo.PDFSurface(self._path, width, height);
            cairo_ctx = cairo.Context(surface)
            cairo_ctx.set_source_surface(drawable_surface, 0, 0)
            cairo_ctx.paint()
            cairo_ctx.show_page()

    def export_as_ps(self):
        """ Export the content shown in the drawing area as PS. """
        # check if a path is defined
        if self._path != None:
            # read width and height
            width = self._drawing_area.get_allocation()[2]
            height = self._drawing_area.get_allocation()[3]
            # get GraphicsContext
            ctx = self._drawing_area.window.cairo_create()
            # create surface and export the created surface
            drawable_surface = ctx.get_target()
            surface = cairo.PSSurface(self._path, width, height);
            cairo_ctx = cairo.Context(surface)
            cairo_ctx.set_source_surface(drawable_surface, 0, 0)
            cairo_ctx.paint()
            cairo_ctx.show_page()

    def export_as_svg(self):
        """ Export the content shown in the drawing area as SVG. """
        # check if a path is defined
        if self._path != None:
            # read width and height
            width = self._drawing_area.get_allocation()[2]
            height = self._drawing_area.get_allocation()[3]
            # get GraphicsContext
            ctx = self._drawing_area.window.cairo_create()
            # create surface and export the created surface
            drawable_surface = ctx.get_target()
            surface = cairo.SVGSurface(self._path, width, height);
            cairo_ctx = cairo.Context(surface)
            cairo_ctx.set_source_surface(drawable_surface, 0, 0)
            cairo_ctx.paint()
            cairo_ctx.show_page()

    def export_as_png(self):
        """ Export the content shown in the drawing area as PNG. """
        # check if a path is defined
        if self._path != None:
            # read width and height
            width = self._drawing_area.get_allocation()[2]
            height = self._drawing_area.get_allocation()[3]
            # get GraphicsContext
            ctx = self._drawing_area.window.cairo_create()
            # create surface and export the created surface
            drawable_surface = ctx.get_target()
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            surface.write_to_png(self._path)

    def export_as_jpg(self):
        """ Export the content shown in the drawing area as JPG. """
        # get properties of drawing area
        drawable = self._drawing_area.window
        colormap = drawable.get_colormap()
        # create gtk.gdk.Pixbuf which is used to save the content as an image
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, *drawable.get_size())
        pixbuf = pixbuf.get_from_drawable(drawable, colormap, 0,0,0,0, *drawable.get_size())
        pixbuf.save(self._path, 'jpeg')
