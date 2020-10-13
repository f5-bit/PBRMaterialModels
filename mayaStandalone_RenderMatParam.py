import maya.standalone
maya.standalone.initialize(name='python')
import pymel.core as pc
import mtoa.cmds.arnoldRender as aR
import numpy as np
import os
import sys
import time
import shutil

mayaFilePath = ""
mayaProjectPath = ""

outputDir = '../../../data/rendered-images/{}/{}/'
currentOutputPath = ""
currentFilename = ""
dirEnvironmentMaps = "../../../data/environment-maps/"

outputFileFormat = '{}_{}_{}-{:02d}'
environment = 'sunflowers_1k'
parameter = 'specularRoughness'
cachedInitParamVal = 0
sampleCount = 11

def setParameter(value):
    global material
    global parameter
    material.attr(parameter).set(value)

def getParameter():
    global material
    global parameter   
    return material.attr(parameter).get() 

def setOutputFileFormat(sample):
    global currentFilename

    filename = outputFileFormat.format(renderEngine, environment, parameter, int(sample*10))
    ext = "png"
    driver = pc.PyNode('defaultArnoldDriver')
    driver.ai_translator.set(ext)
    driver.pre.set(filename)
    currentFilename = filename + "." + ext


def renderImage(width, height):
    aR.arnoldRender(width, height, True, True, 'PBRCam', [ '-ofn "test"' ])


def setEnvironmentName(hdr_name):
    envMap = pc.PyNode('aiSkyDomeLightShape1')
    fileNode = envMap.inputs(t='file')
    fileNode[0].attr("fileTextureName").set(
        '{}{}.hdr'.format(dirEnvironmentMaps, hdr_name))
    return hdr_name

def retrieveCmdArgs():
    global environment
    global parameter
    global mayaFilePath

    def getCmdArgFromBack(i):
        return sys.argv[len(sys.argv) - (i+1)]

    if len(sys.argv) >= 3:
        environment = getCmdArgFromBack(0)
        parameter = getCmdArgFromBack(1)
        mayaFilePath = getCmdArgFromBack(2)

def validateParameter():
    global parameter
    if(parameter.lower() == "roughness"):
        print('Info: Maya has several material parameters for roughness. Will use "specularRoughness" instead of "{}".'.format(parameter))
        parameter = "specularRoughness"
    if(parameter.lower() == "metallic"):
        print('Info: Will use "metalness" instead of "{}".'.format(parameter))
        parameter = "metalness"
    if(parameter.lower() == "clearcoat"):
        print('Info: Will use "coat" instead of "{}".'.format(parameter))
        parameter = "coat"

def openMayaFile():
    global mayaFilePath
    global mayaProjectPath

    mayaProjectPath = os.path.abspath(mayaFilePath.rsplit('\\',2)[0])
    print("Project path: {}\nFile path: {}\nWill open file now...".format(mayaProjectPath, mayaFilePath))
    pc.mel.setProject(mayaProjectPath)
    pc.openFile(mayaFilePath, force=True)

def setOutputPath():
    global environment
    global parameter
    global currentOutputPath
    
    if(parameter == "specularRoughness"):
        paramFolder = "roughness"
    elif(parameter.lower() == "metalness"):
        paramFolder = "metallic"
    elif(parameter.lower() == "coat"):
        paramFolder = "clearcoat"
    else:
        paramFolder = parameter.lower()

    currentOutputPath = outputDir.format(paramFolder, environment)
    pc.workspace.fileRules['images'] = currentOutputPath

def moveFromTmpFolder():
    global mayaProjectPath
    global currentOutputPath
    global currentFilename

    absOutputPath = os.path.normpath(os.path.join(mayaProjectPath, currentOutputPath))

    current = os.path.join(absOutputPath,"tmp", currentFilename)
    target = os.path.join(absOutputPath,currentFilename)
    
    shutil.move(current, target)

def deleteTmpFolder():
    global mayaProjectPath
    global currentOutputPath

    absOutputPath = os.path.normpath(os.path.join(mayaProjectPath, currentOutputPath))

    tmpFolder = os.path.join(absOutputPath,"tmp")
    os.rmdir(tmpFolder)

# Main
retrieveCmdArgs()
validateParameter()

openMayaFile()

renderEngine = str(pc.PyNode('defaultRenderGlobals').currentRenderer.get())
material = pc.PyNode('maya_default')
cachedInitParamVal = getParameter()

if not environment == 'none':
    environment = setEnvironmentName(environment)

setOutputPath()

print("Renderer used: " + renderEngine)
print("Environment: " + environment)
print("Start rendering...\n=====\n")

for i in np.linspace(0.0, 1.0, sampleCount):
    setOutputFileFormat(i)
    setParameter(i)
    print("Current value of {}: {}".format(parameter, i))
    begin = time.time()
    renderImage(500, 500)
    end = time.time()
    print("Rendering time / duration: {} sec".format(end-begin))
    moveFromTmpFolder()


# reset to default material
setParameter(cachedInitParamVal)

deleteTmpFolder()
print("\nFinished rendering!")