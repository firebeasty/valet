bl_info = {
    "name": "Valet",
    "category": "Animation",
    "version": (2, 0, 1),
    "blender": (2, 80, 0),
    "author": "Keith Morgan",
    "location": "Properties > Data > ShapeKeys",
    "description": "Keyframe baking toolkit for shape keys with drivers",
}

import bpy

#Draw Buttons
def draw_valet(self, context):
    layout= self.layout

    col = layout.column(align=True)
    col.label(text="VALET TOOLKIT:")

    col = layout.column()
    col.label(text="Bake to Keys:")
    col = layout.column(align=True)
    col.operator('valet.baker', icon='KEY_HLT')
    col.operator('valet.braker', icon='KEY_DEHLT')
    col = layout.column()
    col.label(text="Revert to Drivers:")
    col = layout.column(align=True)
    col.operator('valet.choker', icon='KEY_DEHLT')
    col.operator('valet.chauffeur', icon='KEY_HLT')



class valet_baker(bpy.types.Operator):
    bl_idname = 'valet.baker'
    bl_label = "Bake Drivers to Keys"
    bl_description = "Bakes shapekey drivers to fcurves from Start to Endframe"

    def execute(self, context):
        context = bpy.context
        scene = context.scene
        object = context.object

        frame = scene.frame_start

        while frame <= scene.frame_end:
            scene.frame_set(frame)
            for values in object.data.shape_keys.animation_data.drivers.values():
                object.data.shape_keys.keyframe_insert(values.data_path)
            frame = frame + 1

        return {'FINISHED'}


class valet_braker(bpy.types.Operator):
    bl_idname = 'valet.braker'
    bl_label = "Disable Shapekey Drivers"
    bl_description = "Temporarily disables drivers on shapekeys for the selected object"

    def execute(self, context):
        ob = bpy.context.active_object.data.shape_keys
        drivers_data = ob.animation_data.drivers

        # for dr in drivers_data:
        for dr in drivers_data:
            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'
            bpy.context.space_data.mode = 'DRIVERS'

            bpy.ops.anim.channels_select_all(action='SELECT')
            bpy.ops.anim.channels_setting_enable(type='MUTE')

            bpy.context.area.type = area

        return {'FINISHED'}


class valet_choker(bpy.types.Operator):
    bl_idname = 'valet.choker'
    bl_label = "Delete Shapekey Keyframes"
    bl_description = "Deletes any baked shapekey keyframes for the active object"

    def execute(self, context):
        ob = bpy.context.active_object.data.shape_keys
        drivers_data = ob.animation_data.drivers

        # for dr in drivers_data:
        for dr in drivers_data:
            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'
            bpy.context.space_data.mode = 'FCURVES'

            #Set Filtering Context
            context.space_data.dopesheet.show_datablock_filters = True
            context.space_data.dopesheet.show_scenes = False
            context.space_data.dopesheet.show_worlds = False
            context.space_data.dopesheet.show_nodes = False
            context.space_data.dopesheet.show_transforms = False
            context.space_data.dopesheet.show_meshes = False
            context.space_data.dopesheet.show_modifiers = False
            context.space_data.dopesheet.show_materials = False
            context.space_data.dopesheet.show_lights = False
            context.space_data.dopesheet.show_textures = False
            context.space_data.dopesheet.show_cameras = False
            context.space_data.dopesheet.show_linestyles = False

            #Selects remaining Shapekey-related keyframes and deletes them
            bpy.ops.anim.channels_select_all(action='SELECT')
            bpy.ops.anim.channels_delete()

            #Resets Context
            context.space_data.dopesheet.show_datablock_filters = False
            bpy.context.area.type = area


        return {'FINISHED'}


class valet_chauffeur(bpy.types.Operator):
    bl_idname = 'valet.chauffeur'
    bl_label = "Re-enable Shapekey Drivers"
    bl_description = "Re-enables drivers on shapekeys for the selected object"

    def execute(self, context):
        ob = bpy.context.active_object.data.shape_keys
        drivers_data = ob.animation_data.drivers

        # for dr in drivers_data:
        for dr in drivers_data:
            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'
            bpy.context.space_data.mode = 'DRIVERS'

            bpy.ops.anim.channels_select_all(action='SELECT')
            bpy.ops.anim.channels_setting_disable(type='MUTE')

            bpy.context.area.type = area

        return {'FINISHED'}


def register():
    bpy.types.DATA_PT_shape_keys.append(draw_valet)
    bpy.utils.register_class(valet_baker)
    bpy.utils.register_class(valet_braker)
    bpy.utils.register_class(valet_choker)
    bpy.utils.register_class(valet_chauffeur)

def unregister():
    bpy.utils.unregister_class(valet_baker)
    bpy.utils.unregister_class(valet_braker)
    bpy.utils.unregister_class(valet_choker)
    bpy.utils.unregister_class(valet_chauffeur)
    bpy.types.DATA_PT_shape_keys.remove(draw_valet)

if __name__ == "__main__":
    register()
