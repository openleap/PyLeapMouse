README:

This is my Proof-of-concept code for a Leap Motion-based mouse controller. It only works on OS X as-is, but if you wanted to rewrite Mouse.py for your OS, it should work fine. This was designed for API 0.7.1.

USAGE WITH FINGER MODE (python PyLeapMouse.py --finger) (default):
Operation is as follows:
1)Insert your hand into frame.
2)The forwardmost finger that the program detects is the mouse finger. Where it points, the cursor goes.
3)Stick your thumb out (see note) to click down, and fold your thumb in to click up.
4)Using two pointer fingers (e.g. index and middle) goes into scroll mode, which is not very intuitive but shows how it might work. The fingertips must be within a short distance of each other to activate scroll mode.

(note) The Leap software at the moment (v0.7.1) is a little iffy about detecting thumbs, and it helps to keep your arm straight out in front of you. It takes a little practice to figure out how to hold your thumb correctly. You may want to un-comment some debug prints to help you figure out when Leap thinks you have your thumb out. Apparently 0.7.3 has better thumb detection, but it is not available at the time of writing.

USAGE WITH PALM MODE (python PyLeapMouse.py --palm):
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

The contents of the files are as follows:

PyLeapMouse.py: The actual program

FingerControl.py: Pointer-finger-control specific code
PalmControl.py: Palm-tilt-control specific code

Leap.py: Python-leap bindings (not my code)
_LeapPython.so and libLeap.dylib: Leap libraries (not my code)

Geometry.py: Geometric functions
MiscFunctions.py: Things that aren't strictly geometry and aren't specific to any interface style

Mouse.py: OS-Specific mouse commands (ideally the only OS-specific file). Subject to rapid change.

README.md: You are here