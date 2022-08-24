"""
Created on 14.04.2014

@author: afedynitch
"""

from impy.common import MCRun, MCEvent
from impy import impy_config
from impy.util import info


class DpmjetIIIEvent(MCEvent):
    """Wrapper class around DPMJET-III HEPEVT-style particle stack."""

    _hepevt = "dtevt1"
    _phep = "phkk"
    _vhep = "vhkk"
    _nevhep = "nevhkk"
    _nhep = "nhkk"
    _idhep = "idhkk"
    _isthep = "isthkk"
    _jmohep = "jmohkk"
    _jdahep = "jdahkk"

    def _charge_init(self, npart):
        return self._lib.dtpart.iich[self._lib.dtevt2.idbam[:npart] - 1]

    # Nuclear collision parameters
    @property
    def impact_parameter(self):
        """Returns impact parameter for nuclear collisions."""
        return self._lib.dtglcp.bimpac

    @property
    def n_wounded_A(self):
        """Number of wounded nucleons side A"""
        return self._lib.dtglcp.nwasam

    @property
    def n_wounded_B(self):
        """Number of wounded nucleons side B"""
        return self._lib.dtglcp.nwbsam

    @property
    def n_wounded(self):
        """Number of total wounded nucleons"""
        return self._lib.dtglcp.nwasam + self._lib.dtglcp.nwbsam

    # Unfortunately not that simple since this is bounced through
    # entire code as argument not in COMMON
    # @property
    # def n_inel_NN_interactions(self):
    #     """Number of inelastic nucleon-nucleon interactions"""
    #     return self.lib.dtglcp.nwtsum


# =========================================================================
# DpmjetIIIMCRun
# =========================================================================
class DpmjetIIIRun(MCRun):
    """Implements all abstract attributes of MCRun for the
    DPMJET-III series of event generators.

    It should work identically for the new 'dpmjet3' module and the legacy
    dpmjet306. No special constructor is necessary and everything is
    handled by the default constructor of the base class.
    """

    def sigma_inel(self, precision="default"):
        """Inelastic cross section according to current
        event setup (energy, projectile, target)"""
        k = self._curr_event_kin
        info(10, "Cross section for", k.A1, k.A2, self.lib.idt_icihad(k.p1pdg))
        if precision == "default":
            self.lib.dt_xsglau(
                k.A1, k.A2, self.lib.idt_icihad(k.p1pdg), 0, 0, k.ecm, 1, 1, 1
            )
        else:
            prev_precision = self.lib.dtglgp.jstatb
            # Set number of trials for Glauber model integration
            self.lib.dtglgp.jstatb = int(precision)
            self.lib.dt_xsglau(
                k.A1, k.A2, self.lib.idt_icihad(k.p1pdg), 0, 0, k.ecm, 1, 1, 1
            )
            self.lib.dtglgp.jstatb = prev_precision

        return self.lib.dtglxs.xspro[0, 0, 0]

    def _dpmjet_tup(self):
        """Constructs an tuple of arguments for calls to event generator
        from given event kinematics object."""
        k = self._curr_event_kin
        info(
            20,
            "Request DPMJET ARGs tuple:\n",
            (k.A1, k.Z1, k.A2, k.Z2, self.lib.idt_icihad(k.p1pdg), k.elab),
        )
        return (k.A1, k.Z1, k.A2, k.Z2, self.lib.idt_icihad(k.p1pdg), k.elab)

    def _set_event_kinematics(self, event_kinematics):
        """Set new combination of energy, momentum, projectile
        and target combination for next event."""
        info(5, "Setting event kinematics")
        assert (
            event_kinematics.A1 <= self._max_A1 and event_kinematics.A2 <= self._max_A2
        ), "Maximal initialization mass exceeded {0}/{1}, {2}/{3}".format(
            event_kinematics.A1, self._max_A1, event_kinematics.A2, self._max_A2
        )

        self._curr_event_kin = event_kinematics

        # AF: No idea yet, but apparently this functionality was around?!
        # if hasattr(k, 'beam') and hasattr(self.lib, 'init'):
        #     print(self.class_name + "::_set_event_kinematics():" +
        #           "setting beam params", k.beam)
        #     self.lib.dt_setbm(k.A1, k.Z1, k.A2, k.Z2, k.beam[0], k.beam[1])
        #     print 'OK'

    def attach_log(self, fname=None):
        """Routes the output to a file or the stdout."""
        fname = impy_config["output_log"] if fname is None else fname
        if fname == "stdout":
            lun = 6
            info(5, "Output is routed to stdout.")
        else:
            lun = self._attach_fortran_logfile(fname)
            info(5, "Output is routed to", fname, "via LUN", lun)

        if hasattr(self.lib, "dtflka"):
            self.lib.dtflka.lout = lun
            self.lib.dtflka.lpri = 50
        elif hasattr(self.lib, "dtiont"):
            self.lib.dtiont.lout = lun
        else:
            raise Exception("Unknown DPMJET version, IO common block not detected.")

        self.lib.pydat1.mstu[10] = lun

    def init_generator(self, event_kinematics, seed="random", logfname=None):
        from impy.util import fortran_chars
        from impy.constants import sec2cm
        from random import randint

        self._abort_if_already_initialized()

        if seed == "random":
            seed = randint(1000000, 10000000)
        else:
            seed = int(seed)
        info(5, "Using seed:", seed)

        # Save maximal mass that has been inisialized
        # (DPMJET sometimes crashes if higher mass requested than initialized)
        self._max_A1 = event_kinematics.A1
        self._max_A2 = event_kinematics.A2

        self._set_event_kinematics(event_kinematics)
        k = self._curr_event_kin
        dpm_conf = impy_config["dpmjetIII"]

        info(1, "Initializing DPMJET-III")
        # Set the dpmjpar.dat file
        if hasattr(self.lib, "pomdls") and hasattr(self.lib.pomdls, "parfn"):
            pfile = dpm_conf["param_file"][self.version]
            info(3, "DPMJET parameter file at", pfile)
            self.lib.pomdls.parfn = fortran_chars(self.lib.pomdls.parfn, pfile)

        # Set the data directory for the other files
        if hasattr(self.lib, "poinou") and hasattr(self.lib.poinou, "datdir"):
            pfile = dpm_conf["dat_dir"][self.version]
            info(3, "DPMJET data dir is at", pfile)
            self.lib.poinou.datdir = fortran_chars(self.lib.poinou.datdir, pfile)
            self.lib.poinou.lendir = len(pfile)

        if hasattr(self.lib, "dtimpy"):
            evap_file = dpm_conf["evap_file"][self.version]
            info(3, "DPMJET evap file at", evap_file)
            self.lib.dtimpy.fnevap = fortran_chars(self.lib.dtimpy.fnevap, evap_file)

        self.attach_log(logfname)
        self.lib.dt_init(-1, k.plab, k.A1, k.Z1, k.A2, k.Z2, k.p1pdg, iglau=0)

        # Set seed of random number generator
        sseed = str(seed)
        n1, n2, n3, n4 = (
            int(sseed[0:2]),
            int(sseed[2:4]),
            int(sseed[4:6]),
            int(sseed[6:]),
        )
        self.lib.dt_rndmst(n1, n2, n3, n4)

        if impy_config["user_frame"] == "center-of-mass":
            self.lib.dtflg1.iframe = 2
            self._output_frame = "center-of-mass"
        elif impy_config["user_frame"] == "laboratory":
            self.lib.dtflg1.iframe = 1
            self._output_frame = "laboratory"

        # Relax momentum and energy conservation checks at very high energies
        if k.ecm > 5e4:
            # Relative allowed deviation
            self.lib.pomdls.parmdl[76] = 0.045
            # Absolute allowed deviation
            self.lib.pomdls.parmdl[77] = 0.395
            # Relax threshhold of rejected events for variable energy runs
            self.lib.pomdls.ipamdl[178] = 5000

        # Relax momentum and energy conservation checks at very high energies
        if k.ecm > 5e4:
            # Relative allowed deviation
            self.lib.pomdls.parmdl[76] = 0.05
            # Absolute allowed deviation
            self.lib.pomdls.parmdl[77] = 0.05

        # if self.def_settings:
        #     print self.class_name + "::init_generator(): Using default settings:", \
        #         self.def_settings.__class__.__name__
        #     self.def_settings.enable()

        self._define_default_fs_particles()
        # Prevent DPMJET from overwriting decay settings
        # self.lib.dtfrpa.ovwtdc = False
        # Set PYTHIA decay flags to follow all changes to MDCY
        self.lib.pydat1.mstj[21 - 1] = 1
        self.lib.pydat1.mstj[22 - 1] = 2
        # # Set ctau threshold in PYTHIA for the default stable list
        self.lib.pydat1.parj[70] = impy_config["tau_stable"] * sec2cm * 10.0  # mm

    def set_stable(self, pdgid, stable=True):
        if abs(pdgid) == 2212:
            return
        kc = self.lib.pycomp(pdgid)
        if stable:
            self.lib.pydat3.mdcy[kc - 1, 0] = 0
            info(5, "defining", pdgid, "as stable particle")
        else:
            self.lib.pydat3.mdcy[kc - 1, 0] = 1
            info(5, "forcing decay of", pdgid)

    def generate_event(self):
        reject = self.lib.dt_kkinc(*self._dpmjet_tup(), kkmat=-1)
        self.lib.dtevno.nevent += 1
        return reject


class DpmjetIII191(DpmjetIIIRun):
    def __init__(self, event_kinematics, seed="random", logfname=None):
        from impy.definitions import interaction_model_by_tag as models_dict

        interaction_model_def = models_dict["DPMJETIII191"]
        super().__init__(interaction_model_def)
        self.init_generator(event_kinematics, seed, logfname)


class DpmjetIII193(DpmjetIIIRun):
    def __init__(self, event_kinematics, seed="random", logfname=None):
        from impy.definitions import interaction_model_by_tag as models_dict

        interaction_model_def = models_dict["DPMJETIII193"]
        super().__init__(interaction_model_def)
        self.init_generator(event_kinematics, seed, logfname)


class DpmjetIII306(DpmjetIIIRun):
    def __init__(self, event_kinematics, seed="random", logfname=None):
        from impy.definitions import interaction_model_by_tag as models_dict

        interaction_model_def = models_dict["DPMJETIII306"]
        super().__init__(interaction_model_def)
        self.init_generator(event_kinematics, seed, logfname)
