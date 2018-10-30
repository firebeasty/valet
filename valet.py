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


def register():
    bpy.types.DATA_PT_shape_keys.append(valet)
    bpy.utils.register_class(valet_baker)

def unregister():
    bpy.utils.unregister_class(valet_baker)
    bpy.types.DATA_PT_shape_keys.remove(valet)

if __name__ == "__main__":
    register()
