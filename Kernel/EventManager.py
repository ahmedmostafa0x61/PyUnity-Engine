"""
    This is the Engine module.

    -- Author : AbdElAziz Mofath
    -- Date: 5th of April 2018 at 12:10 AM
"""

import UserAssets.Scripts
import Kernel.Physics
import importlib.util
import Kernel.Time
import OpenGL.GL
import gc
import os

__world_id_counter = 1000
__script_module = {}

__start = {}
__render = {}
__update = {}
__events = {}
__late_update = {}

__born_scripts = []
__dead_scripts = []
__disables_scripts = []

gc_time = 0.0


def loadScripts():
    scriptsPath = os.path.dirname(UserAssets.Scripts.__file__)
    scripts = os.listdir(scriptsPath)

    for script in scripts:
        if script[:2] == 's_':
            __LoadScript('UserAssets.Scripts.' + script[:-3])


def __LoadScript(script):
    global __world_id_counter, __script_module
    __world_id_counter = __world_id_counter + 1

    metaData = importlib.util.find_spec(script)
    ObjectModule = importlib.util.module_from_spec(metaData)
    metaData.loader.exec_module(ObjectModule)

    if hasattr(ObjectModule, '__id__'):
        current_id = ObjectModule.__id__
    else:
        setattr(ObjectModule, '__id__', __world_id_counter)
        current_id = __world_id_counter

    __script_module[current_id] = ObjectModule
    subscribeStart(current_id, hasattr(ObjectModule, 'Start'))
    subscribeUpdate(current_id, hasattr(ObjectModule, 'Update'))
    subscribeRender(current_id, hasattr(ObjectModule, 'Render'))
    subscribeEvents(current_id, hasattr(ObjectModule, 'Events'))
    subscribeLateUpdate(current_id, hasattr(ObjectModule, 'LateUpdate'))


def __DisableScript(script_id):
    __disables_scripts.append(script_id)


def __EnableScript(script_id):
    global __script_module

    subscribeStart(script_id, hasattr(__script_module[script_id], 'Start'))
    subscribeUpdate(script_id, hasattr(__script_module[script_id], 'Update'))
    subscribeRender(script_id, hasattr(__script_module[script_id], 'Render'))
    subscribeEvents(script_id, hasattr(__script_module[script_id], 'Events'))
    subscribeLateUpdate(script_id, hasattr(__script_module[script_id], 'LateUpdate'))
    Kernel.Physics.__EnableCollider(script_id)


def __SendMeggage(script_id, method_name, *args):
    global __script_module

    if script_id in __script_module:
        if hasattr(__script_module[script_id], method_name):
            method = getattr(__script_module[script_id], method_name)
            if len(args) > 0:
                method(*args)
            else:
                method()


def __DestroyScript(script_id):
    global __dead_scripts

    if not (script_id in __dead_scripts):
        __dead_scripts.append(script_id)


def __InstantiateScript(prefab_name):
    global __born_scripts
    prefab_module, prefab_id = __LoadPrefab('UserAssets.Prefabs.' + prefab_name)
    __born_scripts.append((prefab_module, prefab_id))

    if hasattr(prefab_module, 'Start'):
        prefab_module.Start()

    return prefab_module


def __GetScript(script_id):
    global __script_module
    if script_id in __script_module:
        return __script_module[script_id]
    return None


def subscribeStart(current_id, status):
    global __start
    __start[current_id] = status


def subscribeRender(current_id, status):
    global __render
    __render[current_id] = status


def subscribeUpdate(current_id, status):
    global __update
    __update[current_id] = status


def subscribeLateUpdate(current_id, status):
    global __late_update
    __late_update[current_id] = status


def subscribeEvents(current_id, status):
    __events[current_id] = status


def __CastEvent(event_name, *args):
    for subscriber in __script_module:
        if __events[subscriber]:
            __script_module[subscriber].Events(event_name, *args)


def castStart():
    for subscriber in __script_module:
        if __start[subscriber]:
            __script_module[subscriber].Start()


def castRender():
    global __render
    # first we sort the objects based on the distance from the camera.
    list_of_rendering = [__script_module[x] for x in __script_module if __render[x]]

    def sortingKey(gameObject):
        if hasattr(gameObject, 'transform') is True:
            return gameObject.transform.position.z
        return 0

    list_of_rendering.sort(key=sortingKey, reverse=True)

    # then we render
    for obj in list_of_rendering:
        OpenGL.GL.glPushMatrix()
        obj.Render()
        OpenGL.GL.glPopMatrix()


def castUpdate():
    for subscriber in __script_module:
        if __update[subscriber]:
            __script_module[subscriber].Update()


def castLateUpdate():
    for subscriber in __script_module:
        if __late_update[subscriber]:
            __script_module[subscriber].LateUpdate()


def collectGarbage():
    global __dead_scripts, __start, __render, __update, __late_update, __script_module, gc_time
    if len(__dead_scripts) > 0:
        for obj in __dead_scripts:

            if obj in __start:
                del __start[obj]

            if obj in __render:
                del __render[obj]

            if obj in __update:
                del __update[obj]

            if obj in __late_update:
                del __late_update[obj]

            if obj in __script_module:
                del __script_module[obj]

            Kernel.Physics.__DestroyCollider(obj)

        __dead_scripts = []

    if Kernel.Time.fixedTime >= gc_time + 1:
        gc_time = Kernel.Time.fixedTime
        gc.collect()


def __LoadPrefab(prefab):
    global __world_id_counter
    __world_id_counter = __world_id_counter + 1

    metaData = importlib.util.find_spec(prefab)
    ObjectModule = importlib.util.module_from_spec(metaData)
    setattr(ObjectModule, '__id__', __world_id_counter)
    metaData.loader.exec_module(ObjectModule)

    return ObjectModule, __world_id_counter


def __HookPrefab(prefabModule, prefab_id):
    __script_module[prefab_id] = prefabModule

    subscribeStart(prefab_id, hasattr(prefabModule, 'Start'))
    subscribeUpdate(prefab_id, hasattr(prefabModule, 'Update'))
    subscribeRender(prefab_id, hasattr(prefabModule, 'Render'))
    subscribeEvents(prefab_id, hasattr(prefabModule, 'Events'))
    subscribeLateUpdate(prefab_id, hasattr(prefabModule, 'LateUpdate'))


def updateDictionary():
    global __born_scripts, __script_module, __disables_scripts
    global __start, __render, __update, __late_update

    if len(__born_scripts) > 0:
        for prefab_module, prefab_id in __born_scripts:
            __script_module[prefab_id] = prefab_module
            __HookPrefab(prefab_module, prefab_id)

    if len(__disables_scripts) > 0:
        for  script_id in __disables_scripts:
            if script_id in __start:
                __start[script_id] = False

            if script_id in __render:
                __render[script_id] = False

            if script_id in __update:
                __update[script_id] = False

            if script_id in __late_update:
                __late_update[script_id] = False

            Kernel.Physics.__DisableCollider(script_id)

    __disables_scripts = []
    __born_scripts = []