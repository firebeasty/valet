bl_info = {
    "name": "Valet",
    "category": "Animation",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "author": "Keith Morgan",
    "location": "Properties > Data > ShapeKeys",
    "description": "Bakes ShapeKeys to fcurves",
}

import bpy


def valet(self, context):
    layout= self.layout
    split = layout.split

    row = layout.row()
    row.operator('valet.baker', icon='ANIM_DATA')
    row = layout.row()
    row.operator('valet.braker', icon='RADIO')

class valet_baker(bpy.types.Operator):
    bl_idname = 'valet.baker'
    bl_label = "Bake Shapekey Drivers"
    bl_description = "Bakes ShapeKey drivers to fcurves from Start to Endframe"

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
    bl_label = "Remove Shapekey Drivers"
    bl_description = "Removes drivers on shapekeys [WARNING: DESTRUCTIVE]"

    def execute(self, context):
        ob = bpy.context.active_object.data.shape_keys
        # ob = bpy.ops.anim.channels_setting_enable(type='MUTE')
        drivers_data = ob.animation_data.drivers

        for dr in drivers_data:
            ob.driver_remove(dr.data_path, -1)
            # bpy.ops.anim.channels_setting_enable(type='MUTE')

        return {'FINISHED'}


def register():
    bpy.types.DATA_PT_shape_keys.append(valet)
    bpy.utils.register_class(valet_baker)
    bpy.utils.register_class(valet_braker)

def unregister():
    bpy.utils.unregister_class(valet_baker)
    bpy.utils.unregister_class(valet_braker)
    bpy.types.DATA_PT_shape_keys.remove(valet)

if __name__ == "__main__":
    register()
