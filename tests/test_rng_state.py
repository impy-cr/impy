from impy.kinematics import FixedTarget, CenterOfMass
from impy.constants import TeV, GeV
import impy.models as im
import pickle
import pytest
from .util import run_in_separate_process
from impy.util import get_all_models


def run_rng_state(Model):
    if Model is im.Sophia20:
        evt_kin = FixedTarget(13 * TeV, "photon", "proton")
    elif Model is im.UrQMD34:
        evt_kin = CenterOfMass(50 * GeV, "proton", "proton")
    else:
        evt_kin = CenterOfMass(13 * TeV, "proton", "proton")

    generator = Model(evt_kin, seed=1)
    nevents = 10

    # Save a initial state to a variable:
    state_0 = generator.random_state.copy()

    # Generate nevents events
    counters = []
    for _ in generator(nevents):
        counters.append(generator.random_state.counter)

    # Pickle generator state after nevents
    pickled_state_1 = pickle.dumps(generator.random_state)

    # Restore initial state from variable
    generator.random_state = state_0

    # Compare counters after each generated event
    for i, _ in enumerate(generator(nevents)):
        counter = generator.random_state.counter
        assert counters[i] == counter, (
            f"Counters for seed {generator.random_state.seed} "
            f"after {i+1} event are different\n"
            f"  expected(previous) = {counters[i]}, received(current) = {counter}"
        )

    state_1a = generator.random_state
    state_1 = pickle.loads(pickled_state_1)

    # check that pickled state_1 and reproduced state_1a are equal
    assert state_1a == state_1, "Restored state from file is different from obtained"


@pytest.mark.parametrize("Model", get_all_models())
def test_rng_state(Model):
    if Model is im.Pythia8:
        pytest.skip("Pythia8 currently does not support rng_state serialization")

    if Model is im.UrQMD34:
        pytest.xfail("UrQMD fails this test for most seeds, needs investigation")

    run_in_separate_process(run_rng_state, Model)
