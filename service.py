"""Defines an abstracted service model for interfacing to a WSGI request with
   specific operations and meta-operations.
"""

import importlib
import json
import urlparse
from src.dxm import Empty

def isop(func):
    """Defines the @isop decorator used to indicate specific methods of a
       Service-derived class are meant to provide REST-ful operations. Such
       methods take two arguments, the urlparse object for the request and a
       dictionary of query string arguments.
    """
    func.isop = True
    return func

class Service(object):
    """The base class for src-compliant microservice objects. Such objects
       define operations as methods using the @isop decorator. Data exchange
       models supporting such operations should be co-defined (or at least
       included) in the module where the Service-derived class is defined, and
       marked with the @isdxm decorator. The top-level folder is used to route
       the operation; when one is not provided, _root is invoked instead.
    """

    def __init__(self):
        pass
        
    def getAllOps(self):
        """Returns the names of all operations provided by this instance of the
           Service class, as determined by the @isop decorator (which adds the
           isop method attribute).
        """
        opNames = []
        for attrName in dir(self):
            attr = getattr(self, attrName)
            if hasattr(attr, 'isop'):
                opNames.append(attrName)
        return opNames
        
    def getAllDxms(self):
        """Returns all data exchange model (DXM) classes defined in conjunction
           with this service object by iterating over the contents of the module
           where this class is defined and returning the names of those classes
           that have the 'isdxm' attribute (assigned by the @isdxm decorator).
        """
        dxms = []
        cls = self.__class__
        mod = importlib.import_module(cls.__module__)
        clsType = type(cls)
        for symName in dir(mod):
            sym = getattr(mod, symName)
            if hasattr(sym, 'isdxm') and type(sym) is clsType:
                dxms.append(sym)
        return dxms
        
    @isop
    def _null(self, url, args):
        """The default service response/operation--returns an empty string.
        """
        return ''
        
    @isop
    def _root(self, url, args):
        """Defines the root-level operation, where no arguments have been
           provided.
        """
        return 'Here is the base.'

    @isop
    def _help(self, url, args):
        """Returns documentation of this service's operations and related data
           exchange models (DXMs). Service operations are marked by the isop
           function attribute (as added by the @isop decorator), while data
           exchange models are marked by the isdxm class attribute (as added by
           the @isdxm decorator). Operations are methods of the Service-derived
           object, whereas DXMs are classes defined within the same module.
        """
        opNames = self.getAllOps()
        dxms = self.getAllDxms()
        help = {'operations':{}, 'models': {}}
        for opn in opNames:
            op = getattr(self, opn)
            help['operations'][opn] = op.__doc__
        for dxm in dxms:
            help['models'][dxm.__name__] = dxm.__doc__
        txt = json.dumps(help)
        return json.dumps(help, sort_keys=True, indent=4, separators=(',',': '))
        
    def app(self, env, res):
        """Feed env parameters into urlparse object and query dictionary to 1)
           determine the appropriate operation to which those arguments will be
           forwarded, and 2) invoke that operation to construct a response.
        """
        url = env['wsgi.url_scheme'] + '://' + env['HTTP_HOST'] + env['PATH_INFO']
        args = {}
        if len(env['QUERY_STRING']) > 0:
            url += '?' + env['QUERY_STRING']
            args = urlparse.parse_qs(env['QUERY_STRING'])
        o = urlparse.urlparse(url)
        paths = o.path.split('/')
        if len(''.join(paths)) > 1 and len(paths) > 1:
            op = paths[1].lower()
        else:
            op = '_root'
        if op == 'favicon.ico':
            op = '_null'
        m = getattr(self, op)
        if not hasattr(m, 'isop'):
            op = '_null'
            m = getattr(self, op)
        print('"%s" => "%s"' % (url, op))
        try:
            rsp = [m(o, args)]
            res('200 OK', [('Content-Type', 'text/plain')])
        except:
            txt = '500 Internal Server Error'
            rsp = [txt]
            res(txt, [('Content-Type', 'text/plain')])
        return rsp
