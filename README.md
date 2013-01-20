README:

This is my Proof-of-concept code for a Leap Motion-based mouse controller. It only works on OS X as-is, but if you wanted to rewrite Mouse.py for your OS, it should work fine. This was designed for API 0.7.1.

USAGE:
Operation is as follows:
One hand in frame: The tilt of this hand moves the mouse.
Two hands in frame: Left hand controls action.
    All fingers closed: Mouse movement with right hand tilt.
    One finger open: Clicking. Left mouse button is down. Mouse movement with right hand tilt.
    Two fingers open: Scrolling. Scrolling with right hand movement.

This is a somewhat unintuitive method of operation, but I find that it gives exceptionally better control than the most obvious "point-at-screen" method of mouse control. With this two-handed tilt based mode, it is easy to hit and properly engage small buttons, scroll through webpages, etc.

CONFIGURATION:
1)Configure your Leap screen from the Leap menu.
2)Copy all prerequisite files into the same directory as PyLeapMouse.py, Mouse.py, LeapFunctions.py, and Geometry.py. This includes Leap.py as well as the proper native library stuff (_LeapPython.so and libLeap.dylib on OS X).
3)Launch the Leap app (if not launched already) and plug in your Leap
4)cd to the directory all this stuff is in and run `python PyLeapMouse.py` (minus quotes)

NOTES:
I hacked this together in a few hours, so it's probably buggy and I doubt the design is anything to write home about. However, I tried to keep the code clean and readable. Let me know if you find any bugs. You can reach me at  will (dot) yager (at) gmail (dot) (what the gmail domain ends in). 
