"""Defines common format for Data eXchange Models over scientific RESTful
   computation services. Any class can be a DXM, so long as it is marked with
   the @isdxm decorator. DXMs will be supported by JSON-object conversions
   defined within this module to facilitate request parsing and response
   construction, and are publicly documented by the class docstring.
"""

def isdxm(cls):
    cls.isdxm = True
    return cls

@isdxm
class Empty(object):
    pass
