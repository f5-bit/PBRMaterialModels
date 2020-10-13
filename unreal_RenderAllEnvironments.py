import unreal
import time
asset_path = "/Game/HDRi/"

all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
all_assets = unreal.EditorAssetLibrary.list_assets(asset_path)
all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]
texture_cube_assets = unreal.EditorFilterLibrary.by_class(all_assets_loaded, unreal.TextureCube)

envIndex = -1
tickhandle = None

def startGame():
    unreal.EditorLevelLibrary.editor_play_simulate()

def endGame():
    unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_game_world(), "Exit")

def exchangeEnvironment(index):
    global all_actors
    global texture_cube_assets

    if not len(texture_cube_assets) > 0:
        unreal.log_error("No cubemap textures found!")
    else:
        for actor in all_actors:
            if not actor.get_name().find("light_HDRIBackdrop") == -1: # get HDRIBackdrop actor in scene
                actor.set_editor_property("Cubemap", texture_cube_assets[index])
                unreal.log_warning("New cubemap: {}".format(actor.get_editor_property("Cubemap")))
                #unreal.EditorLevelLibrary.save_current_level()

def renderAllEnvironments(deltaTime):
    global envIndex
    global texture_cube_assets

    # check if game has been quit: no game world = no running game
    # (could not find a better solution in the API)
    if(unreal.EditorLevelLibrary.get_game_world() == None):
        envIndex += 1
        if(envIndex < len(texture_cube_assets) and envIndex >= 0):
            exchangeEnvironment(envIndex)
            startGame()
        else:
            unreal.unregister_slate_pre_tick_callback(tickhandle)
    else:
        unreal.log_warning("game still running.")


tickhandle = unreal.register_slate_pre_tick_callback(renderAllEnvironments)


