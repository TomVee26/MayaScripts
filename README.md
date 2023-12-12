# MayaScripts
A collection of various Maya scripts

## TomV_SmoothMesh.py
<img style="float: right" src="https://velebny.net/thumbs/smooth_mesh.jpg">

- Controls the Smooth Mesh properties of multiple objects at once
- Can toggle Smooth Mesh Preview with a keyboard shortcut (handy when not using default shortcuts)
- Remembers Cage/Smooth setting for all objects
- Updates UI with all values from selected objects
- Uses [PyMEL](https://github.com/Lumapictures/pymel), tested with Maya 2024

See more at [velebny.net](https://velebny.net/smooth_mesh.html)

### Installation
- Copy `TomV_SmoothMesh.py` to your Maya scripts folder `C:\Users\<User>\Documents\maya\<version>\prefs\scripts`

#### Shelf
- Create a new shelf item
- Use this code as the Python command:
```
import TomV_SmoothMesh
TomV_SmoothMesh.main()
```
#### Keyboard shortcut for "Toggle Smooth Mesh"
- Open Hotkey Editor
- In the Runtime Command Editor insert this code as the Python command:
```
import TomV_SmoothMesh
TomV_SmoothMesh.toggle_smooth()
```

#### Speed-up
- To make the script launch faster, copy `userSetup.py` into your Maya scripts folder (like above)

### TODO
- Right click on a button to select objects with that value
- Option to set a custom number for smoothing levels
- Move the whole window when click and dragging anywhere in it
