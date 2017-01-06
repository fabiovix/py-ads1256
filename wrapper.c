#include <Python.h>
#include "wrapper.h"

/* Docstrings */
static char module_docstring[] =
    "Esta biblioteca é um wrapper ";
static char oi_docstring[] =
    "imprime oi";

/* Available functions */
static PyObject *ads_leia_canais(PyObject *self, PyObject *args);

/* Module specification */
static PyMethodDef module_methods[] = {
 //   {"chi2", chi2_chi2, METH_VARARGS, chi2_docstring},
    {"leia_canais", ads_leia_canais, METH_VARARGS, oi_docstring},
    {NULL, NULL, 0, NULL}
};

/* Initialize the module */
PyMODINIT_FUNC initads1256(void)
{
    PyObject *m = Py_InitModule3("ads1256", module_methods, module_docstring);
    if (m == NULL)
        return;

}

static PyObject *ads_leia_canais(PyObject *self, PyObject *args)
{

    char * ganho, *sps;
    PyObject *yerr_obj;
    double v[8];
                                         

 /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "ss", &ganho, &sps,&yerr_obj))
        return NULL;

    /* execute the code */ 
    lerCanais(4,"0",ganho,sps,v);

    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("[d,d,d,d, d,d,d,d]",
	 v[0],
	 v[1],
	 v[2],
	 v[3],
	 v[4],
	 v[5],
	 v[6],
	 v[7]
     );
    return ret;
}
