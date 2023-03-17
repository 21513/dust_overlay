import bpy
import os
from bpy.types import Panel, Operator, Scene
from bpy.props import EnumProperty
from bpy.utils import register_class, unregister_class
from mathutils import Matrix
from bpy_extras import view3d_utils

bl_info = {
    "name": "Dust Overlays for Blender",
    "author": "baeac",
    "version" : (1, 0),
    "blender" : (3, 4, 0),
    "location" : "View3D > baeac",
    "category" : "baeac",
    "description" : "placeholder",
}

# adding a panel
class DUST_PT_panel(Panel):
    bl_idname = 'DUST_PT_panel'
    bl_label = 'Dust Overlays by baeac'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'baeac'
 
    def draw(self, context):      
        layout = self.layout
        placeholder = context.scene.placeholder
        layout.operator('dust.op', text='Add Overlay', icon='CUBE').action = 'add dust'
        layout.operator('materials.op', text='Set Material', icon='MATERIAL').action = 'set material'
        layout.operator('delete.op', text='Delete Overlay', icon='PANEL_CLOSE').action = 'delete dust'

class DUST_OT_op(Operator):
    bl_idname = 'dust.op'
    bl_label = 'dust overlay'
    bl_description = 'dust overlay'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('add dust', 'dust overlay', 'dust overlay'),
        ]
    )
 
    def execute(self, context):
        if self.action == 'add dust':
            self.dust_overlays(context=context)
        return {'FINISHED'}

    # composite nodetree setup
    @staticmethod
    def dust_overlays(context):
        camera = bpy.context.scene.camera
        name = camera.name
        focal_length = bpy.data.cameras[name].lens
        rotation = bpy.data.objects[name].rotation_euler
        scale = bpy.data.objects[name].scale
        
        x_resolution = bpy.context.scene.render.resolution_x
        y_resolution = bpy.context.scene.render.resolution_y
        
        if x_resolution > y_resolution: # check to see which one is the biggest
            resolution_ratio = (y_resolution / x_resolution) / 2
        elif y_resolution > x_resolution:
            resolution_ratio = (x_resolution / y_resolution) / 2
            
        translate_by = -(focal_length / 36) * scale.x # idk why its 36 but i calculated it and it seems to work
        
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(rotation), scale=(1, 1, 1))
        
        for obj in bpy.context.selected_objects: # set name
            obj.name = "Dust Plane"
            obj.data.name = "Dust Plane"
            
        dust_plane = bpy.data.objects["Dust Plane"] # store in variable
        
        dust_plane.parent= camera
        dust_plane.matrix_parent_inverse = camera.matrix_world.inverted() #plane would do stupid things, so fix
        
        transform = bpy.ops.transform
        transform.resize(value=((0.5 * scale.x), (resolution_ratio * scale.x), 1), orient_type='LOCAL') # must use scale.x bcs thats only 1 value instead of just scale(x,y,z). doesnt really matter since you cant scale the camera along axis'
        
        transform.translate(value=(0, 0, translate_by), orient_type='LOCAL')
        bpy.ops.object.transform_apply(scale=True)
        transform.translate(value=(camera.location))
        
class DELETE_OT_op(Operator):
    bl_idname = 'delete.op'
    bl_label = 'delete dust overlay'
    bl_description = 'delete dust overlay'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('delete dust', 'dust overlay', 'dust overlay'),
        ]
    )
 
    def execute(self, context):
        if self.action == 'delete dust':
            self.delete_dust(context=context)
        return {'FINISHED'}

    @staticmethod
    def delete_dust(context):
        dust_plane = bpy.data.objects["Dust Plane"]
        bpy.data.objects.remove(dust_plane)
        
class MATERIALS_OT_op(Operator):
    bl_idname = 'materials.op'
    bl_label = 'set dust material'
    bl_description = 'set dust material'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('set material', 'set dust material', 'set dust material'),
        ]
    )
 
    def execute(self, context):
        if self.action == 'set material':
            self.set_material(context=context)
        return {'FINISHED'}
    
    @staticmethod
    def set_material(context):
        dust_plane = bpy.data.objects["Dust Plane"]

        absolute_path = os.path.dirname(__file__)
        relative_path = "blend/dust overlays.blend"
        path = os.path.join(absolute_path, relative_path)

        with bpy.data.libraries.load(path) as (data_from, data_to):
            data_to.materials = data_from.materials

        mat = bpy.data.materials['Dust overlay']
        dust_plane.data.materials.append(mat)
        
        
def register():
    bpy.utils.register_class(DUST_PT_panel)
    bpy.utils.register_class(DUST_OT_op)
    bpy.utils.register_class(DELETE_OT_op)
    bpy.utils.register_class(MATERIALS_OT_op)
 
def unregister():
    bpy.utils.register_class(MATERIALS_OT_op)
    bpy.utils.register_class(DELETE_OT_op)
    bpy.utils.unregister_class(DUST_OT_op)
    bpy.utils.unregister_class(DUST_PT_panel)
 
if __name__ == '__main__':
    register()