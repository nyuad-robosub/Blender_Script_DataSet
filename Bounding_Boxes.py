import bpy
from bpy_extras.object_utils import world_to_camera_view
import random
import os
import numpy as np
from math import *
from mathutils import *

o = bpy.context.object
camera = bpy.data.objects['Camera']
cam_location = camera.matrix_world.translation
local_bbox_center = 0.125 * sum((Vector(b) for b in o.bound_box), Vector())
global_bbox_center = o.matrix_world @ local_bbox_center
cam_distance = (o.matrix_world * global_bbox_center - cam_location).length
if cam_distance > 25: 
    print(' Distance between object and camera greater than 25m')
    continue
else: 
    #print (global_bbox_center[-1])
    check = world_to_camera_view(bpy.context.scene, camera, global_bbox_center)
    print(check)
    if check[-1] < 0:
        print('object behind camera')
        continue 

    else: 
        #create new mesh data using inverse transform matrix to undo transformations

        dg = bpy.context.evaluated_depsgraph_get()
        obj = bpy.context.object.evaluated_get(dg)
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)

        lx = []
        ly = []

        # 0bpy.context.view_layer.update()// separate list for z vertices: less than 0; if all are less than 0 then teh object is entirely behind 
        for v in mesh.vertices:
            co_final = obj.matrix_world @ v.co
            co_image = world_to_camera_view(bpy.context.scene, camera, co_final)
            x = co_image[0]
            y = co_image[1]
            
            
            lx.append(x)
            ly.append(y)

        # if all the x &y are outside the range 
        # check if object is too far== eliminate the longer ones     
        min_x = np.clip(min(lx), 0.0, 1.0)
        min_y = np.clip(min(ly), 0.0, 1.0)
        max_x = np.clip(max(lx), 0.0, 1.0)
        max_y = np.clip(max(ly), 0.0, 1.0)