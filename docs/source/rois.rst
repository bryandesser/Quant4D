.. _rois:

ROIs
----
By default, Quant4D uses all real space probe positions to generate a
diffraction pattern; however, the user can specify a region of interest (ROI)
on any real space image to generate a local diffraction pattern. This is done
in the **Real-space ROI** panel of the main UI. 

* **Full image** - default, uses all real space probe positions.
* **Point** - used to visualize individual diffraction patterns.
* **Ellipse** - defaults to a circle
* **Rectangle** - defaults to a square
* **Draw Polygon** - prompts the user to select a real-space image for initial
  drawing. The user clicks as many vertices as desired until finally finishing
  the polygon by clicking on the initial vertex or double clicking anywhere in
  the image. 
* **From File** - 

`Point`_, `Ellipse`_, `Rectangle`_, and `Polygon`_ ROIs generate interactive
annotations on *all* real space images, whether or not all images are
displayed. All annotations are synced across images, allowing the user to
interact with them on whichever image is most convenient.

Ellipse and Rectangle ROIs can be resized, translated, and rotated. Their aspect
ratio can be fixed by right clicking on the annotation and selecting "Fix
Aspect Ratio".

Additional vertices can be added to Polygon ROIs by right clicking on the
polygon line and selecting "Add Vertex". Vertices can be removed by right
clicking on the vertex and selecting "Delete Vertex".

If any ROI is deleted (right click, "Delete ROI"), the UI reverts to using all
probe positions. 

.. _Point : https://mathworks.com/help/images/ref/images.roi.point.html
.. _Ellipse : https://mathworks.com/help/images/ref/images.roi.ellipse.html
.. _Rectangle : https://mathworks.com/help/images/ref/images.roi.rectangle.html
.. _Polygon : https://mathworks.com/help/images/ref/images.roi.polygon.html

.. video:: ../_static/rois.mp4
    :width: 100%
    :autoplay: