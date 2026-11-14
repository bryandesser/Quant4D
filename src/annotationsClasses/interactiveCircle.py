from matplotlib.backend_tools import Cursors
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_bases import MouseEvent
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import numpy as np

class InteractiveCircle(qtc.QObject):
    """
    Generate one or more circles with which the user can interact

    center:         (x,y) point pair defining the center of the circle(s)
    radius:         (n,) float/int defining the radius of any/all circle(s) in axis units
    axis:           matplotlib.axes._subplots.AxesSubplot (i.e. self.Fig[id].ax)
    color:          matplotlib color specs (https://matplotlib.org/stable/tutorials/colors/colors.html)
    interactions:   'all'           radius and center can be changed (default)
                    'resize'        only radius can be changed, center is locked
                    'translate'     only center can be changed, radius is locked
                    'none'          no user modifications allowed
    """
    updateCircle = qtc.pyqtSignal()
    rightClick = qtc.pyqtSignal(MouseEvent)

    lock = None # only one InteractiveCircle can be interactived with at a time

    def __init__(self, axis, center=None, radius=None, color='r', interactions='all'):
        super().__init__()

        # set defaults for center and radius if none are provided
        

        # properties
        self.x = np.cos(2 * np.pi * np.arange(0.0, 1.01, 0.01))     # keep basic circle on hand for convenience
        self.y = np.sin(2 * np.pi * np.arange(0.0, 1.01, 0.01))     #
        self.center = np.array(center)                              # force conversion to array; accepts tuple or list input
        self.radius = np.array([radius]).flatten()                  # force conversion to array; accepts scalar, tuple, or list input
        self.transform = None                                       # defines the current user interaction
        self.selectedPoint = None                                   # reference to the selected point
        self.press = None                                           # passes along artist information between on_press and on_motion
        self.color = color                                          # annotation color
        self.interactions = interactions                            # allowed interactions, defined above

        # plot circle(s) based on provided radius/radii
        self.circ = axis.plot(self.x[:,None]*self.radius[None,:] + self.center[0],self.y[:,None]*self.radius[None,:] + self.center[1],color = color)

        # plot point at each radius, if more than one present
        self.point = axis.scatter(self.center[0]+self.radius,self.center[1].repeat(self.radius.size),color = color)

        # hide any intermediate points, only keeping first and last visible
        sz = np.zeros_like(self.radius)
        sz[0] = sz[-1] = self.point.get_sizes()
        self.point.set_sizes(sz)

        # points are only needed for resizing
        if interactions in ["none","translate"]:
            self.point.set_visible(False)
        
        # shortcuts
        self.canvas = self.circ[0].figure.canvas
        self.axis = self.circ[0].axes

        # annotations are animated for quick blitting
        for circ in self.circ:
            circ.set_animated(True)
        self.point.set_animated(True)
        
        # update axis with new annotations
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(axis.bbox)

    def containsArtist(self,event):
        """
        this funciton decides whether or not the current mouseevent
        includes any artists (circles or points),

        input:      event -> matplotlib.backend_bases.MouseEvent

        events are connected through InteractiveCircle.connect():
                        - button_press_event
                        - button_release_event
                        - motion_notify_event
        
        return:     (containsPoint,contains) -> (bool,bool), where:
                        - containsPoint is True if the curosr has selected
                            or hovered over any points
                        - contains is True if the cursor has selected
                            or hovered over any circles or points, including
                            within the circle with the largest radius
        """
        containsCirc=[]
        for iCirc in self.circ:
            c,_ = iCirc.contains(event)
            containsCirc.append(c)

        # is a circle included?
        if (True in containsCirc):
            containsCirc = True
        else:
            containsCirc = False
        
        # is a point included? if more than one and no current selectedPoint, select the last one in the list
        containsPoint,attrd = self.point.contains(event)
        if (containsPoint) and (self.selectedPoint == None):
            self.selectedPoint = attrd["ind"][-1]
        
        if event.name == "motion_notify_event" and InteractiveCircle.lock == None:
            self.selectedPoint = None

        # are any artists included in the click?
        contains = containsCirc or containsPoint

        # check if press is within the radius of the outer circle (i.e. not ON the circle)
        if (np.linalg.norm((event.xdata,event.ydata)-self.center)<=self.radius[-1]) and (self.interactions in ["all","translate"]):
            contains = True
        
        return containsPoint,contains
    
    def remove(self):
        ''' remove all circle(s) and points(s) from axes '''
        for circ in self.circ:
            circ.remove()
        self.point.remove()

    def connect(self):
        ''' connect to all the MouseEvents we need '''
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def pointVisibility(self):
        # in case self.interactions is changed programmatically, monitor point visibility
        if (self.interactions in ["all","resize"]) and (self.point.get_visible()==False):
            self.point.set_visible(True)
        elif (self.interactions in ["none","translate"]) and (self.point.get_visible()==True):
            self.point.set_visible(False)
            self.restoreBackground()

    def on_press(self, event):
        """
        user pressed mouse button
        event -> matplotlib.backend_bases.MouseEvent of type 'button_press_event'
        """

        # allow for context menu popups
        if event.button == MouseButton.RIGHT:
            self.rightClick.emit(event)
            return

        # monitor point visibility
        self.pointVisibility()
        
        # exit if no interactions allowed, press is not in the axes, or another circle is being interacted with
        if self.interactions == "none": return
        if event.inaxes != self.axis: return
        if InteractiveCircle.lock is not None: return

        # update center and radii
        self.center = np.mean(self.circ[0]._xy[:-1],axis=0)
        for ii in range(len(self.circ)):
            self.radius[ii] = np.mean(np.linalg.norm(self.circ[ii]._xy-self.center,axis=1))
        
        # check that mouse press contains the outer circle
        containsPoint,contains = self.containsArtist(event)

        # if the click is not on or in the artist, exit now
        if not contains:
            # reset selected point to None
            self.selectedPoint = None
            return
        
        # check if the user has clicked on/near the point
        if (self.interactions in ["all","resize"]) and (containsPoint): # only change to the HAND pointer if resizing is allowed
            self.transform = 'resize'
            self.canvas.set_cursor(Cursors.HAND)

        elif self.interactions in ["all","translate"]: # only translation allowed
            self.transform = 'translate'
            self.canvas.set_cursor(Cursors.MOVE)

        else: #no interactions allowed
            self.canvas.set_cursor(Cursors.POINTER)
            self.transform = None
        
        # save info to the self.press 
        self.press = [circ._xy for circ in self.circ], self.point.get_offsets(), (event.xdata, event.ydata)

        # block any other InteractiveCircle interactions
        InteractiveCircle.lock = self

        # draw everything but the artists and store the pixel buffer
        for circ in self.circ:
            circ.set_animated(True)
        self.point.set_animated(self.point.get_visible())
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)

        # now redraw the circle(s) and point(s) 
        for circ in self.circ:
            self.axis.draw_artist(circ)
        if self.point.get_visible():
            self.axis.draw_artist(self.point)

        # and blit just the redrawn area
        self.canvas.blit(self.axis.bbox)

    def on_motion(self, event):
        """
        user moving mouse, either dragging after a press, or just hovering
        event -> matplotlib.backend_bases.MouseEvent of type 'motion_notify_event'
        """

        # monitor point visibility
        self.pointVisibility()
        
        # exit if no interactions allowed, press is not in the axes
        if self.interactions == "none": return
        if event.inaxes != self.axis: return

        # are any artists under the mouse?
        containsPoint,contains = self.containsArtist(event)
        
        # check if the user has clicked on/near the point or the circle
        if (contains) and (self.interactions in ["all","resize"]) and (containsPoint):
            self.canvas.set_cursor(Cursors.HAND)
        elif (contains) and (self.interactions in ["all","translate"]):
            self.canvas.set_cursor(Cursors.MOVE)
        else:
            self.canvas.set_cursor(Cursors.POINTER)
        
        # if no press event has happened, quit now
        if InteractiveCircle.lock is not self:
            return
        
        # get artist info from the initial mouse press event
        circData, ptData, (xpress, ypress) = self.press

        # get mouse movement vector from event and press location
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        # if the user is attempting a translation and that is allowed, update circle(s) and point(s) locations
        if (self.transform == 'translate') and (self.interactions in ["all","translate"]):
            
            # move circle(s) by (dx,dy)
            for ii in range(len(self.circ)):
                self.circ[ii].set_xdata(circData[ii][:,0]+dx)
                self.circ[ii].set_ydata(circData[ii][:,1]+dy)
            
            # move point(s) by (dx,dy)
            self.point.set_offsets(ptData+(dx,dy))
            
            # update center by (dx,dy)
            self.center = np.mean(self.circ[0]._xy[:-1],axis=0)
        
        # if the user is attempting a resize and that is allowed, update point(s) locations and circle(s) radius
        elif (self.transform == 'resize') and (self.interactions in ["all","resize"]) and (self.selectedPoint != None):
            
            # only update location of the selected point
            ptDelta = np.zeros(shape=self.point.get_offsets().shape)
            ptDelta[self.selectedPoint,:] += (dx,dy)
            
            # update radius
            self.radius = np.linalg.norm(ptData+ptDelta-self.center,axis=1)

            # if more than 2 circles are included, the intermediate circle radii should be
            # automatically scaled between the inner/outermost circles
            self.radius = np.linspace(self.radius[0],self.radius[-1],self.radius.size)
            
            # move point on axes
            #self.point.set_offsets(ptData+ptDelta) #TODO
            # keep points in the same relative position on the circle, only scale radius
            vec = ptData+ptDelta-self.center
            vec /= np.linalg.norm(vec,axis=1)[:,None]
            self.point.set_offsets(vec*self.radius[:,None] + self.center)
            
            # update corresponding circle radius
            for ii in range(len(self.circ)):
                self.circ[ii].set_xdata(self.x*self.radius[ii]+self.center[0])
                self.circ[ii].set_ydata(self.y*self.radius[ii]+self.center[1])

        # restore pixels that were behind any moved artists
        self.restoreBackground()

        # emit pyqtSignal to main program so these updates can be reflected in the UI components and images
        self.updateCircle.emit()

    def on_release(self, event):
        """
        user released mouse button
        event -> matplotlib.backend_bases.MouseEvent of type 'button_release_event'
        """
        
        # exit if no interactions allowed or another circle is being interacted with
        if self.interactions == "none": return
        if InteractiveCircle.lock is not self: return

        # reset interaction parameters
        self.press = None
        self.selectedPoint = None
        self.transform = None
        InteractiveCircle.lock = None

        # update cursor
        _,contains = self.containsArtist(event)
        if not contains: self.canvas.set_cursor(Cursors.POINTER)

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        for circ in self.circ:
            circ.set_animated(False)

        # redraw the full figure
        self.canvas.draw()

        # reorder circles and points if user drags inner beyond outer, or vice versa
        if not (np.diff(self.radius)>0).all():
            sortIdx = np.argsort(self.radius)
            self.circ = [self.circ[idx] for idx in sortIdx]
            self.point.set_offsets(self.point.get_offsets()[sortIdx,:])
            self.radius = self.radius[sortIdx]
            

    def redraw(self):
        """ in the case where center/radius are updated externally, redraw all point(s) and circle(s) """

        # keep points in the same relative position on the circle, only scale radius
        vec = self.point.get_offsets()-np.mean([circ._xy[:-1] for circ in self.circ],axis=1)
        vec /= np.linalg.norm(vec,axis=1)[:,None]
        self.point.set_offsets(vec*self.radius[:,None] + self.center)
        
        # update circle data with new radius information
        for ii in range(len(self.circ)):
            self.circ[ii].set_xdata(self.radius[ii]*self.x+self.center[0])
            self.circ[ii].set_ydata(self.radius[ii]*self.y+self.center[1])
        
        # reblit
        self.restoreBackground()

    def restoreBackground(self):
        """ this function is used to restore background for blitting """

        # monitor point visibility
        self.pointVisibility()

        # restore the background region
        self.canvas.restore_region(self.background)

        # redraw just the current rectangle
        for circ in self.circ:
            self.axis.draw_artist(circ)
        if self.point.get_visible():
            self.axis.draw_artist(self.point)

        # blit just the redrawn area
        self.canvas.blit(self.axis.bbox)

    def updateBackground(self):
        """ this function is used to redraw artists and update background for blitting """

        # draw everything but the selected circle and store the pixel buffer
        for circ in self.circ:
            circ.set_animated(True)
        self.point.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axis.bbox)

        # now redraw the circle(s) and point(s)
        for circ in self.circ:
            self.axis.draw_artist(circ)
        if self.point.get_visible():
            self.axis.draw_artist(self.point)

        # and blit just the redrawn area
        self.canvas.blit(self.axis.bbox)
