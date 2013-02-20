This is wyager's Proof-of-concept code for a Leap Motion-based mouse controller. It now works with both OS X and Windows.  

The most recent version is on Github at github.com/openleap/pyleapmouse.  

CONFIGURATION:  
1)Launch the Leap app (if not launched already) and plug in your Leap  
2)If you have not done so already, Configure your Leap screen from the Leap menu.  
3)`cd` to the directory all this stuff is in and run `python PyLeapMouse.py` (minus quotes) or just double-click PyLeapMouse.py if you have your computer configured to launch .py files.  
4)If your OS or Python 2.7 installation (i.e. x86 vs x86_64) is not compatible with the Leap Library files included in OSX/ or Windows/, you may need to copy the library files from your Leap SDK folder into your OSX or Windows folder.  
5)Launch with the --palm argument to run in palm mode (with much more accurate two-handed control).  

USAGE WITH FINGER MODE (python PyLeapMouse.py --finger) (default):  
Operation is as follows:  
1)Insert your hand into frame.  
2)The forwardmost finger that the program detects is the mouse finger. Where it points, the cursor goes.  
3)Stick your thumb out (see note) to click down, and fold your thumb in to click up.  
4)Using two pointer fingers (e.g. index and middle) goes into scroll mode, which is not very intuitive but shows how it might work. The fingertips must be within a short distance of each other to activate scroll mode.  

USAGE WITH PALM MODE (python PyLeapMouse.py --palm):  
Operation is as follows:  
One hand in frame: The tilt of this hand moves the mouse.  
Two hands in frame: Left hand controls action.  
    All fingers closed: Mouse movement with right hand tilt.  
    One finger open: Clicking. Left mouse button is down. Mouse movement with right hand tilt.  
    Two fingers open: Scrolling. Scrolling with right hand movement.  

This is a somewhat unintuitive method of operation, but I find that it gives exceptionally better control than the most obvious "point-at-screen" method of mouse control. With this two-handed tilt based mode, it is easy to hit and properly engage small buttons, scroll through webpages, etc.  

NOTES:  
This is a spare-time project, so it's not perfect quality. However, I tried to keep the code clean and readable. Let me know if you find any bugs (which there are certainly at least a few of). You can reach me at  will (dot) yager (at) gmail (dot) (what the gmail domain ends in).  

The contents of the files are as follows:  

PyLeapMouse.py: The actual program  

FingerControl.py: Pointer-finger-control specific code  
PalmControl.py: Palm-tilt-control specific code  

OSX/Windows:  
    Various OS-specific Leap library files  
    Mouse.py: A set of generic commands and classes to abstract away from OS-Specific mouse commands  

Geometry.py: Geometric functions  
MiscFunctions.py: Things that aren't strictly geometry and aren't specific to any interface style  

README.md: You are here