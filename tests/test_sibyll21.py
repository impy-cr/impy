from impy.kinematics import CenterOfMass
from impy.models import Sibyll21
from impy.constants import TeV
from numpy.testing import assert_allclose, assert_equal
import numpy as np
from .util import reference_charge, run_in_separate_process
import pytest
from particle import Particle


def event_run():
    evt_kin = CenterOfMass(10 * TeV, 2212, 2212)
    m = Sibyll21(evt_kin, seed=1)
    for event in m(1):
        pass
    return event.copy()  # copy is pickleable


@pytest.fixture
def event():
    return run_in_separate_process(event_run)


@pytest.mark.xfail(reason="needs a fix to sibylls ICHP table")
def test_charge(event):
    expected = reference_charge(event.pid)
    assert_allclose(event.charge, expected)


def test_children(event):
    assert event.children is None


def test_parents(event):
    # check that there are particles with a single parent
    # and that parent is short-lived or an initial particle

    d = event.parents[:, 1] - event.parents[:, 0]
    ma = (d == 0) & (event.parents[:, 0] > 0)

    assert np.sum(ma) > 0

    idx = event.parents[ma, 0] - 1

    # remove beam particles (if any)
    ma = event.status[idx] != 3
    idx = idx[ma]

    # remaining particles should be short-lived or
    # bookkeeping particles like K0
    for pid in event.pid[idx]:
        p = Particle.from_pdgid(pid)
        assert p.ctau is None or p.ctau < 1


def test_vertex(event):
    # no vertex info in Sibyll21
    assert_equal(event.vx, 0)
    assert_equal(event.vy, 0)
    assert_equal(event.vz, 0)
    assert_equal(event.vt, 0)
