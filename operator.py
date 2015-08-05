import bpy
import blf
import bgl
from . utils import *
from . properties import *  
  
        
def updateTextHandlers(scene):
    show_text = bpy.context.window_manager.show_text
    mode = bpy.context.object.mode
    
    if mode == 'EDIT':
        if show_text.edt_use:
            if 'EDIT' not in show_text.update_toggle_mode:
                show_text.update_toggle_mode[:] = []
                show_text.update_toggle_mode.append(bpy.context.object.mode)
                editInfo()
            ob = scene.objects.active
            if ob.data.is_updated_data:                                      
                editInfo()
    elif mode == 'OBJECT':
        if show_text.obj_use:
            if 'OBJECT' not in show_text.update_toggle_mode:
                show_text.update_toggle_mode[:] = []
                show_text.update_toggle_mode.append(bpy.context.object.mode)
                objInfo()
            if bpy.context.selected_objects not in show_text.obj_pre:
                show_text.obj_pre[:] = []            
                show_text.obj_pre.append(bpy.context.selected_objects)
                objInfo()                     
            
            
        
def updateTextProperties(self, context):
    if self.vp_info_enabled:
        if self.edt_use and context.object.mode == 'EDIT':
            editInfo()
        if context.object.mode == 'OBJECT':
            if self.obj_use:
                objInfo()
            if self.rder_use:
                renderInfo()
            if self.scn_use:
                sceneInfo()
        if self.sculpt_use and context.object.mode == 'SCULPT':
            sculptInfo()
         
        

def drawObjTextArray(text, corner, pos_x, pos_y):
    show_text = bpy.context.window_manager.show_text
    mode = bpy.context.object.mode
    font_id = 0
    height = bpy.context.region.height
    width = bpy.context.region.width
    txt_width = []
    list_line_width = []
    blf.size(font_id, show_text.text_font_size, 72) 
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45) 
    x = 0
    y = 0 
    
    for command in text:            
        if len(command) == 2:
            Text, Color = command             
            text_width, text_height = blf.dimensions(font_id, Text) 
            txt_width.append(text_width)
    
    if corner == '1' or corner == '3':
        x = pos_x
            
    else:
        if mode == 'OBJECT' and show_text.obj_use and show_text.multi_obj_enabled and (len(bpy.context.selected_objects) >= 2):                
            count_obj = len(bpy.context.selected_objects)            
            len_list = len(txt_width)                           # count of item in the list
            count_item = int(len_list / count_obj)              # count of item by object
            i = 0
            start = 0
            end = count_item
            list_text = [] 
            
            for item in txt_width:
                while i < count_obj:
                    list_text.append(txt_width[start:start + end])
                    start+=end
                    i+=1      
            for item in list_text:
                list_line_width.append(sum(item[:]))
            x = width - (max(list_line_width) + pos_x)
        else:
            for label, value in zip(txt_width[0::2], txt_width[1::2]): 
                l_width = label + value        
                list_line_width.append(l_width) 
            x = width - (max(list_line_width) + pos_x)
            
    if corner == '1' or corner == '2': 
        y = height - pos_y
    
    else: 
        if mode == 'OBJECT' and show_text.obj_use and show_text.multi_obj_enabled and (len(bpy.context.selected_objects) >= 2):
            line_count = len(bpy.context.selected_objects)
            y = pos_y + (line_height*line_count)
        else:
            line_count = text.count("Carriage return")   
            y = pos_y + (line_height*line_count)
    
        
    for command in text:            
        if len(command) == 2:
            Text, Color = command          
            bgl.glColor3f(*Color)
            text_width, text_height = blf.dimensions(font_id, Text)                                                   
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)          
            blf.draw(font_id, Text)                
            x_offset += text_width  
                      
        else:                
            x_offset = 0           
            y_offset -= line_height
                                
def drawTextArray(text, corner, pos_x, pos_y):
    show_text = bpy.context.window_manager.show_text
    font_id = 0
    height = bpy.context.region.height
    width = bpy.context.region.width
    txt_width = []
    list_line_width = []
    blf.size(font_id, show_text.text_font_size, 72) 
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45) 
    x = 0
    y = 0 
    
    for command in text:            
        if len(command) == 2:
            Text, Color = command             
            text_width, text_height = blf.dimensions(font_id, Text) 
            txt_width.append(text_width)
    
    if corner == '1' or corner == '3':
        x = pos_x
            
    else:
        for label, value in zip(txt_width[0::2], txt_width[1::2]): 
            l_width = label + value        
            list_line_width.append(l_width) 
        x = width - (max(list_line_width) + pos_x)
            
    if corner == '1' or corner == '2': 
        y = height - pos_y
    
    else: 
        line_count = text.count("Carriage return")   
        y = pos_y + (line_height*line_count)
    
        
    for command in text:            
        if len(command) == 2:
            Text, Color = command          
            bgl.glColor3f(*Color)
            text_width, text_height = blf.dimensions(font_id, Text)                                                   
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)          
            blf.draw(font_id, Text)                
            x_offset += text_width  
                      
        else:                
            x_offset = 0           
            y_offset -= line_height
            
             
                                                                       
# Draw the text in the viewport
def drawTextCallback(self, context):        
    show_text = bpy.context.window_manager.show_text
    if context.active_object and (context.object.type == 'MESH' or context.object.type == 'CAMERA'):
        if context.object.mode == 'EDIT':
            if show_text.edt_use:
                drawTextArray(show_text.updated_edt_text, show_text.edt_corner, show_text.edt_pos_x, show_text.edt_pos_y)
        elif context.object.mode == 'OBJECT':
            if show_text.obj_use: 
                drawObjTextArray(show_text.updated_obj_text, show_text.obj_corner, show_text.obj_pos_x, show_text.obj_pos_y) 
            if show_text.rder_use: 
                drawTextArray(renderInfo(), show_text.rder_corner, show_text.rder_pos_x, show_text.rder_pos_y)
            if show_text.scn_use:
                drawTextArray(sceneInfo(), show_text.scn_corner, show_text.scn_pos_x, show_text.scn_pos_y)                
        elif context.object.mode == 'SCULPT':
            if show_text.sculpt_use:
                drawTextArray(sculptInfo(),show_text.sculpt_corner, show_text.sculpt_pos_x, show_text.sculpt_pos_y)

 
            
class VIEW3D_OT_ADH_display_text(bpy.types.Operator):
    """Display detail_refine_method active"""
    bl_idname = "view3d.adh_display_text"
    bl_label = "Display Text"
    bl_options = {'REGISTER'}
    
    _vp_info_handle = None
    
    def modal(self, context, event):
        context.area.tag_redraw()
        if not context.window_manager.show_text.vp_info_enabled:
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
     
    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_ADH_display_text._vp_info_handle = bpy.types.SpaceView3D.draw_handler_add(
               drawTextCallback, 
               (self, context),
               'WINDOW', 'POST_PIXEL')
    
    @staticmethod
    def handle_remove(context):
        _vp_info_handle = VIEW3D_OT_ADH_display_text._vp_info_handle
        if _vp_info_handle != None:
            bpy.types.SpaceView3D.draw_handler_remove(_vp_info_handle, 'WINDOW')
        VIEW3D_OT_ADH_display_text._vp_info_handle = None
                        
    def invoke(self, context, event):
        if context.window_manager.show_text.vp_info_enabled == False:
            context.window_manager.show_text.vp_info_enabled = True
            context.window_manager.modal_handler_add(self)
            VIEW3D_OT_ADH_display_text.handle_add(self, context)
            bpy.app.handlers.scene_update_post.append(updateTextHandlers)

            return {'RUNNING_MODAL'}
        else:
            context.window_manager.show_text.vp_info_enabled = False
            VIEW3D_OT_ADH_display_text.handle_remove(context)
            bpy.app.handlers.scene_update_post.remove(updateTextHandlers) 

            return {'CANCELLED'}

        return {'CANCELLED'}
