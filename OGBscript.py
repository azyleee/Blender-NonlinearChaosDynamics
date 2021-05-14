# Authors: Eoghan Phelan, Aidan Lee
# This script is must be run in the Blender Text Editor.
# This script generates the oscillating Galton board model, runs the simulation, and exports the result

import bpy
import os
import csv
from math import sin

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)  # Deletes previous configuration before creating again
bpy.ops.ptcache.free_bake_all() # delete previous bake


context = bpy.context
scene = context.scene

# Go to frame 0
bpy.context.scene.frame_set(0)

# define the first and last frequencies to be tested
# NOTE: DO NOT CHANGE lastf. TEST 1 FREQUENCY AT A TIME. THE LOOP NO LONGER WORKS IN v2.91. 
firstf=10
lastf=firstf+1

# MORE INPUTS ARE REQUIRED FROM LINE 65 TO LINE 92
# DIRECTORY FOR SIMULATION RESULT MUST BE DEFINED ON LINE 307

# define the substeps per frame
sspf=5

for f in range(firstf,lastf):

    # SET BAKE SETTINGS

    # Set framerate
    if f<6:
        FPS=24
    else:    
        FPS=4*f # framerate of animation
        
    bpy.context.scene.render.fps=FPS
    
    # Set Frame Start and End
    bpy.context.scene.frame_start=0

    endframe=(FPS/24)*10000
    bpy.context.scene.frame_end=endframe

    # Go to frame 0
    bpy.context.scene.frame_set(0)     
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False) # Deletes previous configuration before creating again
   
    bpy.ops.ptcache.free_bake_all() # delete previous bake


    context = bpy.context
    scene = context.scene

    #####

    for c in scene.collection.children:
        scene.collection.children.unlink(c)
        
    for c in bpy.data.collections:
        if not c.users:
            bpy.data.collections.remove(c)        # Creates scene
            
    # INPUTS FOR SINUSOIDAL OSCILLATION OF PEGS
    pi=3.14159265358979323846264338327950288419716939937510

    A=0.325 # input the amplitude of oscillation
    f=f # input the frequency of oscillation
    
    phase_diff=0 # input the offset of oscillation

    # INPUTS FOR GALTON BOARD DIMENSIONS & PARAMETERS
    s = 0.25  # Diameter of the scater pegs

    rgapx = 0.84855 # Distance between pegs to the right in x direction

    gapz =rgapx # Distance between pegs in z direction

    lgapx =rgapx # Distance between pegs to the left in x direction

    n = 6  # Number of rows of pegs
    slotn = 600 # Number of bins_

    cube = 0.3 # Diameter of particle

    cubex = 40 # Number of x rows of particles
    cubez = 25  # Number of z rows of particles
    cubemass=0.0002

    ramp_offset=1.4*cube # control the size of the funnel opening 
    extra=200 # spread of bins

    # CALCULATION OF CONSTANTS 
    if f==0:
        period=1
    else:
        period=FPS/f

    l = n*gapz*4.75*2.5 # length of the board
    w = (n*lgapx + rgapx*n+extra) # width of the bins
    w2 = (n*lgapx + rgapx*n)*1.5 # width of back board
    bret = cube*1.05 # breadth of the board

    ramp = l # length of funnel 

    x = 0             # Default x position
    y = -bret*0.5     # Default y position
    z = l*0.6         # Default z position

    # PLACE CAMERA AND LIGHT
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0,72.404, 25.0051), 
        rotation=(90/57.3, 0, 180/57.3), scale=(1, 1, 1))
    bpy.ops.object.light_add(type='SUN', location=(0, 180.081, 188.388), 
        rotation=(-90/57.3, 0, 0), scale=(1, 1, 1))


    # CONTRUCTION OF OBJECTS

    bin_collection = bpy.data.collections.new('bins')
    bpy.context.scene.collection.children.link(bin_collection) # Creates collection of the bins

    # Construction of the the back board
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0 , bret*0.5, l*0.5))
    bpy.ops.transform.resize(value=(extra+w2, bret, l*2), constraint_axis=(True, True, True))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0.0001
    bpy.context.object.hide_viewport = False
    bpy.context.object.hide_render = True

    # Construction of the front board
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0 , -bret*1.5, l*0.5))
    bpy.ops.transform.resize(value=(extra+w2, bret, l*2), constraint_axis=(True, True, True))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0.0001
    bpy.context.object.hide_viewport = False
    bpy.context.object.hide_render = True



    # Construction of the floor board
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -bret*0.5))
    bpy.ops.transform.resize(value=(extra+w2, bret*4, bret), constraint_axis=(True, True, True))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0.0001

    #Code that constucts the 1st ramp

    bpy.ops.mesh.primitive_cube_add(size=1, location=(x - 1.5*cube - 0.5*ramp*0.72 + ramp_offset, 
        y, z + 1.5*gapz + ramp*0.5*0.72))
    bpy.ops.transform.resize(value=(ramp, bret, s), constraint_axis=(True, True, True))
    bpy.ops.transform.rotate(value=0.7853981, orient_axis='Y', orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL', constraint_axis=(True, True, True),)
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0.0001
    bpy.context.object.rigid_body.friction = 0

    #Code that constucts the 2nd ramp
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 1.5*cube + 0.5*ramp*0.72 - ramp_offset, 
        y, z + 1.5*gapz + ramp*0.5*0.72))
    bpy.ops.transform.resize(value=(ramp, bret, s), constraint_axis=(True, True, True))
    bpy.ops.transform.rotate(value=-0.7853981, orient_axis='Y', orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL', constraint_axis=(True, True, True),)
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    bpy.context.object.rigid_body.use_margin = True
    bpy.context.object.rigid_body.collision_margin = 0.0001
    bpy.context.object.rigid_body.friction = 0


    # CONSTRUCTION OF OBJECTS IN LOOPS

    count = 0

    # Loop that contstructs the specified number of scatter pegs
    while (count < n):     
        
        
        
        for i in range (0, n-count):
            bpy.ops.mesh.primitive_cylinder_add(radius=s*0.5, depth=bret, enter_editmode=False, 
                location=((x - lgapx*count) + rgapx*i, y, (z - gapz*count) - gapz*i))
            bpy.ops.transform.rotate(value=2*0.7853981, orient_axis='X', orient_type='GLOBAL', 
                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                orient_matrix_type='GLOBAL', constraint_axis=(True, True, True),)
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'PASSIVE'
            bpy.context.object.rigid_body.use_margin = True
            bpy.context.object.rigid_body.collision_margin = 0.0001
            bpy.context.object.rigid_body.friction = 0.25
            bpy.context.object.rigid_body.restitution = 0.25

            peg = bpy.context.selected_objects[0] # newly created peg will be automatically selected
            bpy.context.object.rigid_body.kinematic = True # make it animated/kinematic
            Peg=bpy.context.object

            # Create keyframes of the peg movements
            
            dot=0
            x0=Peg.location[0]        

            if f!=0:
                if (i%2==0 and count%2==0) or (i%2!=0 and count%2!=0):
                    C=phase_diff
                else:
                    C=0
                        
                while (dot<period+1): 
                    
                    # calculate displacement for a frame
                    x=A*sin(2*pi*(f/FPS)*dot+C)

                    Peg.location[0] = x0+x # location is its original position + the displacement 
                    Peg.keyframe_insert(data_path="location", frame=dot) # Set the keyframe with that location, and which frame.
                    
                    dot+=1
            
                #repeat the movement infinitely with cycles modifier
                obj = bpy.context.selected_objects[0]
                #pick the fcurve to add to 
                fcurve = obj.animation_data.action.fcurves[0]
                #add a modifier and get a reference.
                fcurve = fcurve.modifiers.new(type='CYCLES')
        count+=1

    # Loop that generates the specificed number of bins 
    for a in range (1, slotn): 
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-n*lgapx + (w/slotn)*a -extra/2, 
            y, z - n*gapz - ((z - n*gapz)*0.5)))
        bpy.ops.transform.resize(value=(cube*0.15, bret, z - n*gapz), 
            constraint_axis=(True, True, True))
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'PASSIVE'
        bpy.context.object.rigid_body.use_margin = True
        bpy.context.object.rigid_body.collision_margin = 0.0001
        bpy.context.object.rigid_body.friction = 0
        obj = bpy.context.object
        bin_collection.objects.link(obj)
        

     
                
    # Create a new collection for physics objects
    sphere_collection = bpy.data.collections.new('spheres')
    bpy.context.scene.collection.children.link(sphere_collection)
    for b in range (1, cubex):  # Loops that generate the number of particles specificed along a single row only
            bpy.ops.mesh.primitive_ico_sphere_add(radius=cube*0.5, 
                location=((-1.5*cube-ramp*0.5*0.71)+ (2*b*(1.5*cube+ramp*0.5*0.71))/cubex, 
                y, z + 2*gapz + ramp*0.5*0.71 +1.25*cube))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'ACTIVE'
            bpy.context.object.rigid_body.use_margin = True
            bpy.context.object.rigid_body.collision_margin = 0.0001
            bpy.context.object.rigid_body.friction = 0.0
            bpy.context.object.rigid_body.restitution = 0.25
            bpy.context.object.rigid_body.linear_damping = 0.6
            bpy.context.object.rigid_body.angular_damping = 0.3
            bpy.context.object.rigid_body.mass = cubemass
            obj = bpy.context.object
            sphere_collection.objects.link(obj)
            
    # Duplicate physics objects in z direction 
    bpy.ops.object.select_same_collection(collection="spheres")
    for n in range(0,cubez):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, 
        TRANSFORM_OT_translate={"value":(0, 0, 0.5), "orient_type":'GLOBAL', 
        "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL'})
        
    text='baking f='+str(f)+'Hz'+' ----------------------------------------'
    print(text)
    
    # BAKE ALL DYNAMICS
    # Set Start and End of Simulation Bake
    bpy.context.scene.rigidbody_world.point_cache.frame_start = 0
    bpy.context.scene.rigidbody_world.point_cache.frame_end = endframe
    
    bpy.context.scene.rigidbody_world.substeps_per_frame = sspf # set steps per second
    bpy.ops.ptcache.bake_all(bake=True)

    # SAVE AND EXPORT DISTRIBUTION

    # Go to the last frame to save the ball locations
    bpy.context.scene.frame_set(endframe)
    
    # Create filename
    name='f'+str(f)
    filename="%s.csv" % name
    
    # Save ball locations in .csv
    bpy.ops.object.select_same_collection(collection="spheres")
    bpy.ops.object.visual_transform_apply() # Applies visual transformation
    os.chdir('C:\\Users\\Aidan\\OneDrive\\BiasedGaltonData\\3mmsim') # File directory
    with open(filename, 'w') as csvfile: # File name
        writer = csv.writer(csvfile, delimiter=',')
        for sphere in bpy.data.collections['spheres'].objects: #Loops through collection of Spheres
            writer.writerow([sphere.location[0],sphere.location[2]]) # Records x and z position
            sphere.location[2]
            
    print('write complete')

    text=str(lastf-1-f)+' remaining'
    print(text)
    

print('ALL COMPLETE *************************************************')
