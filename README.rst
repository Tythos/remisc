src
===

Scientific REST-ful Computation tools for rapid microservice development and
deployment. Users define a class derived from src.service.Service, for which
microservice operations are defined by methods decorated by *@src.service.isop*.
Operations utilize user-defined models for data exchange, supported by I/O
parsing behaviors defined in the src.dxm module.

Services
--------

A new microservice is defined by subclassing *src.service.Service*. Methods of
this class can be decorated by *@src.service.isop*. These operations take two
inputs, the urlparse object of the request and a dictionary of any arguments
parsed from the URL's query string segment. They should return a textual
response. A request will be mapped to an operation method by matching the method
name to the top-level directory in the request URL (i.e., if a service is hosted
on http://mysvcs.com/, the request to http://mysvcs.com/test will look for the
method 'test' of the hosting Service-derived class.

The base Service class includes an *app()* method that defines a WSGI-compliant
application interface used to parse request arguments, map them to the
appropriate method, and wrap the response generation process to return content.

Models
------

Frequently, users must provide--or expect to receive--data formatted in
accordance with specific models. Such data exchange formats can be defined by
any class co-located with a Service-derived class, so long as they are
decorated by *@src.dxm.isdxm*.

Operations
----------

Several default operations are built into the base Service class:

_root
~~~~~

Any request without a top-level directory name will be routed to the *_root*
method. As with any other method, this operation can be overridden by the user.

_null
~~~~~

This built-in operation returns an empty response. This is one way to hide error
handling--if you're really into that sort of thing.

_help
~~~~~

This is one of the most powerful behaviors of the *src* framework. The *_help*
operation returns documentation of all operations and data exchange models for
the current Service-derived object. Operations are determined by evaluating all
instance methods for the @isdxm decorator. Data exchange models are determined
by evaluating all classes co-located in the same module as the Service-derived
class for the @isdxm decorator. The response maps a JSON object to the
docstrings for each operation and data exchange model, so users can determine
what operations the service provides and how it may utilize them.

Serving
-------

By default, the *src* package includs a *server* module that utilizes the
core module *wsgiref*'s *simple_server* model to host a Service. All
Service-derived classes include a WSGI-compliant *app()* method invoked by the
server host process. For production runs, it is strongly advised to invoke that
methods from a production-level WSGI server instead.
