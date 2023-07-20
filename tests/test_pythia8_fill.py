import chromo
from chromo.common import EventData
from .util import run_in_separate_process


def init_pythia8():
    config = ["ProcessLevel:all = off" "ParticleDecays:tau0Max = 1e100"]
    pythia8 = chromo.models.Pythia8(seed=1, config=config, banner=False)
    return pythia8._pythia


def init_events(nevents):
    evt_kin = chromo.kinematics.FixedTarget(1e7, "p", "p")
    evt_gen = chromo.models.Sibyll23d(evt_kin)

    events = []
    for event in evt_gen(nevents):
        event = event.final_state()
        events.append(event.copy())

    return events


def get_pythia_event(pythia, evt_kin):
    pevent = pythia.event
    res = EventData(
        ("pythia", "pythia"),
        evt_kin,
        0,
        0.0,
        (0, 0),
        pevent.pid(),
        pevent.status(),
        pythia.charge(),
        pevent.px(),
        pevent.py(),
        pevent.pz(),
        pevent.en(),
        pevent.m(),
        pevent.vx(),
        pevent.vy(),
        pevent.vz(),
        pevent.vt(),
        pevent.parents(),
        pevent.children(),
    )
    return res.copy()


def append_result(pythia, event):
    pythia.event.reset()
    for i in range(len(event)):
        pythia.event.append(
            event.pid[i],
            91,
            0,
            0,
            event.px[i],
            event.py[i],
            event.pz[i],
            event.en[i],
            event.m[i],
        )
    return get_pythia_event(pythia, event.kin)


def fill_result(pythia, event):
    pythia.event.fill(
        event.pid, event.status + 90, event.px, event.py, event.pz, event.en, event.m
    )
    return get_pythia_event(pythia, event.kin)


def run_event_fill():
    """
    Tests that `pythia.event.fill` and `pythia.event.append`
    produce the same event stack

    `pythia.event.fill` is optimized version of `pythia.event.append`
    `pythia.event.fill` accepts numpy arrays instead of scalar value
    as for `pythia.event.append`.

    `pythia.event.fill` resets event stack by `pythia.event.reset()`
    and uses `pythia.event.append` in C++ loop
    """
    pythia = init_pythia8()
    for event in init_events(10):
        fill_res = fill_result(pythia, event)
        append_res = append_result(pythia, event)
        assert fill_res == append_res


def test_event_fill():
    run_in_separate_process(run_event_fill)
