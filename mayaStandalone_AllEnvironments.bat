@echo off
set parameterList=metalness coat specular roughness diffuseRoughness

rem foreach parameter and environment map
rem render image in maya with arnold

for %%P in (%parameterList%) do (
for /f "tokens=*" %%f in ('dir ..\data\environment-maps /b^|findstr .*.hdr') do (

mayapy mayaStandalone_RenderMatParam.py "..\renderprojects\maya\PBRMaterialModels\scenes\basic-scene.ma" %%P %%~nf
))
pause