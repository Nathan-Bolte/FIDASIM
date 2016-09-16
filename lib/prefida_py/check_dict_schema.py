#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prefida_py import info
from prefida_py import error


def check_dict_schema(schema, s, err_status, desc=None):
    """
    #check_struct_schema
     Check structure `s` is formatted according to `schema`
    ***
    ##Input Arguments
         **schema**: structure schema

         **s**: structure to check

    ##Output Arguments
         **err**: error code

    ##Keyword Arguments
         **desc**: description of structure `s`

    ##Example usage
    ```idl
    IDL> s = {a:0, b:[1.d0,2.d0], c:"example"}
    IDL> schema = {a:{dims:0,type:"INT"}, b:{dims:[2],type:"DOUBLE"}, c:{dims:0,type:"STRING"}  }

    IDL> check_struct_schema, schema, s, err, desc="Example structure"
    IDL> print, err
        0
    ```
    """
    if desc is None:
        desc = 'dict'

    err_status = 0
    schema_keys = schema.keys()
    skeys = s.keys()

    for i in range(len(skeys)):
        w = (skeys[i] == schema_keys)
        nw = len(schema_keys[w])
        if (nw == 0):
            info('Extra variable "'+skeys[i]+'" found in '+desc)

    for i in range(len(schema_keys)):
        w = (schema_keys[i] == skeys)
        nw = len(schema_keys[w])
        if nw == 0:
            error('"'+schema_keys[i]+'" is missing from the '+desc
            err_status = 1
         else
            ;; Check dimensions
            ww = where((size(s.(w),/dim) eq schema.(i).dims) ne 1,nww)
            if nww ne 0:
                error,'"'+schema_keys[i]+'" has the wrong dimensions. Expected ('+ $
                      strjoin(strcompress(string(schema.(i).dims),/remove_all),',')+')'
                print,'size('+schema_keys[i]+') = ',size(s.(w),/dim)
                err_status = 1

            ;; Check type
            tname = size(s.(w),/tname)
            if tname ne schema.(i).type:
                error,'"'+schema_keys[i]+'" has the wrong type. Expected '+schema.(i).type
                print,'type('+schema_keys[i]+') = '+tname
                err_status = 1

            ;; Check for NaNs or Inf
            if tname ne 'STRING' and tname ne 'STRUCT'
                ww = where(finite(s.(w)) == 0,nww)
             else nww = 0
            if nww ne 0:
                error,'NaN or Infinity detected in "'+schema_keys[i]+'"'
                err_status = 1




