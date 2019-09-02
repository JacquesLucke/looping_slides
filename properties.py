import bpy
from bpy.props import *

class SlideData(bpy.types.PropertyGroup):
    start_frame: IntProperty(
        name="Start Frame",
        min=0,
    )

    end_frame: IntProperty(
        name="End Frame",
        min=0,
    )

    camera: PointerProperty(
        name="Camera",
        type=bpy.types.Object,
    )

    def is_set(self, context):
        return (context.scene.frame_start == self.start_frame
                and context.scene.frame_end == self.end_frame)

    def is_playing(self, context):
        return context.screen.is_animation_playing and self.is_set(context)

class LoopingSlidesSettings(bpy.types.PropertyGroup):
    slides: CollectionProperty(type=SlideData)

    switch_to_camera_view: BoolProperty(name="Switch to Camera View")

def register():
    bpy.types.Scene.looping_slides = PointerProperty(type=LoopingSlidesSettings)

def unregister():
    del bpy.types.Scene.looping_slides
