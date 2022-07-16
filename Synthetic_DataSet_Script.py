import bpy
from bpy_extras.object_utils import world_to_camera_view
import random
import os
import numpy as np
from math import *
from mathutils import *
import xml.etree.cElementTree as ET

# Creating a Dictionary for opening the objects 
Dict = {0: 'qual_gate', 
        1: 'bin_empty',
        2: 'lid_empty',
        3: 'image_badge',
        4: 'image_bootlegger',
        5: 'image_gman',
        6: 'image_tommygun',
        7: 'handle',
        8: 'marker' ,
        9: 'Collecting_Bins_Gman_Alc' ,
        10:'Collecting_Bins_Gman_Bin' , 
        11 :'Collecting_Bins_Gman_Notepad' , 
        12 :'Collecting_Bins_Gman_Phone'
        }
cam_bound_size = {
    0: (35, False, 0),
    1: (20, True, 1),
    2: (3, True, 1.6),
    3: (25, False, 0),
    4: (25, False, 0),
    5: (25, False, 0),
    6: (25, False, 0),
    7: (2, True, 1.6),
    8: (6, True, 1),
    9: (25, False, 0),
    10: (25, False, 0),
    11: (25, False, 0),
    12: (25, False, 0)
}
obj_z_from_bottom = {
    0: (False, 0),
    1: (True, 0.5),
    2: (False, 0),
    3: (False, 0),
    4: (False, 0),
    5: (False, 0),
    6: (False, 0),
    7: (False, 0),
    8: (True, 0.2),
    9: (False, 0),
    10: (False, 0),
    11: (False, 0),
    12: (False, 0)
}

# importing the different objects 
def object_importing(x):
    # variable for the file location 
    file_loc = '/home/aira/Downloads/render package-20220710T234909Z-001/render package/new_blender_models'
    
    # importing object file 
    joined_path = os.path.join(file_loc, (Dict[x]) + '.dae')
    imported_object = bpy.ops.wm.collada_import(filepath = joined_path, 
                      auto_connect = True, 
                      find_chains = True, 
                      fix_orientation = True) 
    
    #assigning name to the imported objects 
    bpy.context.selected_objects[0].name = Dict[x]
    
    # import object to origin 
    #(Dict[x]).location = (0.0, 0.0, 0.0)
    bpy.data.objects[(Dict[x])].cycles.is_caustics_receiver = True 


#making sure the camera tracks the newly imported object
def Track_To( current_object):
    
    # This code will create the camera and set it up to track to the Cube
    track_object = current_object
    scene = bpy.context.scene

    cam = bpy.data.objects['Camera Housing']
    # cons = cam.constraints.new(type='TRACK_TO')
    cons = cam.constraints['Track To']
    cons.target = track_object
    # scene.camera = cam

#this function deletes a given object
def ObjectDeletion(obj):
    
    current_object = bpy.data.objects[obj.name]
    
    bpy.ops.object.select_all(action='DESELECT')

    current_object.select_set(True)
  
    bpy.ops.object.delete()
 
    
def Camera_Motion(pos, d):
    # Parameter position of object to follow & id of object
    
    camera_housing = bpy.data.objects['Camera Housing']
    camera = bpy.data.objects['Camera']
     
    xlim_min = max(pos[0] - cam_bound_size[d][0] / 2.0, -24)
    xlim_max = min(pos[0] + cam_bound_size[d][0] / 2.0, 24)
    ylim_min = max(pos[1] - cam_bound_size[d][0] / 2.0, -11)
    ylim_max = min(pos[1] + cam_bound_size[d][0] / 2.0, 11)
    
    x = round(random.uniform(xlim_min, xlim_max), 5)
    y = round(random.uniform(ylim_min, ylim_max), 5)

#    x = random.random() * 49.4 -24.458
#    y = random.random() * 22.8 -11.385
        
    if x > 17.842: 
        z_lower_bound = -0.16994 + 0.2
    else:
        z_lower_bound = -0.04019 * x + 0.8870 + 0.2
    
    if not cam_bound_size[d][1]:
        z = random.random() * (3.7 - z_lower_bound) + z_lower_bound
    else:
        z = 3.7 - random.random() * cam_bound_size[d][2]
        
    camera_housing.location[0] = x
    camera_housing.location[1] = y
    camera_housing.location[2] = z
        
   

def Object_Motion(object_to_follow, d):
    
    x = random.random() * 40 - 20
    y = random.random() * 18 - 9

    if x > 17.842: 
        z_lower_bound = -0.16994 + 0.2
    else:
        z_lower_bound = -0.04019 * x + 0.8870 + 0.2
    
    if not obj_z_from_bottom[d][0]:
        z =  random.random() * (2.7053 - z_lower_bound) + z_lower_bound
    else:
        z =  random.random() * obj_z_from_bottom[d][1] + z_lower_bound
    
    object_to_follow.location[0] = x
    object_to_follow.location[1] = y
    object_to_follow.location[2] = z
    bpy.context.object.rotation_euler[2] = random.random()*pi

    return (x, y, z)
    
def HDRI_Import():
    
    scn = bpy.context.scene
    
    # Get the environment node tree of the current scene
    node_tree = scn.world.node_tree
    tree_nodes = node_tree.nodes

    # Clear all nodes
    tree_nodes.clear()

    # Add Background node
    node_background = tree_nodes.new(type='ShaderNodeBackground')

    # Add Environment Texture node
    node_environment = tree_nodes.new('ShaderNodeTexEnvironment')

    file_pathway_4_hdris = '/home/aira/Downloads/render package-20220710T234909Z-001/render package/Backgrounds_Blender-20220710T021809Z-001/Backgrounds_Blender'  
    
    x = str(random.randint(0,20))

    # importing object file 
    joined_path = os.path.join(file_pathway_4_hdris, x + '.exr')

    # Load and assign the image to the node property
    node_environment.image = bpy.data.images.load(joined_path) 
    node_environment.location = -300,0

    # Add Output node
    node_output = tree_nodes.new(type='ShaderNodeOutputWorld')   
    node_output.location = 400,0

    # Link all nodes
    links = node_tree.links
    link = links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
    link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])
    
    # generating random number for strength of the HDRI             
    w = round(random.uniform(1.20, 3.00), 2)
    
    # assigning strength to the HDRI
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = w
            
    
    
def Change_Water_Features():

    H = round(random.uniform(0.50, 0.65), 5)
    S = round(random.uniform(0.9, 1.0), 5)
    V = round(random.uniform(0.7, 1.0), 5)
    
    bpy.data.materials["Water"].node_tree.nodes["Hue Saturation Value"].inputs[4].default_value = ( H, S, V, 1) 
    
    math_multiply = round(random.uniform(0.04, 0.12), 3) 
    bpy.data.materials["Water"].node_tree.nodes["Math"].inputs[1].default_value = math_multiply 


def Change_Pool_tiles():
    
    # Get the environment node tree of the current scene
    tree_nodes = bpy.data.materials["Pool.001"].node_tree.nodes["Image Texture"]

    file_pathway_4_pool_tiles = '/home/aira/Downloads/render package-20220710T234909Z-001/render package/Pool_Floor_Options'  
    
    x = str(random.randint(0,6))

    # importing object file 
    joined_path = os.path.join(file_pathway_4_pool_tiles , x + '.png')

    # Load and assign the image to the node property
    tree_nodes.image = bpy.data.images.load(joined_path) 

            

def Bounding_Box(obj, camera, scene, obj_name, j): 

#    #get the inverse transformation matrix
#    matrix = camera.matrix_world.normalized().inverted()

#    #create new mesh data using inverse transform matrix to undo transformations
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
        
    print(len(lx), min(lx), max(lx))
    print(min(ly), max(ly))
    
    
    # if all the x &y are outside the range 
    # check if object is too far== eliminate the longer ones     
    min_x = np.clip(min(lx), 0.0, 1.0)
    min_y = np.clip(min(ly), 0.0, 1.0)
    max_x = np.clip(max(lx), 0.0, 1.0)
    max_y = np.clip(max(ly), 0.0, 1.0)
    
        
    ## Verify there's no coordinates equal to zero
    coord_list = [min_x, min_y, max_x, max_y]
    if min(coord_list) == 0.0:
        indexmin = coord_list.index(min(coord_list))
        coord_list[indexmin] = coord_list[indexmin] + 0.0000001

  

    scene = bpy.context.scene
    cam = bpy.data.objects['Camera']
    render_path = '/home/aira/Desktop/Annimation_test_1/new_Data_Set'
    joined_path = os.path.join(render_path, obj_name + "_" + "{:03d}".format(j) + '.jpg')
    scene.render.filepath =  joined_path
    bpy.ops.render.render(write_still=True, use_viewport=True)
    

    rp = scene.render.resolution_percentage
    rx = scene.render.resolution_x
    ry = scene.render.resolution_y

    fac = rp * 0.01
    dim_x =  rx * fac
    dim_y =  ry * fac

    xmin = min_x * dim_x
    ymin = dim_y - max_y * dim_y

    width = (max_x - min_x) * dim_x
    height = (max_y - min_y) * dim_y

    xmax = xmin + width
    ymax = ymin + height

    #write parameters into xml file
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "0"
    ET.SubElement(annotation, "filename").text = "0"
    ET.SubElement(annotation, "path").text = "0"
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(dim_x)
    ET.SubElement(size, "height").text = str(dim_y)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(annotation, "segmented").text = "0"
    object = ET.SubElement(annotation, "object")
    ET.SubElement(object, "name").text = str(obj.name)
    ET.SubElement(object, "pose").text = "Unspecified"
    ET.SubElement(object, "truncated").text = "1"
    ET.SubElement(object, "difficult").text = "0"
    bndbox = ET.SubElement(object, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(int(xmin))
    ET.SubElement(bndbox, "ymin").text = str(int(ymin))
    ET.SubElement(bndbox, "xmax").text = str(int(xmax))
    ET.SubElement(bndbox, "ymax").text = str(int(ymax))

    XML = ET.ElementTree(annotation)
    label_path = '/home/aira/Desktop/Annimation_test_1/labels_4_blender'
    joined_path = os.path.join(label_path, obj_name + "_" + "{:03d}".format(j) + '.xml')
    XML.write (joined_path) 










if __name__ == "__main__":
    
   
    
   #random.seed()#340589)#551545)#594982) #67578)
   #initialize objects, camera, and scenes  
   camera = bpy.data.objects['Camera']
   scene = bpy.data.scenes['Scene']

   for d in range(9, 13):
       # importing the object into the scene
       object_importing(d)
       # assigning imported object to obj 
       import time 
       start = 0
       if d == 9:
           start = 0
       for i in range(start, 500):
           obj = bpy.data.objects[Dict[d]]
           Track_To(obj)
           pos = Object_Motion(obj, d)
           Camera_Motion(pos, d)
           Change_Water_Features()
           HDRI_Import()
           Change_Pool_tiles()
           Bounding_Box(obj, camera, scene, Dict[d], i)
       ObjectDeletion(obj)
#            