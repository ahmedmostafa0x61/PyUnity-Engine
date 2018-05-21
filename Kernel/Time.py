"""
    This is the Time module.

    -- Author : AbdElAziz Mofath
    -- Date: 4th of April 2018 at 11:40 PM
"""

import time as tm

deltaTime = 0.0
fixedTime = 0.0
__previousTime = tm.time()
__startTime = tm.time()


def __UpdateDeltaTime():
    """
        Update the timing of the game.
        * Call every frame
    """
    global deltaTime, __previousTime, fixedTime

    deltaTime = __Clamp(tm.time() - __previousTime, 0.0001, 10)
    fixedTime = tm.time() - __startTime
    __previousTime = tm.time()


def __SleepTimeToLockFramsOn(fps):
    """
        Force the main thread to sleep the exact amount of time to make sure that the game is locked at target fps.
        * the actual fps will be <= target fps. 5% tolerance.
    :param fps: frame rate be second
    """
    global __previousTime
    NormalSleepTime = 1. / fps
    ElapsedTime = tm.time() - __previousTime
    SleepTime = __Clamp(NormalSleepTime - ElapsedTime, 0, NormalSleepTime)
    tm.sleep(SleepTime)


def __Clamp(value, min_val, max_val):
    """
    :return: the float equals value if value in range(min, max), else min if value < min, otherwise max.
    """
    if value <= min_val:
        return min_val

    if value >= max_val:
        return max_val

    return value
