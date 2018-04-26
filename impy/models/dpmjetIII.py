'''
Created on 14.04.2014

@author: afedynitch
'''

import numpy as np
from impy.common import MCRun, MCEvent, impy_config
from impy.util import standard_particles, info


class DpmjetIIIMCEvent(MCEvent):
    """Wrapper class around DPMJET-III particle stack."""

    def __init__(self, lib, event_config):
        # HEPEVT (style) common block
        evt = lib.dtevt1
        # Number of entries on stack
        npart = evt.nhkk

        # Filter stack for charged particles if selected
        if impy_config["event_scope"] == 'charged':
            sel = np.where((evt.isthkk[:npart] == 1) & (
                lib.dtpart.iich[lib.dtevt2.idbam[:npart] - 1] != 0))
        elif impy_config["event_scope"] == 'stable':
            sel = np.where(evt.isthkk[:npart] == 1)
        else:
            raise Exception("not implemented, yet")

        # Save selector for implementation of on-demand properties
        self.sel = sel

        MCEvent.__init__(
            self,
            event_config=event_config,
            lib=lib,
            px=evt.phkk[0, sel][0],
            py=evt.phkk[1, sel][0],
            pz=evt.phkk[2, sel][0],
            en=evt.phkk[3, sel][0],
            p_ids=evt.idhkk[sel],
            npart=npart)

    @property
    def charge(self):
        return self.lib.dtpart.iich[lib.dtevt2.idbam[sel] - 1]

    @property
    def mass(self):
        return self.lib.dtevt1.phkk[4, self.sel][0]


#=========================================================================
# DpmjetIIIMCRun
#=========================================================================
class DpmjetIIIMCRun(MCRun):
    """Implements all abstract attributes of MCRun for the 
    DPMJET-III series of event generators.
    
    It should work identically for the new 'dpmjet3' module and the legacy
    dpmjet306.
    """

    def __init__(self, libref, event_class=None, **kwargs):

        if event_class is None:
            self.event_class = DpmjetIIIMCEvent
        else:
            self.event_class = event_class

        MCRun.__init__(self, libref, **kwargs)

    @property
    def name(self):
        """Event generator name"""
        return "DPMJET"

    @property
    def version(self):
        """Event generator version"""
        # Needs some sort of smart handling here
        return "III-2018.1"

    def get_sigma_inel(self):
        """Inelastic cross section according to current
        event setup (energy, projectile, target)"""
        k = self.evkin
        self.lib.dt_xsglau(k.A1, k.A2, self.lib.idt_icihad(k.p1pdg), 0, 0,
                           k.ecm, 1, 1, 1)
        return self.lib.dtglxs.xspro[0, 0, 0]

    def _dpmjet_tup(self, event_kinematics):
        """Constructs an tuple of arguments for calls to event generator
        from given event kinematics object."""
        k = event_kinematics
        return k.A1, k.Z1, k.A2, k.Z2, self.lib.idt_icihad(k.p1pdg), k.elab

    def set_event_kinematics(self, event_kinematics):
        """Set new combination of energy, momentum, projectile
        and target combination for next event."""
        k = event_kinematics

        # AF: No idea yet, but apparently this functionality was around?!
        # if hasattr(k, 'beam') and hasattr(self.lib, 'init'):
        #     print(self.class_name + "::set_event_kinematics():" +
        #           "setting beam params", k.beam)
        #     self.lib.dt_setbm(k.A1, k.Z1, k.A2, k.Z2, k.beam[0], k.beam[1])
        #     print 'OK'
        self.event_config['event_kinematics'] = event_kinematics

    def attach_log(self):
        """Routes the output to a file or the stdout."""
        fname = impy_config['output_log']
        if fname == 'stdout':
            self.lib.dtflka.lout = 6
            self.lib.dtflka.lpri = 50
            self.lib.pydat1.mstu[10] = 6
            info(5, 'Output is routed to stdout.')
        else:
            lun = self._attach_fortran_logfile(fname)
            self.lib.dtiont.lout = lun
            self.lib.pydat1.mstu[10] = lun
            info(5, 'Output is routed to', fname, 'via LUN', lun)

    def init_generator(self, config):

        # Comprise DPMJET input from the event kinematics object
        k = self.evkin

        dpm_conf = impy_config['dpmjet']

        # print self.class_name + "::init_generator(): calling init with:", \
        #     - 1, k.elab, PM, PCH, TM, TCH, k.p1pdg

        # Set the dpmjpar.dat file
        pfile = dpm_conf['param_file']['III-2018.1']
        self.lib.pomdls.parfn[0:len(pfile)] = pfile

        self.lib.dt_init(
            -1,
            dpm_conf['e_max'],
            k.A1, 
            k.Z1, 
            k.A2, 
            k.Z2,
            k.p1pdg,
            iglau=1)
        # Put protection to not run this stuff again
        self.lib.init = True

        if dpm_conf['user_frame'] == 'center-of-mass':
            self.lib.dtflg1.iframe = 2
        elif dpm_conf['user_frame'] == 'laboratory':
            self.lib.dtflg1.iframe = 1

        # if self.def_settings:
        #     print self.class_name + "::init_generator(): Using default settings:", \
        #         self.def_settings.__class__.__name__
        #     self.def_settings.enable()

        # Set pi0 stable
        self.set_stable(111)

        if 'stable' in self.event_config:
            for pdgid in self.event_config['stable']:
                self.set_stable(pdgid)

    def set_stable(self, pdgid):
        kc = self.lib.pycomp(pdgid)
        self.lib.pydat3.mdcy[kc - 1, 0] = 0
        info(5, 'defining', pdgid, 'as stable particle')

    def generate_event(self):
        reject = self.lib.dt_kkinc(*self.dpmevt_tup, kkmat=-1)
        self.lib.dtevno.nevent += 1
        #         print "bimpac", self.lib.dtglcp.bimpac
        return reject


#=========================================================================
# SettDPMJETIII_DisablePythiaTune
#=========================================================================


class SettDPMJETIII_DisablePythiaTune(Settings):
    def __init__(self, lib, args):
        Settings.__init__(self, lib)

    def enable(self):
        self.lib.dt_initjs(0)
        self.lib.dt_initjs(-1)

    def reset(self):
        pass


#=========================================================================
# DpmjetIIIMCRun
#=========================================================================


class DpmjetIIICascadeRun():
    def __init__(self,
                 lib_str,
                 label,
                 decay_mode,
                 n_events,
                 fill_subset=True,
                 p_debug=True,
                 inimass=14):

        from ParticleDataTool import DpmJetParticleTable
        exec "import " + lib_str + " as dpmlib"
        self.lib = dpmlib  # @UndefinedVariable
        self.label = label
        self.nEvents = n_events
        self.spectrum_hists = []

        self.dbg = p_debug
        self.fill_subset = fill_subset
        self.inimass = inimass
        self.set_stable(decay_mode)
        self.ptab = DpmJetParticleTable()
        self.projectiles = [
            'p', 'n', 'K+', 'K-', 'pi+', 'pi-', 'K0L', 'p-bar', 'n-bar',
            'Sigma-', 'Sigma--bar', 'Sigma+', 'Sigma+-bar', 'Xi0', 'Xi0-bar',
            'Xi-', 'Xi--bar', 'Lambda0', 'Lambda0-bar'
        ]
        self.proj_allowed = [
            self.ptab.modname2pdg[p] for p in self.projectiles
        ]
        self.init_generator()

    def get_hadron_air_cs(self, E_lab, projectile_id):
        ntrials = 50000
        if self.dbg:
            print(
                "DpmjetIIICascadeRun::get_hadron_air_cs():" +
                "calculating cross-section calculation for {0} @ {1:3.3g} GeV"
            ).format(projectile_id, E_lab)
        self.lib.dtglgp.jstatb = ntrials
        # Calculate inelastic cross section
        pdg = self.ptab.modname2pdg[projectile_id]
        k = EventKinematics(plab=E_lab, p1pdg=pdg, nuc2_prop=(14, 7))
        self.lib.dt_xsglau(k.A1, k.A2, self.lib.idt_icihad(k.p1pdg), 0, 0,
                           k.ecm, 1, 1, 1)
        self.lib.dtglgp.jstatb = 1000
        print self.lib.dtglxs.xspro[0, 0, 0]
        return self.lib.dtglxs.xspro[0, 0, 0]

    def init_generator(self):
        from random import randint

        # Initialize for maximum energy
        self.evkin = EventKinematics(
            plab=1e11,
            p1pdg=2212,
            nuc2_prop=(self.inimass, int(self.inimass / 2)))
        k = self.evkin
        self.dpmevt_tup = k.A1, k.Z1, k.A2, k.Z2, \
            self.lib.idt_icihad(k.p1pdg), k.elab

        ounit = 6
        try:
            self.lib.dtflka.lout = ounit
            self.lib.dtflka.lpri = 50
            self.lib.pydat1.mstu[10] = ounit
        except AttributeError:
            self.lib.dtiont.lout = ounit
            self.lib.pydat1.mstu[10] = ounit
        self.lib.dt_init(-1, k.elab, *self.dpmevt_tup[:-1], iglau=0)

        # Set seed of random number generator
        rseed = randint(1000000, 10000000)
        sseed = str(rseed)
        n1, n2, n3, n4 = int(sseed[0:2]), int(sseed[2:4]), \
            int(sseed[4:6]), int(sseed[6:8])
        self.lib.dt_rndmst(n1, n2, n3, n4)

        # Lab frame for atmospheric cascade
        self.lib.dtflg1.iframe = 1

    def start(self, projectile, E_lab, sqs, Atarget=0):
        templ = '''
        Model     : {0}
        N_events  : {1}
        Projectile: {2}
        E_lab     : {3:5.3e} GeV
        E_cm      : {3:5.3e} GeV
        Target    : {4}
        '''
        print templ.format(self.label, self.nEvents, projectile, E_lab,
                           Atarget)
        projectile = self.ptab.modname2pdg[projectile]

        if projectile not in self.proj_allowed:
            raise Exception("DpmjetIIICascadeRun(): Projectile " +
                            int(projectile) + " not allowed.")
        if Atarget == 0:
            self.dpmevt_tup = 1, 1, 14, 7, \
                self.lib.idt_icihad(projectile), E_lab
        else:
            Z_target = int(Atarget / 2) if Atarget > 1 else 1
            self.dpmevt_tup = 1, 1, Atarget, Z_target, \
                self.lib.idt_icihad(projectile), E_lab
        hist_d = {}
        for hist in self.spectrum_hists:
            hist_d[hist.particle_id] = hist
        ngenerated = self.nEvents
        for i in xrange(self.nEvents):
            reject = self.lib.dt_kkinc(*self.dpmevt_tup, kkmat=-1)
            self.lib.dtevno.nevent += 1
            if reject:
                ngenerated = ngenerated - 1
                continue
            if not (i % 10000) and i and self.dbg:
                print i, "events generated."
            event = DpmjetIIICascadeEvent(self.lib)

            unique_pids = np.unique(event.p_ids)
            if not self.fill_subset:
                [hist_d[pid].fill_event(event) for pid in unique_pids]
            else:
                for pid in unique_pids:
                    if pid in hist_d.keys():
                        hist_d[pid].fill_event(event)
        # Correct for selective filling of histograms
        for hist in self.spectrum_hists:
            hist.n_events_filled = ngenerated

    def set_stable(self, decay_mode):
        from ParticleDataTool import SibyllParticleTable
        if self.dbg:
            print(self.__class__.__name__ + "::set_stable():" +
                  " Setting standard particles stable.")
        if decay_mode < 0:
            print(self.__class__.__name__ + "::set_stable():" +
                  " use default stable def.")
            return

        # fast-mode particles
        if decay_mode == 0:
            for pdg_id in standard_particles:
                if self.dbg:
                    print 'stable,', pdg_id
                kc = self.lib.pycomp(pdg_id)
                self.lib.pydat3.mdcy[kc - 1, 0] = 0
            return

        # keep muons pions, kaons
        stab = SibyllParticleTable()
        for i in range(4, 5 + 1):
            if self.dbg:
                print 'stable,', stab.modid2pdg[i]
            kc = self.lib.pycomp(stab.modid2pdg[i])
            self.lib.pydat3.mdcy[kc - 1, 0] = 0
        for i in range(7, 18 + 1):
            if self.dbg:
                print 'stable,', stab.modid2pdg[i]
            kc = self.lib.pycomp(stab.modid2pdg[i])
            self.lib.pydat3.mdcy[kc - 1, 0] = 0
        # K0 and K0-bar have to remain unstable to form K0S/L
        # set pi0 unstable
        kc = self.lib.pycomp(111)
        self.lib.pydat3.mdcy[kc - 1, 0] = 1

        if decay_mode <= 1:
            return

        # Decay mode 2 for generation of decay spectra (all conventional with
        # lifetime >= K0S
        if self.dbg:
            print(self.__class__.__name__ + "::set_stable(): Setting "
                  "conventional Sigma-, Xi0," +
                  "Xi- and Lambda0 stable (decay mode).")
        for i in range(36, 39 + 1):
            if self.dbg:
                print 'unstable,', stab.modid2pdg[i]
            kc = self.lib.pycomp(stab.modid2pdg[i])
            self.lib.pydat3.mdcy[kc - 1, 0] = 0

        if decay_mode <= 2:
            return

        # Conventional mesons and baryons
        # keep eta, eta', rho's, omega, phi, K*
        if self.dbg:
            print(self.__class__.__name__ + "::set_stable(): Setting" +
                  " all conventional stable.")
        # pi0
        if self.dbg:
            print 'unstable,', stab.modid2pdg[i]
        kc = self.lib.pycomp(111)
        self.lib.pydat3.mdcy[kc - 1, 0] = 0
        for i in range(23, 33 + 1):
            if self.dbg:
                print 'unstable,', stab.modid2pdg[i]
            kc = self.lib.pycomp(stab.modid2pdg[i])
            self.lib.pydat3.mdcy[kc - 1, 0] = 0

        # keep SIGMA, XI, LAMBDA
        for i in range(34, 49 + 1):
            if self.dbg:
                print 'unstable,', stab.modid2pdg[i]
            kc = self.lib.pycomp(stab.modid2pdg[i])
            self.lib.pydat3.mdcy[kc - 1, 0] = 0

        if decay_mode <= 3:
            return

        if decay_mode <= 4:
            for i in range(59, 99 + 1):
                if i > 60 and i < 71 or i == 82 or \
                        i > 89 and i < 94:
                    continue
                if self.dbg:
                    print 'unstable,', stab.modid2pdg[i]
                kc = self.lib.pycomp(stab.modid2pdg[i])
                self.lib.pydat3.mdcy[kc - 1, 0] = 0


#=========================================================================
# DpmjetIIIMCEvent
#=========================================================================
class DpmjetIIICascadeEvent():
    def __init__(self, lib):

        evt = lib.dtevt1
        npart = evt.nhkk

        sel = np.where(evt.isthkk[:npart] == 1)

        self.p_ids = evt.idhkk[sel]
        self.pz = evt.phkk[2, sel][0]
        self.E = evt.phkk[3, sel][0]
