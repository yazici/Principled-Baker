import bpy

class PBAKER_PT_panel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Principled Baker"
    bl_context = "objectmode"
    bl_category = "Principled Baker"

    @classmethod
    def poll(cls, context):
        if context.space_data.tree_type == 'ShaderNodeTree':
            return True
        return False

    def draw(self, context):
        settings = context.scene.principled_baker_settings
        render_settings = context.scene.render.bake

        if bpy.context.scene.render.engine == 'CYCLES':
            self.layout.operator('object.principled_baker_bake', text='Bake', icon='RENDER_STILL')
        else:
            self.layout.label(text="Set Render engine to Cycles! {} is not supported (yet).".format(bpy.context.scene.render.engine), icon='ERROR')

        # box = self.layout.box()
        # bake/render options:
        col = self.layout.box().column(align=True)
        col.prop(render_settings, "margin")
        # col.prop(render_settings, "use_clear", text="Clear Image")
        col.separator()
        col.prop(render_settings, "use_selected_to_active")
        sub = col.column()
        sub.active = render_settings.use_selected_to_active
        sub.prop(render_settings, "use_cage", text="Cage")
        if render_settings.use_cage:
            sub.prop(render_settings, "cage_extrusion", text="Extrusion")
            sub.prop(render_settings, "cage_object", text="Cage Object")
        else:
            sub.prop(render_settings, "cage_extrusion", text="Ray Distance")
        
        col.separator()
        col.prop(settings, "samples")

        # output options:
        col = self.layout.box().column(align=True)
        row = col.row()
        row.prop(settings, "resolution", expand=True)
        if settings.resolution == 'CUSTOM':
            col.prop(settings, "custom_resolution")
        col.separator()
        col.prop(settings, "file_path")
        col.prop(settings, "use_overwrite")

        col.separator()
        # image settings:
        col.prop(settings, "file_format")

        row = col.row()
        row.prop(settings, "color_mode", text="Color", expand=True)
        row = col.row()
        row.prop(settings, "color_depth", text="Color Depth", expand=True)
        
        if settings.file_format == 'OPEN_EXR':
            col.prop(settings, "exr_codec", text="Codec")

        if settings.file_format == 'TIFF':
            col.prop(settings, "tiff_codec", text="Compression")

        if settings.file_format == 'JPEG':
            col.prop(settings, "quality", text="Quality")


        # prefix and suffix settings:
        col = self.layout.box().column(align=True)
        col.prop(settings, "image_prefix")
        col.prop(settings, "use_object_name")
        col.prop(settings, "image_suffix_settings_show", toggle=True)
        if settings.image_suffix_settings_show:
            col.prop(settings, "suffix_color")
            col.prop(settings, "suffix_metallic")
            col.prop(settings, "suffix_roughness")
            col.prop(settings, "suffix_glossiness")
            col.prop(settings, "suffix_normal")
            col.prop(settings, "suffix_bump")
            col.prop(settings, "suffix_displacement")
            col.prop(settings, "suffix_vertex_color")
            row = col.row()
            row.prop(settings, 'suffix_text_mod', expand=True)

        # new material:
        col = self.layout.box().column(align=True)
        col.prop(settings, "use_new_material")
        col.prop(settings, "new_material_prefix")

        # autodetect
        col = self.layout.box().column(align=True)
        col.prop(settings, "use_autodetect", toggle=True)
        col.separator()


        if not settings.use_autodetect:
        #     col.prop(settings, "use_Bump")
        # else:
            col.prop(settings, "use_Base_Color", toggle=True)
            col.prop(settings, "use_Metallic", toggle=True)
            col.prop(settings, "use_Roughness", toggle=True)

            col.prop(settings, "use_Normal", toggle=True)
            # col.prop(settings, "use_Bump", toggle=True)
            col.prop(settings, "use_Displacement", toggle=True)

            col.separator()
            col.prop(settings, "use_Alpha", toggle=True)
            col.prop(settings, "use_Emission", toggle=True)
            # 2.80
            if bpy.app.version_string.startswith('2.8'):
                col.prop(settings, "use_AO", toggle=True)

            col.separator()
            col.prop(settings, "use_Subsurface", toggle=True)
            # TODO col.prop(settings, "use_Subsurface_Radius", toggle=True)
            col.prop(settings, "use_Subsurface_Color", toggle=True)
            col.prop(settings, "use_Specular", toggle=True)
            col.prop(settings, "use_Specular_Tint", toggle=True)
            col.prop(settings, "use_Anisotropic", toggle=True)
            col.prop(settings, "use_Anisotropic_Rotation", toggle=True)
            col.prop(settings, "use_Sheen", toggle=True)
            col.prop(settings, "use_Sheen_Tint", toggle=True)
            col.prop(settings, "use_Clearcoat", toggle=True)
            col.prop(settings, "use_Clearcoat_Roughness", toggle=True)
            col.prop(settings, "use_IOR", toggle=True)
            col.prop(settings, "use_Transmission", toggle=True)
            col.prop(settings, "use_Transmission_Roughness", toggle=True)
            col.prop(settings, "use_Clearcoat_Normal", toggle=True)
            col.prop(settings, "use_Tangent", toggle=True)
        
        col.prop(settings, "use_invert_roughness")
        col.prop(settings, "use_Bump")
        col.prop(settings, "use_vertex_color")

        # settings:
        col = self.layout.box().column(align=True)
        col.label(text="Auto Smooth:" )
        row = col.row()
        row.prop(settings, "auto_smooth", text="Auto Smooth", expand=True)
        col.separator()
        if settings.color_mode == 'RGBA':
            col.prop(settings, "use_alpha_to_color")
        col.prop(settings, "use_exclude_transparent_colors")


        col = self.layout.box().column(align=True)
        col.prop(settings, "use_smart_uv_project")
        if settings.use_smart_uv_project:
            col.prop(settings, "angle_limit")
            col.prop(settings, "island_margin")
            col.prop(settings, "user_area_weight")
            col.prop(settings, "use_aspect")
            col.prop(settings, "stretch_to_bounds")

