import bpy

class ManageSlidesPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_manage_slides"
    bl_label = "Manage Slides"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Slides"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.looping_slides

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="Name")
        row.label(text="Start")
        row.label(text="End")
        row.label(text="Camera")

        for i, slide in enumerate(settings.slides):
            row = col.row(align=True)

            if slide.is_playing(context):
                row.operator("screen.animation_play", text="", icon='PAUSE')
            else:
                props = row.operator("scene.play_slide", text="", icon='PLAY')
                props.index = i

            row.prop(slide, "name", text="")
            row.prop(slide, "start_frame", text="")
            row.prop(slide, "end_frame", text="")
            row.prop(slide, "camera", text="")

            props = row.operator("scene.remove_slide", text="", icon='X')
            props.index = i

        layout.operator("scene.add_slide", text="Add Slide", icon='PLUS')

        layout.prop(settings, "switch_to_camera_view")
