@echo off
set renderNames=eevee cycles
set parameterList=Roughness Metallic Specular Clearcoat

rem foreach renderer, parameter and environment map
rem render image in blender

for %%R in (%renderNames%) do (
for %%P in (%parameterList%) do (
for /f "tokens=*" %%f in ('dir ..\data\environment-maps /b^|findstr .*.hdr') do (

blender -b "..\renderprojects\blender\basic-scene.blend" -P "blender_RenderMatParam.py" %%P %%R %%~nf 
)))
pause