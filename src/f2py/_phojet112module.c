/* File: _phojet112module.c
 * This file is auto-generated with f2py (version:1.23.5).
 * f2py is a Fortran to Python Interface Generator (FPIG), Second Edition,
 * written by Pearu Peterson <pearu@cens.ioc.ee>.
 * Generation date: Mon Jan 16 05:27:39 2023
 * Do not edit this file directly unless you know what you are doing!!!
 */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef PY_SSIZE_T_CLEAN
#define PY_SSIZE_T_CLEAN
#endif /* PY_SSIZE_T_CLEAN */

/* Unconditionally included */
#include <Python.h>
#include <numpy/npy_os.h>

/*********************** See f2py2e/cfuncs.py: includes ***********************/
#include "fortranobject.h"
/*need_includes0*/

/**************** See f2py2e/rules.py: mod_rules['modulebody'] ****************/
static PyObject *_phojet112_error;
static PyObject *_phojet112_module;

/*********************** See f2py2e/cfuncs.py: typedefs ***********************/
/*need_typedefs*/

/****************** See f2py2e/cfuncs.py: typedefs_generated ******************/
/*need_typedefs_generated*/

/********************** See f2py2e/cfuncs.py: cppmacros **********************/
#if defined(PREPEND_FORTRAN)
#if defined(NO_APPEND_FORTRAN)
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) _##F
#else
#define F_FUNC(f,F) _##f
#endif
#else
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) _##F##_
#else
#define F_FUNC(f,F) _##f##_
#endif
#endif
#else
#if defined(NO_APPEND_FORTRAN)
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F
#else
#define F_FUNC(f,F) f
#endif
#else
#if defined(UPPERCASE_FORTRAN)
#define F_FUNC(f,F) F##_
#else
#define F_FUNC(f,F) f##_
#endif
#endif
#endif
#if defined(UNDERSCORE_G77)
#define F_FUNC_US(f,F) F_FUNC(f##_,F##_)
#else
#define F_FUNC_US(f,F) F_FUNC(f,F)
#endif


/************************ See f2py2e/cfuncs.py: cfuncs ************************/
/*need_cfuncs*/

/********************* See f2py2e/cfuncs.py: userincludes *********************/
/*need_userincludes*/

/********************* See f2py2e/capi_rules.py: usercode *********************/


/* See f2py2e/rules.py */
/*eof externroutines*/

/******************** See f2py2e/capi_rules.py: usercode1 ********************/


/******************* See f2py2e/cb_rules.py: buildcallback *******************/
/*need_callbacks*/

/*********************** See f2py2e/rules.py: buildapi ***********************/
/*eof body*/

/******************* See f2py2e/f90mod_rules.py: buildhooks *******************/
/*need_f90modhooks*/

/************** See f2py2e/rules.py: module_rules['modulebody'] **************/

/******************* See f2py2e/common_rules.py: buildhooks *******************/

static FortranDataDef f2py_dtflg1_def[] = {
  {"ifrag",1,{{2}},NPY_INT},
  {"iresco",0,{{-1}},NPY_INT},
  {"imshl",0,{{-1}},NPY_INT},
  {"iresrj",0,{{-1}},NPY_INT},
  {"ioulev",1,{{6}},NPY_INT},
  {"lemcck",0,{{-1}},NPY_INT},
  {"lhadro",1,{{10}},NPY_INT},
  {"lseadi",0,{{-1}},NPY_INT},
  {"levapo",0,{{-1}},NPY_INT},
  {"iframe",0,{{-1}},NPY_INT},
  {"itrspt",0,{{-1}},NPY_INT},
  {NULL}
};
static void f2py_setup_dtflg1(char *ifrag,char *iresco,char *imshl,char *iresrj,char *ioulev,char *lemcck,char *lhadro,char *lseadi,char *levapo,char *iframe,char *itrspt) {
  int i_f2py=0;
  f2py_dtflg1_def[i_f2py++].data = ifrag;
  f2py_dtflg1_def[i_f2py++].data = iresco;
  f2py_dtflg1_def[i_f2py++].data = imshl;
  f2py_dtflg1_def[i_f2py++].data = iresrj;
  f2py_dtflg1_def[i_f2py++].data = ioulev;
  f2py_dtflg1_def[i_f2py++].data = lemcck;
  f2py_dtflg1_def[i_f2py++].data = lhadro;
  f2py_dtflg1_def[i_f2py++].data = lseadi;
  f2py_dtflg1_def[i_f2py++].data = levapo;
  f2py_dtflg1_def[i_f2py++].data = iframe;
  f2py_dtflg1_def[i_f2py++].data = itrspt;
}
extern void F_FUNC(f2pyinitdtflg1,F2PYINITDTFLG1)(void(*)(char*,char*,char*,char*,char*,char*,char*,char*,char*,char*,char*));
static void f2py_init_dtflg1(void) {
  F_FUNC(f2pyinitdtflg1,F2PYINITDTFLG1)(f2py_setup_dtflg1);
}

static FortranDataDef f2py_dtcomp_def[] = {
  {"emufra",1,{{20}},NPY_DOUBLE},
  {"iemuma",1,{{20}},NPY_INT},
  {"iemuch",1,{{20}},NPY_INT},
  {"ncompo",0,{{-1}},NPY_INT},
  {"iemul",0,{{-1}},NPY_INT},
  {NULL}
};
static void f2py_setup_dtcomp(char *emufra,char *iemuma,char *iemuch,char *ncompo,char *iemul) {
  int i_f2py=0;
  f2py_dtcomp_def[i_f2py++].data = emufra;
  f2py_dtcomp_def[i_f2py++].data = iemuma;
  f2py_dtcomp_def[i_f2py++].data = iemuch;
  f2py_dtcomp_def[i_f2py++].data = ncompo;
  f2py_dtcomp_def[i_f2py++].data = iemul;
}
extern void F_FUNC(f2pyinitdtcomp,F2PYINITDTCOMP)(void(*)(char*,char*,char*,char*,char*));
static void f2py_init_dtcomp(void) {
  F_FUNC(f2pyinitdtcomp,F2PYINITDTCOMP)(f2py_setup_dtcomp);
}

static FortranDataDef f2py_dtiont_def[] = {
  {"linp",0,{{-1}},NPY_INT},
  {"lout",0,{{-1}},NPY_INT},
  {"ldat",0,{{-1}},NPY_INT},
  {NULL}
};
static void f2py_setup_dtiont(char *linp,char *lout,char *ldat) {
  int i_f2py=0;
  f2py_dtiont_def[i_f2py++].data = linp;
  f2py_dtiont_def[i_f2py++].data = lout;
  f2py_dtiont_def[i_f2py++].data = ldat;
}
extern void F_FUNC(f2pyinitdtiont,F2PYINITDTIONT)(void(*)(char*,char*,char*));
static void f2py_init_dtiont(void) {
  F_FUNC(f2pyinitdtiont,F2PYINITDTIONT)(f2py_setup_dtiont);
}
/*need_commonhooks*/

/**************************** See f2py2e/rules.py ****************************/

static FortranDataDef f2py_routine_defs[] = {
/*eof routine_defs*/
    {NULL}
};

static PyMethodDef f2py_module_methods[] = {

    {NULL,NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_phojet112",
    NULL,
    -1,
    f2py_module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit__phojet112(void) {
    int i;
    PyObject *m,*d, *s, *tmp;
    m = _phojet112_module = PyModule_Create(&moduledef);
    Py_SET_TYPE(&PyFortran_Type, &PyType_Type);
    import_array();
    if (PyErr_Occurred())
        {PyErr_SetString(PyExc_ImportError, "can't initialize module _phojet112 (failed to import numpy)"); return m;}
    d = PyModule_GetDict(m);
    s = PyUnicode_FromString("1.23.5");
    PyDict_SetItemString(d, "__version__", s);
    Py_DECREF(s);
    s = PyUnicode_FromString(
        "This module '_phojet112' is auto-generated with f2py (version:1.23.5).\nFunctions:\n"
"COMMON blocks:\n""  /dtflg1/ ifrag(2),iresco,imshl,iresrj,ioulev(6),lemcck,lhadro(10),lseadi,levapo,iframe,itrspt\n""  /dtcomp/ emufra(20),iemuma(20),iemuch(20),ncompo,iemul\n""  /dtiont/ linp,lout,ldat\n"".");
    PyDict_SetItemString(d, "__doc__", s);
    Py_DECREF(s);
    s = PyUnicode_FromString("1.23.5");
    PyDict_SetItemString(d, "__f2py_numpy_version__", s);
    Py_DECREF(s);
    _phojet112_error = PyErr_NewException ("_phojet112.error", NULL, NULL);
    /*
     * Store the error object inside the dict, so that it could get deallocated.
     * (in practice, this is a module, so it likely will not and cannot.)
     */
    PyDict_SetItemString(d, "__phojet112_error", _phojet112_error);
    Py_DECREF(_phojet112_error);
    for(i=0;f2py_routine_defs[i].name!=NULL;i++) {
        tmp = PyFortranObject_NewAsAttr(&f2py_routine_defs[i]);
        PyDict_SetItemString(d, f2py_routine_defs[i].name, tmp);
        Py_DECREF(tmp);
    }
/*eof initf2pywraphooks*/
/*eof initf90modhooks*/

  tmp = PyFortranObject_New(f2py_dtflg1_def,f2py_init_dtflg1);
  F2PyDict_SetItemString(d, "dtflg1", tmp);
  Py_DECREF(tmp);
  tmp = PyFortranObject_New(f2py_dtcomp_def,f2py_init_dtcomp);
  F2PyDict_SetItemString(d, "dtcomp", tmp);
  Py_DECREF(tmp);
  tmp = PyFortranObject_New(f2py_dtiont_def,f2py_init_dtiont);
  F2PyDict_SetItemString(d, "dtiont", tmp);
  Py_DECREF(tmp);/*eof initcommonhooks*/


#ifdef F2PY_REPORT_ATEXIT
    if (! PyErr_Occurred())
        on_exit(f2py_report_on_exit,(void*)"_phojet112");
#endif
    return m;
}
#ifdef __cplusplus
}
#endif
