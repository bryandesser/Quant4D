.. _rois:

Real-Space ROIs
===============

Real-space Region-of-Interest (ROI) selection allows you to restrict the
diffraction pattern to frames from a chosen sub-region of the scan.  Only
frames within the ROI contribute to the displayed diffraction pattern.

ROI types
---------

- **Full** — all frames (default)
- **Point** — single frame at (FrameX, FrameY)
- **Rectangle** — drag inside to move, a corner handle to resize (the opposite
  corner stays put), and the handle on the stalk to rotate
- **Ellipse** — drag inside to move; each of the two handles sits at the end of a
  semi-axis: dragging it sets that semi-axis and turns the ellipse towards the cursor
- **Polygon** — click to place vertices, click the first vertex to close it
  (``Esc`` cancels).  When more than one real-space image is shown you are asked
  which one to draw on.  Afterwards drag a vertex to move it, or drag inside to
  move the polygon
- **File** — load a boolean mask from a file

The mask can be **inverted** using the Invert ROI button, selecting all frames
*outside* the drawn region instead.

Usage
-----

1. Select the desired ROI type from the Real-space ROI dropdown in the main
   window.
2. If drawing a shape, an interactive annotation appears on the real-space image
   window.  Drag to position and resize.
3. The diffraction pattern updates live as the ROI is moved.

.. note::
   Full walkthrough with screenshots will be added in a future documentation
   update.
