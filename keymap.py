import bpy

keymap = None

def register():
    global keymap

    wm = bpy.context.window_manager
    keymap = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type='VIEW_3D')

    keymap.keymap_items.new("scene.previous_slide", type='F7', value='PRESS')
    keymap.keymap_items.new("scene.next_slide", type='F8', value='PRESS')

def unregister():
    global keymap

    wm = bpy.context.window_manager
    wm.keyconfigs.addon.keymaps.remove(keymap)
