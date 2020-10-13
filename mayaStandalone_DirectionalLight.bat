@echo off
set parameterList=metalness coat specular roughness diffuseRoughness

rem foreach parameter and environment map
rem render image in maya with arnold

for %%P in (%parameterList%) do (

mayapy mayaStandalone_RenderMatParam.py "..\renderprojects\maya\PBRMaterialModels\scenes\directional-light.ma" %%P none
)
pause