# -*- coding: utf-8 -*-
"""Formation control: target slots and tracking error."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embodyforge.orchestra.formation import FormationController

for pattern in ("grid", "circle", "line"):
    f = FormationController(pattern)
    targets = f.targets(9)
    print("%-7s targets: %s" % (pattern, [[round(x, 2) for x in t[:2]] for t in targets[:3]], ))
