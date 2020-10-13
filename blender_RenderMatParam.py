import bpy
import os
import sys
import numpy as np

# Convenience Imports:
from mathutils import *
from math import *
# Convenience Variables:
C = bpy.context
D = bpy.data
O = bpy.ops

output_dir = '//../../data/rendered-images/{}/{}/'
output_file_format = '{}{}_{}_{}-{:02d}.png'

dir_environment_maps = "//..\\..\\data\\environment-maps\\"

renderEngine = "eevee"
renderEngineId = "BLENDER_EEVEE"
rendererDictionary = {"BLENDER_EEVEE": "eevee",
                      "CYCLES": "cycles", "BLENDER_WORKBENCH": "workbench"}
environment = "sunflowers_1k"
denoisedString = ""
parameter = "Roughness"

material = D.materials["blender-default"]
cachedInitParamVal = 0
count = 11


def setParameter(value):
    global material
    global parameter

    def setMaterialNodes():
        inputs = material.node_tree.nodes["Principled BSDF"].inputs
        inputs[parameter].default_value = value

    # def setMaterialViewport():
    #    material.roughness = value

    if C.scene.render.engine == 'BLENDER_WORKBENCH' or (not material.use_nodes):
        # setMaterialViewport()
        raise NotImplementedError(
            'Viewport materials are not supported. Use material nodes instead.')

    setMaterialNodes()
    
def getParameter():
    global material
    global parameter
    
    inputs = material.node_tree.nodes["Principled BSDF"].inputs
    
    return inputs[parameter].default_value


def renderIdToName(id):
    if id in rendererDictionary:
        return rendererDictionary[id]
    else:
        return "blender-unknown"


def renderNameToId(name):
    for id, value in rendererDictionary.items():
        if name == value:
            return id

    raise KeyError('The given renderer name "{}" is not supported in Blender. Please use one of the following: {}'.format(name,
                   ', '.join(list(rendererDictionary.values()))))


def setRenderEngine(id):
    global denoisedString

    C.scene.render.engine = id
    if id == 'CYCLES':
        if C.scene.view_layers[0].cycles.use_denoising == True:
            denoisedString = "-denoised"

    return renderIdToName(id)


# def getSceneName():
    # get filename (including extension .blend)
    #name = bpy.path.basename(bpy.context.blend_data.filepath)
    # return os.path.splitext(name)[0]


def setEnvironment(hdr_name):
    world = D.worlds[0]
    nodes = world.node_tree.nodes
    nodes["Environment Texture"].image = bpy.data.images.load(
        '{}{}.hdr'.format(dir_environment_maps, hdr_name))
    return hdr_name


def setEnvTexInterpMethod(rendererId):
    world = D.worlds[0]
    nodes = world.node_tree.nodes
    envTex = nodes["Environment Texture"]
    
    
    if(rendererId == "BLENDER_EEVEE"):
        envTex.interpolation = 'Closest'
    elif (rendererId == "CYCLES"):
        envTex.interpolation = 'Cubic'
    else:
        envTex.interpolation = 'Linear' # default
    
    print("Texture interpolation set to: " + envTex.interpolation)

def retrieveCmdArgs():
    global environment
    global renderEngineId
    global parameter

    def getCmdArgFromBack(i):
        return sys.argv[len(sys.argv) - (i+1)]

    if len(sys.argv) >= 3:
        environment = getCmdArgFromBack(0)
        renderEngineId = renderNameToId(getCmdArgFromBack(1))
        parameter = getCmdArgFromBack(2)    

def setOutputName(currentVal):
    global renderEngine
    global denoisedString
    global environment
    global parameter
    
    bpy.context.scene.render.filepath = output_dir.format(parameter.lower(), environment) + \
        (output_file_format.format(renderEngine,
                                   denoisedString, environment, parameter.lower(), int(currentVal*10)))
    

# Main

retrieveCmdArgs()

renderEngine = setRenderEngine(renderEngineId)
if not environment == 'none':
    environment = setEnvironment(environment)
    setEnvTexInterpMethod(renderEngineId)

cachedInitParamVal = getParameter()

print("Renderer used: " + renderEngine)
print("Environment: " + environment)
print("Start rendering...\n=====\n")

for i in np.linspace(0.0, 1.0, count):
    setOutputName(i)
    setParameter(i)
    print("Current value of {}: {}".format(parameter, i))
    file = bpy.ops.render.render(write_still=True)

print("\nFinished rendering!")

# reset to default material
setParameter(cachedInitParamVal)