#!/usr/bin/env python
# -*- coding: utf-8 -*-


def source_file(name=None):
    """
    ;+ Returns the source file of the routine `name`
    ;+ If name is not given then it returns the source file of caller routine
    """
    if name is None:
        s = scope_traceback(/structure)
        nlevels = n_elements(s)
        sfile = s[nlevels-2].filename
        return file_expand_path(sfile)
    else:
        help,/source_files,output=csf  # all compiled source files
        nc = n_elements(csf)
        for i=2,nc-1:
            has_name = stregex(csf[i],name,/fold_case) ne -1
            if has_name:
                sfile = stregex(csf[i],"(/[^/ ]*)+/?$",/extract,/fold_case)
                return file_expand_path(sfile)

    return ''
