@echo off
set renderNames=eevee cycles
set parameterList=Roughness Metallic Specular Clearcoat

rem foreach renderer, parameter and environment map
rem render image in blender

for %%R in (%renderNames%) do (
for %%P in (%parameterList%) do (

blender -b "..\renderprojects\blender\directional-light.blend" -P "blender_RenderMatParam.py" %%P %%R none
))
pause