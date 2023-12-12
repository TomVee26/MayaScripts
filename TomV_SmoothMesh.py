import pymel.core as pm

# Store smooth type (cage/smooth) for all objects in a global dict
if 'objs_smooth_vals' not in globals():
    objs_smooth_vals = dict()

# Define UI values
win_name = 'SmoothMesh'
ui_btns = list()
highlightColor = [0.322, 0.522, 0.651]
defaultBG = [0.365, 0.365, 0.365]
frameBG = [0.216, 0.216, 0.216]
win_width = 175
win_height = 50


def get_selected_meshes():
    """Return all selected mesh shapes"""
    return pm.ls(pm.listRelatives(shapes=True, noIntermediate=True, type='mesh'))


def store_smooth_vals():
    """Store last smooth type if used"""
    for obj in get_selected_meshes():
        smooth_val = obj.displaySmoothMesh.get()
        if smooth_val > 0:
            objs_smooth_vals[obj.name()] = smooth_val


def toggle_smooth(*args):
    """Toggle between smoothed and un-smoothed mesh. Last selected object dictates state (on/off)"""
    store_smooth_vals()
    objs = get_selected_meshes()

    if objs:
        obj_last = objs[-1]
        smooth_val_last = obj_last.displaySmoothMesh.get()

        for obj in objs:
            # Smooth on > off
            if smooth_val_last > 0:
                obj.displaySmoothMesh.set(0)

            # Smooth off > on
            else:
                show_smooth(obj)
    update_ui()


def show_smooth(obj):
    """
    Show smoothed mesh, type (cage/smooth) is saved per object
    Arg: Object to show smooth preview
    """
    try:
        # Read last smooth type if exists
        smooth_val = objs_smooth_vals[obj.name()]
    except Exception:
        # Default type is "Smooth"
        smooth_val = 2

    obj.displaySmoothMesh.set(smooth_val)


def display_subdivs(index):
    """
    Display Subdivisions
    Arg: 0,1
    """
    store_smooth_vals()
    for obj in get_selected_meshes():
        obj.displaySubdComps.set(1 - index)
        if obj.displaySmoothMesh.get() == 0:
            show_smooth(obj)
    update_ui()


def set_smooth_type(index):
    """
    Show Smooth Mesh Preview
    Args: 0,1,2 (Off/Cage/Smooth)
    """
    store_smooth_vals()
    pm.displaySmoothness(polygonObject=index + 1)
    update_ui()


def set_preview_level(level):
    """
    Preview Division Levels
    Arg: int for the level to show
    """
    store_smooth_vals()
    for obj in get_selected_meshes():
        obj.smoothLevel.set(level)
        show_smooth(obj)
    update_ui()


def set_render_level(level):
    """
    Render Division Levels
    Arg: int for the level to show
    """
    store_smooth_vals()
    for obj in get_selected_meshes():
        obj.renderSmoothLevel.set(level)
    update_ui()


def use_render_preview(index):
    """
    Use Preview for Rendering
    Arg: 0,1
    """
    store_smooth_vals()
    for obj in get_selected_meshes():
        obj.useSmoothPreviewForRender.set(1 - index)
    update_ui()


def main():
    """Create the main UI"""

    # Destroy window if already exists
    try:
        if pm.window(win_name, exists=True):
            pm.deleteUI(win_name, window=True)
    except Exception:
        pass

    # Define UI templates
    template = pm.uiTemplate('SmoothMeshTemplate', force=True)
    template.define(pm.text, align='left')
    template.define(pm.button, height=25)
    template.define(pm.frameLayout, collapsable=True, backgroundColor=frameBG, collapseCommand=resize_window)
    template.define(pm.rowLayout, margins=5)
    template.define(pm.columnLayout, adjustableColumn=True)

    # UI layout
    with pm.window(win_name, width=win_width, height=win_height, closeCommand=remove_selection_changed_callback):
        with template:
            with pm.columnLayout():
                with pm.frameLayout(label='Preview'):
                    with pm.columnLayout():
                        # Display Subdivisions
                        with pm.rowLayout():
                            pm.text(label='Display Subdivisions:')
                        with pm.horizontalLayout():
                            # Create buttons from an array
                            labels = ['On', 'Off']
                            for index, label in enumerate(labels):
                                btn_id = f'btn_display_subdivs_{index}'
                                ui_btns.append(btn_id)
                                pm.button(btn_id, label=label, command=pm.Callback(display_subdivs, index))

                        # Smooth Mesh Type
                        with pm.rowLayout():
                            pm.text(label='Smooth Mesh Preview:')
                        with pm.horizontalLayout():
                            # Create buttons from an array
                            labels = ['Off', 'Cage', 'Smooth']
                            for index, label in enumerate(labels):
                                btn_id = f'btn_smooth_mesh_{index}'
                                ui_btns.append(btn_id)
                                pm.button(btn_id, label=label, command=pm.Callback(set_smooth_type, index))

                        # Preview Div Levels
                        with pm.rowLayout():
                            pm.text(label='Preview Division Levels:')
                        with pm.horizontalLayout():
                            # Create 1-5 buttons
                            for level in range(5):
                                btn_id = f'btn_preview_lev_{level}'
                                ui_btns.append(btn_id)
                                pm.button(btn_id, label=level, width=10, command=pm.Callback(set_preview_level, level))

                with pm.frameLayout(label='Render', collapse=True):
                    with pm.columnLayout():
                        # Render Div Levels
                        with pm.rowLayout():
                            pm.text(label='Render Division Levels:')
                        with pm.horizontalLayout():
                            # Create 1-5 buttons
                            for level in range(5):
                                btn_id = f'btn_render_lev_{level}'
                                ui_btns.append(btn_id)
                                pm.button(btn_id, label=level, width=10, command=pm.Callback(set_render_level, level))

                        # Use Preview level for Rendering
                        with pm.rowLayout():
                            pm.text(label='Use Preview for Rendering:')
                        with pm.horizontalLayout():
                            # Create buttons from an array
                            labels = ['On', 'Off']
                            for index, label in enumerate(labels):
                                btn_id = f'btn_use_render_preview_{index}'
                                ui_btns.append(btn_id)
                                pm.button(btn_id, label=label, command=pm.Callback(use_render_preview, index))

                with pm.columnLayout(margins=3):
                    pm.button(label='Toggle Smooth Mesh', command=toggle_smooth, height=40)

    # Register selection callback
    add_selection_changed_callback()
    # Update UI when starting with objects selected
    update_ui()
    # Resize UI to default height
    resize_window()


def add_selection_changed_callback():
    """Update UI every time the selection changes"""
    global selection_changed_callback
    selection_changed_callback = pm.scriptJob(event=['SelectionChanged', update_ui])


def remove_selection_changed_callback():
    """Remove callback when window closes"""
    global selection_changed_callback
    if pm.scriptJob(exists=selection_changed_callback):
        pm.scriptJob(kill=selection_changed_callback)


def reset_ui():
    """Remove button highlights from the UI. All buttons are put into an array on their creation"""
    for btn in ui_btns:
        pm.button(btn, edit=True, backgroundColor=defaultBG)


def resize_window():
    """Resize window when expanding or collapsing UI elements"""
    pm.window(win_name, edit=True, height=win_height)


def update_ui(*args):
    """Every time objects are selected, check their properties and update the UI with the collected values"""
    if pm.window(win_name, exists=True):
        objs = get_selected_meshes()
        reset_ui()

        if objs:
            for obj in objs:
                # Get objects properties
                display_subdivs = 1 - int(obj.displaySubdComps.get())
                smooth_mesh = obj.displaySmoothMesh.get()
                preview_lev = obj.smoothLevel.get()
                render_lev = obj.renderSmoothLevel.get()
                use_render_preview = 1 - int(obj.useSmoothPreviewForRender.get())

                # Get corresponding UI buttons
                btn_display_subdivs = f'btn_display_subdivs_{display_subdivs}'
                btn_smooth_mesh = f'btn_smooth_mesh_{smooth_mesh}'
                btn_preview_lev = f'btn_preview_lev_{preview_lev}'
                btn_render_lev = f'btn_render_lev_{render_lev}'
                btn_use_render_preview = f'btn_use_render_preview_{use_render_preview}'

                # Add Ui highlight
                pm.button(btn_display_subdivs, edit=True, backgroundColor=highlightColor)
                pm.button(btn_smooth_mesh, edit=True, backgroundColor=highlightColor)
                pm.button(btn_preview_lev, edit=True, backgroundColor=highlightColor)
                pm.button(btn_render_lev, edit=True, backgroundColor=highlightColor)
                pm.button(btn_use_render_preview, edit=True, backgroundColor=highlightColor)

        else:
            # Remove UI highlights when nothing is selected
            reset_ui()


# TODO: Right click on a button to select objects with that value
# TODO: Option to set a custom number for smoothing levels
# TODO: Move the whole window when click and dragging anywhere in it
