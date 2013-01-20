README:

This is my Proof-of-concept code for a Leap Motion-based mouse controller. It only works on OS X as-is, but if you wanted to rewrite Mouse.py for your OS, it should work fine. This was designed for API 0.7.1.

USAGE:
Operation is as follows:
1)The tilt of your right hand controls mouse movement. If you only use one hand, the program assumes it's your right one.
2) Your left hand controls clicking. Simply extend any finger on your left hand to click down, and fold it back in to click up.
This is a somewhat unintuitive method of operation, but I find that it gives exceptionally better control than the most obvious "point-at-screen" method of mouse control. With this two-handed tilt based mode, it is easy to hit and properly engage small buttons.

CONFIGURATION:
1)Configure your Leap screen from the Leap menu.
2)Copy all prerequisite files into the same directory as PyLeapMouse.py, Mouse.py, LeapFunctions.py, and Geometry.py. This includes Leap.py as well as the proper native library stuff (_LeapPython.so and libLeap.dylib on OS X).
3)Launch the Leap app (if not launched already) and plug in your Leap
4)cd to the directory all this stuff is in and run `python PyLeapMouse.py` (minus quotes)

NOTES:
I hacked this together in a few hours, so it's probably buggy and I doubt the design is anything to write home about. However, I tried to keep the code clean and readable. Let me know if you find any bugs. You can reach me at  will (dot) yager (at) gmail (dot) (what the gmail domain ends in). 
