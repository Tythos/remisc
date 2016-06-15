"""Provides the WSGI application entry point for ReMiSC microservices. This means
   serving the WSGI-compliant app() method of a Service-derived object
   instantiation using the built-in WSGI reference server. Command-line
   arguments take a fully-qualified package/module/class name string to the
   Service-derived class whose instantiation will be used to provide app(). When
   invoked from the command line without an argument, this defaults to the base
   Service class.
"""

import importlib
import sys
from remisc import service
from wsgiref import simple_server

def main(ip='127.0.0.1', port=8000, Svc=service.Service):
    """Instantiates an object of the Service-derived class whose app() method
       will be used to generate responses. This instance is then bound to a
       reference WSGI server. The server is started on the given IP and port
       (defaulting to 127.0.0.1:8000), and the default Service class is the base
       remisc.service.Service class itself.
    """
    svc = Svc()
    httpd = simple_server.make_server(ip, port, svc.app)
    fqn = Svc.__module__ + '.' + Svc.__name__
    print('Serving "%s" with wsgiref.simple_server @ %s:%u' % (fqn, ip, port))
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fqmn = sys.argv[1].split('.')
        m = importlib.import_module('.'.join(fqmn[:-1]))
        main(Svc=getattr(m, fqmn[-1]))
    else:
        main()
