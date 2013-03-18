#!/usr/bin/python

import pygtk
import gtk

import view

class ViewDrawingArea(gtk.ScrolledWindow, view.View):
    """ The ViewDrawingArea class is a specific view that inherits from the general View class and is used to create custom drawing area which is specificly designed to nest it into another view or as a standalone GUI. Additionally the class inherits from gtk.ScrolledWindow to allow the creation of a scrollable drawing area. """

    _start_pos = []

    def __init__(self):
        """ Constructor of ViewDrawingArea and default values will be initialised. """

        # call constructor of parent classes
        gtk.ScrolledWindow.__init__(self)
        view.View.__init__(self)

        # set default values
        self._start_pos = []

    def __init__(self, model = None, controller = None):
        """ Constructor of ViewDrawingArea and default values will be initialised. """

        # call constructor of parent classes
        gtk.ScrolledWindow.__init__(self)
        view.View.__init__(self, model, controller)

        # set default values
        self._start_pos = []
    
    def update(self):
        """ Interface to notify MVCObserver objects about a general data change. """
        self.refresh()

    def reset(self):
        """ Interface to notify MVCObserver objects about a reset event. """
        self._controller.reset()
        self.refresh()

    def update_component(self, key):
        """ Interface to notify Observer objects about a data change of a component. """
        pass

    def update_output(self):
        """ Interface to notify Observer objects about a data change of simulation results. """
        pass

    def undo(self):
        """ Interface to notify Observer objects about an undo. """
        pass

    def show(self):
        """ Interface to create and display the GUI on the screen. """

        # instantiation of a gtk.DrawingArea object with a default size of 900x600
        self._drawing_area = gtk.DrawingArea()
	self._drawing_area.size(900, 600)

        # set the events of the drawing area
        self._drawing_area.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.ENTER_NOTIFY_MASK | gtk.gdk.BUTTON_PRESS_MASK | 
                                      gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)
        self._drawing_area.connect("expose-event", self._update_drawing_area)
        self._drawing_area.connect("button-press-event", self._button_press_event)
        self._drawing_area.connect("motion-notify-event", self._motion_notify_event)
        self._drawing_area.connect("button-release-event", self._button_release_event)
        self._drawing_area.connect("leave-notify-event", self._leave_notify_event)
        self._drawing_area.connect("enter-notify-event", self._enter_notify_event)
        
        # instantiation of a gtk.Viewport object
        self._viewport = gtk.Viewport()
	self._viewport.connect("expose-event", self._update_drawing_area)
        self._viewport.add(self._drawing_area)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self._viewport)

        # assign the drawing area to the controller of the view
        if self._controller != None:
            self._controller.drawing_area = self._drawing_area

    def refresh(self):
        """ Refresh the drawing area. """
        ctx = self._drawing_area.window.cairo_create()
        # check if a GraphicsContext could be determined
        if ctx != None:
            # redraw drawing area
            self._model.data.draw(ctx)
            ctx.stroke()
            # clear buffer
            gtk.gdk.flush()
            ctx.clip()

    def _update_drawing_area(self, widget, event):
	""" Update drawing area in case of a defined event. """
        ctx = self._drawing_area.window.cairo_create()
        self._model.data.draw(ctx)
        ctx.clip()

    def _button_press_event(self, widget, event):
        """ Forward button-press-event to the controller. """
        # position within the drawing area
        self._start_pos = [event.x, event.y]
        # forward command
        self._controller.button_press([event.x, event.y], event)
        # refresh drawing area
        self.refresh()

    def _button_release_event(self, widget, event):
        """ Forward button-release-event to the controller. """
        # forward command
        self._controller.button_release([event.x, event.y])
        # refresh drawing area
        self.refresh()
        
    def _motion_notify_event(self, widget, event):
        """ Forward motion-motion-notify-event to the controller. """
        ctx = self._drawing_area.window.cairo_create()
        # determine current position
        position = []
        if event.is_hint:
            x, y, state = event.window.get_pointer()
            position = [x, y]
        else:
            position = [event.x, event.y]  
        # forward command
        self._controller.motion_notify(position, ctx)
       
    def _leave_notify_event(self, widget, event):
        """ Forward event that ocurres if the mouse leaves the drawing area to the controller. """
        self._controller.leave_drawing_area()

    def _enter_notify_event(self, widget, event):
        """ Forward event that ocurres if the mouse enters the drawing area to the controller. """
        self._controller.enter_drawing_area()
