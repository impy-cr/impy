/* File: _phojet191module.c
 * This file is auto-generated with f2py (version:1.23.5).
 * f2py is a Fortran to Python Interface Generator (FPIG), Second Edition,
 * written by Pearu Peterson <pearu@cens.ioc.ee>.
 * Generation date: Mon Jan 16 05:28:01 2023
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
static PyObject *_phojet191_error;
static PyObject *_phojet191_module;

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

static FortranDataDef f2py_hnreac_def[] = {
  {"umo",1,{{296}},NPY_DOUBLE},
  {"plabf",1,{{296}},NPY_DOUBLE},
  {"siin",1,{{296}},NPY_DOUBLE},
  {"wk",1,{{5184}},NPY_DOUBLE},
  {"nrk",2,{{2,268}},NPY_INT},
  {"nure",2,{{30,2}},NPY_INT},
  {NULL}
};
static void f2py_setup_hnreac(char *umo,char *plabf,char *siin,char *wk,char *nrk,char *nure) {
  int i_f2py=0;
  f2py_hnreac_def[i_f2py++].data = umo;
  f2py_hnreac_def[i_f2py++].data = plabf;
  f2py_hnreac_def[i_f2py++].data = siin;
  f2py_hnreac_def[i_f2py++].data = wk;
  f2py_hnreac_def[i_f2py++].data = nrk;
  f2py_hnreac_def[i_f2py++].data = nure;
}
extern void F_FUNC(f2pyinithnreac,F2PYINITHNREAC)(void(*)(char*,char*,char*,char*,char*,char*));
static void f2py_init_hnreac(void) {
  F_FUNC(f2pyinithnreac,F2PYINITHNREAC)(f2py_setup_hnreac);
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
    "_phojet191",
    NULL,
    -1,
    f2py_module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit__phojet191(void) {
    int i;
    PyObject *m,*d, *s, *tmp;
    m = _phojet191_module = PyModule_Create(&moduledef);
    Py_SET_TYPE(&PyFortran_Type, &PyType_Type);
    import_array();
    if (PyErr_Occurred())
        {PyErr_SetString(PyExc_ImportError, "can't initialize module _phojet191 (failed to import numpy)"); return m;}
    d = PyModule_GetDict(m);
    s = PyUnicode_FromString("1.23.5");
    PyDict_SetItemString(d, "__version__", s);
    Py_DECREF(s);
    s = PyUnicode_FromString(
        "This module '_phojet191' is auto-generated with f2py (version:1.23.5).\nFunctions:\n"
"COMMON blocks:\n""  /hnreac/ umo(296),plabf(296),siin(296),wk(5184),nrk(2,268),nure(30,2)\n"".");
    PyDict_SetItemString(d, "__doc__", s);
    Py_DECREF(s);
    s = PyUnicode_FromString("1.23.5");
    PyDict_SetItemString(d, "__f2py_numpy_version__", s);
    Py_DECREF(s);
    _phojet191_error = PyErr_NewException ("_phojet191.error", NULL, NULL);
    /*
     * Store the error object inside the dict, so that it could get deallocated.
     * (in practice, this is a module, so it likely will not and cannot.)
     */
    PyDict_SetItemString(d, "__phojet191_error", _phojet191_error);
    Py_DECREF(_phojet191_error);
    for(i=0;f2py_routine_defs[i].name!=NULL;i++) {
        tmp = PyFortranObject_NewAsAttr(&f2py_routine_defs[i]);
        PyDict_SetItemString(d, f2py_routine_defs[i].name, tmp);
        Py_DECREF(tmp);
    }
/*eof initf2pywraphooks*/
/*eof initf90modhooks*/

  tmp = PyFortranObject_New(f2py_hnreac_def,f2py_init_hnreac);
  F2PyDict_SetItemString(d, "hnreac", tmp);
  Py_DECREF(tmp);/*eof initcommonhooks*/


#ifdef F2PY_REPORT_ATEXIT
    if (! PyErr_Occurred())
        on_exit(f2py_report_on_exit,(void*)"_phojet191");
#endif
    return m;
}
#ifdef __cplusplus
}
#endif
