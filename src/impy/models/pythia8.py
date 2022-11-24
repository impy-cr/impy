from impy.common import MCRun, MCEvent, CrossSectionData
from impy import impy_config
from impy.util import _cached_data_dir
from os import environ
import numpy as np


class PYTHIA8Event(MCEvent):
    """Wrapper class around HEPEVT particle stack."""

    _hepevt = "hepevt"

    def _charge_init(self, npart):
        return self._lib.charge_from_pid(
            self._lib.pythia.particleData, self._lib.hepevt.idhep[:npart]
        )

    def _get_impact_parameter(self):
        hi = self._lib.pythia.info.hiInfo
        if hi is None:
            return np.nan
        return hi.b

    def _get_n_wounded(self):
        hi = self._lib.pythia.info.hiInfo
        if hi is None:
            return (0, 0)
        return hi.nPartProj, hi.nPartTarg


class Pythia8(MCRun):
    _name = "Pythia"
    _version = "8.307"
    _library_name = "_pythia8"
    _event_class = PYTHIA8Event
    _output_frame = "center-of-mass"
    _restartable = True
    _data_url = (
        "https://github.com/impy-project/impy"
        + "/releases/download/zipped_data_v1.0/Pythia8_v001.zip"
    )

    def __init__(self, event_kinematics, seed=None, logfname=None):
        super().__init__(seed, logfname)

        self._lib.hepevt = self._lib.Hepevt()

        datdir = _cached_data_dir(self._data_url) + "xmldoc"

        # Must delete PYTHIA8DATA from environ if it exists, since it overrides
        # our argument here. When you install Pythia8 with conda, it sets
        # PYTHIA8DATA. If that version does not match this version, readString()
        # or init() may fail.
        if "PYTHIA8DATA" in environ:
            del environ["PYTHIA8DATA"]
        self._lib.pythia = self._lib.Pythia(datdir, True)

        # must come last
        self.event_kinematics = event_kinematics
        self._set_final_state_particles()

    def _cross_section(self, evt_kin):
        with self._temporary_evt_kin(evt_kin):
            st = self._lib.pythia.info.sigmaTot
            return CrossSectionData(
                st.sigmaTot,
                st.sigmaTot - st.sigmaEl,
                st.sigmaEl,
                st.sigmaAX,
                st.sigmaXB,
                st.sigmaXX,
                st.sigmaAXB,
            )

    def _set_event_kinematics(self, k):
        pythia = self._lib.pythia
        pythia.settings.resetAll()

        if not pythia.particleData.isParticle(k.p1pdg):
            raise ValueError(f"Particle {k.p1pdg} not recognized")

        if not pythia.particleData.isParticle(k.p2pdg):
            raise ValueError(f"Particle {k.p2pdg} not recognized")

        config = [
            "Random:setSeed = on",
            f"Random:seed = {self._seed}",
            # Specify energy in center of mass
            "Beams:frameType = 1",
            "SoftQCD:inelastic = on",
            # reduce verbosity
            "Print:quiet = on",
            "Next:numberCount = 0",  # do not print progress
        ]
        # Add more options from config file
        config += impy_config["pythia8"]["options"]

        if k.p1_is_nucleus or k.p2_is_nucleus:
            import warnings

            warnings.warn(
                "Support for nuclei is experimental; event generation takes a long time",
                RuntimeWarning,
            )

            # speed-up initialization by not fitting nuclear cross-section
            config.append("HeavyIon:SigFitNGen = 0")
            config.append("HeavyIon:SigFitDefPar = 10.79,1.75,0.30,0.0,0.0,0.0,0.0,0.0")

        config += [
            f"Beams:idA = {k.p1pdg}",
            f"Beams:idB = {k.p2pdg}",
            f"Beams:eCM = {k.ecm}",
        ]

        for line in config:
            if not pythia.readString(line):
                raise RuntimeError(f"readString('{line}') failed")

        # calling init several times is allowed
        if not pythia.init():
            raise RuntimeError("Pythia8 initialization failed")

    def _attach_log(self, fname):
        # not implemented
        pass

    def _set_stable(self, pdgid, stable):
        self._lib.pythia.particleData.mayDecay(pdgid, not stable)

    def _generate_event(self):
        success = self._lib.pythia.next()
        if success:
            # We copy over the event record from Pythia's internal buffer to our
            # Hepevt-like object. This is not efficient, but easier to
            # implement. The time needed to copy the record is small compared to
            # the time needed to generate the event. If this turns out to be a
            # bottleneck, we need to make Hepevt a view of the interval record.
            self._lib.hepevt.fill(self._lib.pythia.event)
        return success
