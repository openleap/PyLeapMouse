import sys
if sys.platform == "darwin":
    import OSX.Leap as Leap
    import OSX.Mouse as Mouse
elif 'linux' in sys.platform:
    import Linux.Leap as Leap
    import Linux.Mouse as Mouse
else:
    import Windows.Leap as Leap
    import Windows.Mouse as Mouse
