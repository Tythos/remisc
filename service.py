"""Defines an abstracted service model for interfacing to a WSGI request with
   specific operations and meta-operations.
"""

import urlparse
import types
import functools

class IsOp(object):
    """Defines the IsOp decorator, which can modify function in several use
       cases. Note that, in all use cases, the function's docstring and an
       'isop' flag (with a value of True) are appended to the function.
        * When assigned without arguments, adds a default 'path' property to the
          function based on the function name (preceeded by a file seperator).
          In documentation, we refer to this as attributal decoration.
        * When assigned with a single string argument, appends the given path to
          the function. In documentation, we will refer to this as invocational
          decoration.
    """
    
    def __init__(self, *args):
        """Invoked at module evaluation time, when the class methods are parsed
           (regardless of attributal or invocational decoration). Attributal
           decoration will pass the function; invocational decoration will pass
           the decorator argument.
        """
        self.func = None
        self.path = None
        self.help = None
        if len(args) == 1 and type(args[0]) is types.FunctionType:
            self.func = args[0]
            self.path = '/' + self.func.__name__
            self.help = self.func.__doc__
        elif len(args) == 1 and type(args[0]) in [type(''),type(u'')]:
            self.path = args[0]
        else:
            raise Exception('Invalid decorator construction')
            
    def __call__(self, *args, **kwargs):
        """For attributal decoration, called when the method is invoked with the
           given arguments as attached to the object instance by __get__. For
           invocational decoration, this is invoked at module evaluation time
           with the function as an argument and should return a decorator.
        """
        if self.func is not None:
            return self.func(*args, **kwargs)
        elif self.path is not None:
            io = IsOp(args[0])
            io.path = self.path
            return io
        else:
            raise Exception('Invalid decorator invocation')
            
    def __get__(self, *args):
        """Invoked when the method is fetched from an instance or class. In
           either case, args[1] will be the class object. When method is fetched
           from an instance, the instance will be the first argument.
        """
        func = functools.partial(self.__call__, args[0])
        func.isop = True
        func.path = self.path
        func.help = self.help
        return func

class Service(object):
    """The base class for ReMiSC-compliant microservice objects. Such objects
       define operations as methods using the @isop decorator. Data exchange
       models supporting such operations should be co-defined (or at least
       included) in the module where the Service-derived class is defined, and
       marked with the @isdxm decorator. The top-level folder is used to route
       the operation; when one is not provided, _root is invoked instead.
    """

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
        
    @IsOp
    def _null(self, **kwargs):
        """The default service response/operation--returns an empty string.
        """
        return ''
        
    @IsOp('/')
    def _root(self, **kwargs):
        """Defines the root-level operation, where no arguments have been
           provided.
        """
        return 'Here is the base.'

    def application(self, environ, start_response):
        """Feed environ parameters into urlparse object and query dictionary to
           1) determine the appropriate operation to which those arguments will
           be forwarded, and 2) invoke that operation to construct a response.
        """
        fullUrl = environ['wsgi.url_scheme'] + '://' + environ['HTTP_HOST'] + environ['PATH_INFO'] + '?' + environ['QUERY_STRING']
        pr = urlparse.urlparse(fullUrl)
        args = urlparse.parse_qs(pr.query)
        allOps = self.getAllOps()
        allPaths = [getattr(self,op).path for op in allOps]
        if pr.path not in allPaths:
            print('"%s" => 404' % pr.path)
            response = '404 Not Found'
            start_response(response, [('Content-Type', 'text/plain')])
        else:
            ndx = allPaths.index(pr.path)
            method = getattr(self, allOps[ndx])
            print('"%s" => "%s"' % (pr.path, allOps[ndx]))
            if environ['REQUEST_METHOD'] == 'GET':
                try:
                    response = method(**args)
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                except Exception as e:
                    response = '500 Internal Server Error'
                    start_response(response, [('Content-Type', 'text/plain')])
                    response += '\n' + e.message
            elif environ['REQUEST_METHOD'] == 'OPTIONS':
                response = re.sub('\s+', ' ', method.help).strip()
                start_response('200 OK', [('Content-Type', 'text/plain')])
            else:
                response = '405 Method Not Allowed'
                start_response(response, [('Content-Type', 'text/plain')])
        return [response]
