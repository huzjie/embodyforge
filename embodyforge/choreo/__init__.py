# -*- coding: utf-8 -*-
"""Choreography: keyframe motion library and beat-synchronized dance routines."""
from .keyframe import Keyframe, MotionClip, interpolate_clip
from .library import MotionLibrary, build_default_library
from .dance import DanceRoutine, build_dance_routine

__all__ = [
    "Keyframe", "MotionClip", "interpolate_clip",
    "MotionLibrary", "build_default_library",
    "DanceRoutine", "build_dance_routine",
]
