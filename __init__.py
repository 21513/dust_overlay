import bpy
from . import ps1_ify

bl_info = {
    "name": "Dust Overlays for Blender",
    "author": "baeac",
    "version" : (1, 0),
    "blender" : (3, 4, 0),
    "location" : "View3D > baeac",
    "category" : "baeac",
    "description" : "Import a plane with a dust overlay material to make your camera look more realistic!",
}

def register():
    dust_overlay.register()

def unregister():
    dust_overlay.unregister()
 
if __name__ == "__main__":
    register()