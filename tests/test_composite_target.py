from impy.constants import GeV
from impy.kinematics import CenterOfMass, CompositeTarget
import impy.models as im
from collections import Counter
import pytest
from .util import run_in_separate_process
from impy.util import get_all_models


# generate list of models to test, skip models which do not support nuclei
Models = get_all_models(
    skip=(im.Sophia20, im.Phojet112, im.Phojet191, im.Phojet193, im.Pythia6)
)


def run_model(Model, evt_kin):
    gen = Model(evt_kin, seed=1)

    c = Counter()
    for event in gen(10):
        ev = event.final_state()
        assert len(ev.pid) > 0
        c.update(ev.pid)

    return c


@pytest.mark.parametrize("Model", Models)
def test_composite_target(Model):
    if Model is im.Pythia8:
        pytest.skip("Switching beams in Pythia8 is very time-consuming")

    projectile = "pi-"
    target = CompositeTarget(
        [
            ("N14", 2 * 0.78084),
            ("O16", 2 * 0.20946),
            ("O16", 0.004),
            ("proton", 2 * 0.004),
        ],
        "Air without argon",
    )

    evt_kin = CenterOfMass(10 * GeV, projectile, target)

    c = run_in_separate_process(run_model, Model, evt_kin)

    assert c[211] > 0, "pi+"
    assert c[-211] > 0, "pi-"
    assert c[2212] > 0, "p"
