# -*- coding: utf-8 -*-
"""One full control step through EmbodiedModel."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.model import EmbodiedModel

m = EmbodiedModel()
for t in (0.0, 0.25, 0.5):
    st = m.step(t, skill=1.0)
    print("t=%.2f  balance_margin=%.4f  fallen=%s  n_dof=%d" % (
        st["time"], st["balance_margin"], st["fallen"], st["n_dof"]))
