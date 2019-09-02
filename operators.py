import bpy
from bpy.props import *

class AddSlideOperator(bpy.types.Operator):
    bl_idname = "scene.add_slide"
    bl_label = "Add Slide"

    def execute(self, context):
        scene = context.scene
        settings = scene.looping_slides

        item = settings.slides.add()
        item.start_frame = scene.frame_current
        item.end_frame = scene.frame_current + 10
        if getattr(context.active_object, "type", "") == "CAMERA":
            item.camera = context.active_object

        context.area.tag_redraw()
        return {'FINISHED'}

class RemoveSlideOperator(bpy.types.Operator):
    bl_idname = "scene.remove_slide"
    bl_label = "Remove Slide"

    index: IntProperty()

    def execute(self, context):
        scene = context.scene
        settings = scene.looping_slides
        settings.slides.remove(self.index)

        context.area.tag_redraw()
        return {'FINISHED'}

class PlaySlideOperator(bpy.types.Operator):
    bl_idname = "scene.play_slide"
    bl_label = "Play Slide"

    index: IntProperty()

    def execute(self, context):
        scene = context.scene
        settings = scene.looping_slides

        slide = settings.slides[self.index]
        scene.frame_current = slide.start_frame
        scene.frame_start = slide.start_frame
        scene.frame_end = slide.end_frame
        scene.camera = slide.camera

        if settings.switch_to_camera_view:
            context.space_data.region_3d.view_perspective = 'CAMERA'

        bpy.ops.object.select_all(action='DESELECT')
        slide.camera.select_set(True)
        context.view_layer.objects.active = slide.camera

        if not context.screen.is_animation_playing:
            bpy.ops.screen.animation_play()

        return {'FINISHED'}

class NextSlideOperator(bpy.types.Operator):
    bl_idname = "scene.next_slide"
    bl_label = "Next Slide"

    def execute(self, context):
        scene = context.scene
        settings = scene.looping_slides
        if len(settings.slides) == 0:
            return {'CANCELLED'}

        next_index = find_slide_with_offset(context, settings, offset=1)
        bpy.ops.scene.play_slide(index=next_index)
        return {'FINISHED'}



class PreviewSlideOperator(bpy.types.Operator):
    bl_idname = "scene.previous_slide"
    bl_label = "Previous Slide"

    def execute(self, context):
        scene = context.scene
        settings = scene.looping_slides
        if len(settings.slides) == 0:
            return {'CANCELLED'}

        previous_index = find_slide_with_offset(context, settings, offset=-1)
        bpy.ops.scene.play_slide(index=previous_index)
        return {'FINISHED'}

def find_slide_with_offset(context, settings, offset):
    current_index = find_current_slide_index(context, settings)
    next_index = (current_index + offset) % len(settings.slides)
    return next_index

def find_current_slide_index(context, settings):
    for i, slide in enumerate(settings.slides):
        if slide.is_set(context):
            return i
    else:
        return -1
