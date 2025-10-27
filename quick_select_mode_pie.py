bl_info = {
    "name": "Select Mode Pie Menu",
    "author": "Minekokos",
    "version": (1, 1),
    "blender": (4, 5, 0),
    "location": "View3D > Edit Mode > Shortcut",
    "description": "Pie menu for quick switching between vertex/edge/face select modes",
    "category": "3D View",
}

import bpy
from bpy.types import Menu, Operator


class VIEW3D_MT_select_mode_pie(Menu):
    bl_label = "Select Mode Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

# --- Edit display names and icons here ---
        pie.operator("mesh.quick_select_mode", text="Vertex", icon='VERTEXSEL').mode = 'VERT'
        pie.operator("mesh.quick_select_mode", text="Edge", icon='EDGESEL').mode = 'EDGE'
        pie.operator("mesh.quick_select_mode", text="Face", icon='FACESEL').mode = 'FACE'


class MESH_OT_quick_select_mode(Operator):
    bl_idname = "mesh.quick_select_mode"
    bl_label = "Select Mode Pie Menu"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(
        items=[
            ('VERT', "Vertex", ""),
            ('EDGE', "Edge", ""),
            ('FACE', "Face", "")
        ],
        name="Mode",
    )

    def execute(self, context):
        if context.object is None or context.object.mode != 'EDIT':
            self.report({'WARNING'}, "Must be in Edit Mode on a mesh object")
            return {'CANCELLED'}

        bpy.ops.mesh.select_mode(use_extend=False, type=self.mode)
        return {'FINISHED'}


# --- Call menu operator ---
class WM_OT_open_select_mode_pie(Operator):
    bl_idname = "wm.call_select_mode_pie"
    bl_label = "Open Select Mode Pie"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_select_mode_pie")
        return {'FINISHED'}


# --- Registering ---
classes = (
    VIEW3D_MT_select_mode_pie,
    MESH_OT_quick_select_mode,
    WM_OT_open_select_mode_pie,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new("wm.call_select_mode_pie", type='Q', value='PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
