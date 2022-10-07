"""This module initializes lists of namedtuple that link the definitions
of models and their various versions to the existing wrapper classes.
"""

from collections import namedtuple
from impy.models import (
    sibyll,
    dpmjetIII,
    epos,
    phojet,
    urqmd,
    pythia6,
    pythia8,
    qgsjet,
    sophia,
)

# Objects of this type contain all default initialization directions
# for each interaction model and create dictionaries that link the
# these settings to either the 'tag' or the 'crmc_id'
InteractionModelDef = namedtuple(
    "InteractionModelDef",
    [
        "tag",
        "name",
        "version",
        "crmc_id",
        "library_name",
        "RunClass",
        "EventClass",
        "output_frame",
    ],
)

# The list of available interaction models. Extend with new models or
# versions when available
interaction_model_nt_init = [
    [
        "SIBYLL23D",
        "SIBYLL",
        "2.3d",
        -1,
        "_sib23d",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    # This was the default version that was firstly circulated in CORSIKA
    [
        "SIBYLL23C",
        "SIBYLL",
        "2.3c",
        -1,
        "_sib23c01",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    # The c03 version was also in CORSIKA until 2020
    [
        "SIBYLL23C03",
        "SIBYLL",
        "2.3c03",
        -1,
        "_sib23c03",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    # The latest patch c04 was renamed to d, to generate less confusion
    [
        "SIBYLL23C04",
        "SIBYLL",
        "2.3d",
        -1,
        "_sib23d",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    # The other versions are development versions and won't be distributed with impy
    # (maybe)
    [
        "SIBYLL23C00",
        "SIBYLL",
        "2.3c00",
        -1,
        "_sib23c00",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    [
        "SIBYLL23C01",
        "SIBYLL",
        "2.3c01",
        -1,
        "_sib23c01",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    [
        "SIBYLL23C02",
        "SIBYLL",
        "2.3c02",
        -1,
        "_sib23c02",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    [
        "SIBYLL23",
        "SIBYLL",
        "2.3",
        -1,
        "_sib23",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    [
        "SIBYLL21",
        "SIBYLL",
        "2.1",
        -1,
        "_sib21",
        sibyll.SIBYLLRun,
        sibyll.SibyllEvent,
        "center-of-mass",
    ],
    [
        "DPMJETIII191",
        "DPMJET-III",
        "19.1",
        -1,
        "_dpmjetIII191",
        dpmjetIII.DpmjetIIIRun,
        dpmjetIII.DpmjetIIIEvent,
        "center-of-mass",
    ],
    [
        "DPMJETIII193",
        "DPMJET-III",
        "19.3",
        -1,
        "_dpmjetIII193",
        dpmjetIII.DpmjetIIIRun,
        dpmjetIII.DpmjetIIIEvent,
        "center-of-mass",
    ],
    [
        "DEV_DPMJETIII193",
        "DEV_DPMJET-III",
        "19.3",
        -1,
        "_dev_dpmjetIII193",
        dpmjetIII.DpmjetIIIRun,
        dpmjetIII.DpmjetIIIEvent,
        "center-of-mass",
    ],
    [
        "DPMJETIII306",
        "DPMJET-III",
        "3.0-6",
        -1,
        "_dpmjet306",
        dpmjetIII.DpmjetIIIRun,
        dpmjetIII.DpmjetIIIEvent,
        "center-of-mass",
    ],
    [
        "EPOSLHC",
        "EPOS",
        "LHC",
        -1,
        "_eposlhc",
        epos.EPOSRun,
        epos.EPOSEvent,
        "center-of-mass",
    ],
    [
        "PHOJET112",
        "PHOJET",
        "1.12-35",
        -1,
        "_phojet112",
        phojet.PHOJETRun,
        phojet.PhojetEvent,
        "center-of-mass",
    ],
    [
        "PHOJET191",
        "PHOJET",
        "19.1",
        -1,
        "_phojet191",
        phojet.PHOJETRun,
        phojet.PhojetEvent,
        "center-of-mass",
    ],
    [
        "PHOJET193",
        "PHOJET",
        "19.3",
        -1,
        "_phojet193",
        phojet.PHOJETRun,
        phojet.PhojetEvent,
        "center-of-mass",
    ],
    [
        "URQMD34",
        "UrQMD",
        "3.4",
        -1,
        "_urqmd34",
        urqmd.UrQMDRun,
        urqmd.UrQMDEvent,
        "center-of-mass",
    ],
    [
        "PYTHIA6",
        "Pythia",
        "6.428",
        -1,
        "_pythia6",
        pythia6.PYTHIA6Run,
        pythia6.PYTHIA6Event,
        "center-of-mass",
    ],
    [
        "PYTHIA8",
        "Pythia",
        "8.240",
        -1,
        "_pythia8",
        pythia8.PYTHIA8Run,
        pythia8.PYTHIA8Event,
        "center-of-mass",
    ],
    [
        "QGSJET01D",
        "QGSJet",
        "01c",
        -1,
        "_qgs01",
        qgsjet.QGSJet01Run,
        qgsjet.QGSJETEvent,
        "laboratory",
    ],
    [
        "QGSJETII03",
        "QGSJet",
        "II-03",
        -1,
        "_qgsII03",
        qgsjet.QGSJetIIRun,
        qgsjet.QGSJETEvent,
        "laboratory",
    ],
    [
        "QGSJETII04",
        "QGSJet",
        "II-04",
        -1,
        "_qgsII04",
        qgsjet.QGSJetIIRun,
        qgsjet.QGSJETEvent,
        "laboratory",
    ],
    [
        "SOPHIA20",
        "SOPHIA",
        "2.0",
        -1,
        "_sophia",
        sophia.SophiaRun,
        sophia.SophiaEvent,
        "laboratory",
    ],
]

# Different kinds of lookup-maps/dictionaries to refer to models by name
# or ID
interaction_model_by_tag = {}
interaction_model_by_crmc_id = {}

for arg_tup in interaction_model_nt_init:
    nt = InteractionModelDef(*arg_tup)
    interaction_model_by_tag[nt.tag] = nt
    interaction_model_by_crmc_id[nt.crmc_id] = nt


def make_generator_instance(int_model_def):
    """Returns instance of a <Model>Run."""
    return int_model_def.RunClass(int_model_def)
