###############################################################################################################################
'''
                __   __           _                    ___                 _              _
                \ \ / / ___  _ _ | |_  ___ __ __      | _ \ __ _  _ _   __| | ___  _ __  (_) ___ ___  _ _
                 \   / / -_)| '_||  _|/ -_)\ \ /      |   // _` || ' \ / _` |/ _ \| '  \ | ||_ // -_)| '_|
                  \_/  \___||_|   \__|\___|/_\_\      |_|_\\__/_||_||_|\__/_|\___/|_|_|_||_|/__|\___||_|

                                                                                                                            '''
###############################################################################################################################

bl_info = {
    "name": "Vertex Randomizer",
    "author": "DS89",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object > Vertex Randomizer",
    "description": "Changes location of vertices at random",
    "warning": "Add a shape key in order to enable the addon",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
import random


# Add a shape key to an object if one does not exist
def AddShapeKey(self, context):
    object = bpy.context.active_object
    if object.active_shape_key_index == 0:
        bpy.ops.object.shape_key_add(from_mix = False)
        bpy.ops.object.shape_key_add(from_mix = False)

# Addon panel
class VertexRandomizer(bpy.types.Panel):
    bl_label = "Vertex Randomizer"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

# Creates the panel for the user interface
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vrtool = scene.vr_tool

        # Panel object indicator
        object = bpy.context.active_object

        # Shape key data (Controls the intensity of shape key)
        shape = object.data.shape_keys
        current = object.active_shape_key_index

        # Scene data (Inputs the location of scene from panel)
        scene = context.scene
        vrtool = scene.vr_tool
        min = vrtool.min_shape
        max = vrtool.max_shape
        min_key = vrtool.min_key
        max_key = vrtool.max_key
        key_value = bpy.data.shape_keys["Key"].key_blocks[current].value
        str_val = round(key_value, 3)

        # Layout data
        layout.label(text = "Selected object: "+object.name)
        row = layout.row()
        row.operator('vr.addshape')
        layout.label(text = "Key intensity range")
        row = layout.row()
        row.prop(vrtool, 'min_key')
        row.prop(vrtool, 'max_key')
        row = layout.row()
        layout.label(text = "Shape distortion amount")
        row = layout.row()
        row.prop(vrtool, 'min_shape')
        row.prop(vrtool, 'max_shape')
        row = layout.row()
        layout.label(text = "Current key value: "+str(str_val))
        row = layout.row()
        row.operator('vr.distortshape')


# Add a shape key if there are none availible

class AddShapeOp(bpy.types.Operator):
    """Add shape key to object if none are present"""
    bl_label = 'Add shape key'
    bl_idname = 'vr.addshape'

    def execute(self,context):
        object = bpy.context.active_object
        AddShapeKey(self, context)
        return {'FINISHED'}

# User defined input

class VertexValue(bpy.types.PropertyGroup):
    min_shape:bpy.props.FloatProperty(
    name = "Min:",
    description = "Set minimum  vertex position float value",
    soft_max = 1,
    soft_min = -1
    )
    max_shape:bpy.props.FloatProperty(
    name = "Max:",
    description = "Set maximum vertex position float value",
    soft_max = 1,
    soft_min = -1
    )
    min_key:bpy.props.FloatProperty(
    name = "Min:",
    description = "Set minimum shape key float value",
    soft_max = 1,
    soft_min = 0
    )
    max_key:bpy.props.FloatProperty(
    name = "Max:",
    description  = "Set maximum shape key float value",
    soft_max = 1,
    soft_min = 0
    )


class RandomDistortion(bpy.types.Operator):
    """Randomize the vertices"""
    bl_label = "Distort shape key"
    bl_idname = 'vr.distortshape'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Active object data (Determines objects in scene)
        selected =  bpy.context.selectable_objects
        object = bpy.context.active_object
        verts = object.data.vertices
        active = selected and object

         # Shape key data (Controls the intensity of shape key)
        shape=object.data.shape_keys
        current=object.active_shape_key_index

        # Scene data (Inputs the location of scene from panel)
        scene = context.scene
        vrtool = scene.vr_tool

        # Distort code
        if vrtool.min_shape != 0 or vrtool.max_shape != 0:
            min = vrtool.min_shape
            max = vrtool.max_shape
            min_key = vrtool.min_key
            max_key = vrtool.max_key
            keyFlo = random.uniform(min_key, max_key)
            randInt = random.randrange(1000)
            bpy.data.shape_keys["Key"].key_blocks[current].value = keyFlo
            randFlo = random.uniform(min,max)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_random(seed=randInt)
            bpy.ops.transform.vertex_random(offset = randFlo, seed = randInt)
            bpy.ops.object.editmode_toggle()
        else:
            self.report({'ERROR'}, "Min and max values must be greater than or less than zero")
        return {'FINISHED'}

classes = [VertexValue, VertexRandomizer, AddShapeOp, RandomDistortion]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.vr_tool = bpy.props.PointerProperty(type = VertexValue)


def unregister():
    for cls in classes:
        bpy.utils.register_class(cls)
    del bpy.types.Scene.vr_tool

if __name__ is "__main__":
    register()
