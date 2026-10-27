"""A deliberately broken checker used only for the red/green negative control.

It monkeypatches exact_patterns to the old, too-small padding, so the padding
regression test must fail.  The unmodified suite is run separately and passes.
"""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import star  # noqa: E402
import test_star  # noqa: E402

original = star.Experiment2Config.exact_patterns


def too_small(self, S, padding=None):
    return original(self, S, padding=1)


star.Experiment2Config.exact_patterns = too_small

suite = unittest.TestLoader().loadTestsFromName(
    "test_star.StarTests.test_padding_regression"
)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
