# PBRMaterialModels
Code for my bachelor thesis "Comparison of material models in modern physically based rendering pipelines", submitted in August 2020 at the Stuttgart Media University

## Introduction

To investigate how the PBR material models of the chosen rendering tools differ in terms of the quality and range of reproducible materials, several images depicting an object with different material properties in a certain lighting condition were generated. The material property is influenced by exactly one parameter at a time. Each time the value of the parameter is incremented with a specific step size, a new image is created. This results in a row of images for each rendering tool, which are contrasted in a table, also referred to as **material chart**.

Within the context of my paper, four material parameters are examined in more detail (*Roughness*, *Specular*, *Metallic*, *Clearcoat*).
The so far examined shader models are:
- the “Principled BSDF” in Blender
- the “Standard Surface” shader in Arnold
- the “Default Lit” or “Clear Coat” model (to evaluate Clearcoat respectively) in the Unreal Engine

## General setup

In general, the rendering framework is controlled via command line. The user can specify an arbitrary parameter name and HDRi image for IBL (if the source image is provided in the appropriate folder).

The general syntax is:
`renderer projectscene pythonscript [renderengine] parameter environment-name`

However, the actual syntax differs between each software tool.

## Maya

`mayapy python-script scene parameter environment-name`

## Blender

`blender -b scene -P python-script render-engine parameter environment-name`

## Unreal Engine

In this case, the logic is partly implemented in blueprints and partly in the provided Python script. If requested, I can provide the Unreal project including the blueprints as well.

The taken approach was to start the application (i.e. game), increment the chosen material parameter while in game mode, render the scene by taking a “high resolution screenshot” and automatically stop the application when the last value has been rendered.

However, Python scripts can only start a level in the so-called “Simulate” mode, that is a game mode without any player controller. As the scene camera cannot be assigned to any player entity, only the editor camera is available. This is a disadvantage because the final image does not necessarily correspond to the result of a digital production. Nevertheless, the renderings should not differ too much since the editor option “Game View” was activated before starting the rendering process.
