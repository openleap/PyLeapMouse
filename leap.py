import sys
if sys.platform == "darwin":
    import OSX.Leap as Leap
    import OSX.Mouse as Mouse
    from OSX.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
elif 'linux' in sys.platform:
    import Linux.Leap as Leap
    import Linux.Mouse as Mouse
    from Linux.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
else:
    import Windows.Leap as Leap
    import Windows.Mouse as Mouse
    from Windows.Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
