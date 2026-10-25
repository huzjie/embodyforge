# -*- coding: utf-8 -*-
"""Dance routines.

A routine is a sequence of ``(clip_name, beat_count)`` steps scheduled on a
shared tempo (beats per minute). ``beat_to_time`` maps a beat index to absolute
time; ``pose_at`` walks the schedule to produce the full-body pose at any time,
blending the active clip with the robot's walk cycle.
"""
from .library import build_default_library


def _bpm_to_spb(bpm):
    return 60.0 / max(bpm, 1e-6)


class DanceRoutine:
    def __init__(self, schedule, bpm=120.0, library=None):
        self.schedule = schedule      # [(clip_name, beats), ...]
        self.bpm = bpm
        self.library = library or build_default_library()
        self.spb = _bpm_to_spb(bpm)

    def total_beats(self):
        return sum(b for _, b in self.schedule)

    def duration(self):
        return self.total_beats() * self.spb

    def clip_at(self, t):
        elapsed = 0.0
        for name, beats in self.schedule:
            seg = beats * self.spb
            if t < elapsed + seg:
                local = (t - elapsed) / seg
                return name, local
            elapsed += seg
        return self.schedule[-1][0], 1.0

    def pose_at(self, t):
        name, local = self.clip_at(t)
        clip = self.library.get(name)
        if clip is None:
            return {}
        return clip.pose_at(clip.duration() * local)


def build_dance_routine(bpm=120.0):
    schedule = [
        ("idle", 2),
        ("wave", 4),
        ("step_touch", 4),
        ("squat", 4),
        ("spin", 4),
        ("wave", 4),
        ("idle", 2),
    ]
    return DanceRoutine(schedule, bpm=bpm)
