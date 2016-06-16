remisc
======

Another framework!? What's the point? Aren't there a thousand-and-one web
frameworks out there already? Don't *some* of them already support REST-oriented
operations? (Spoiler: Sort of...) Who cares about scientific computing anyways?

Here's the problem... Who needs a full-up MVC framework if all you're doing is
passing system model data back and forth, or hosting a simulation service in a
cloud environment? You don't. You need something model-centric, which doesn't
assume clients are using a web browser. You need something that's going to
provide the supporting infrastructure, like WSGI mapping and automated operation
& model documentation, with the least possible overhead of work and processing
power. Focus on the unique part of your work--defining operations and the models
they use--and let *remisc* take care of everything else.

Services
--------

A new microservice is defined by subclassing *remisc.service.Service*. Methods
of this class can be decorated by *@remisc.service.isop*. These operations take
two inputs, the urlparse object of the request and a dictionary of any arguments
parsed from the URL's query string segment. They should return a textual
response. A request will be mapped to an operation method by matching the method
name to the top-level directory in the request URL (i.e., if a service is hosted
on http://mysvcs.com/, the request to http://mysvcs.com/test will look for the
method *test* of the host Service-derived class.

The base Service class includes an *app()* method that defines a WSGI-compliant
application interface used to parse request arguments, map them to the
appropriate method, and wrap the response generation process to return content.

Models
------

Frequently, users must provide--or expect to receive--data formatted in
accordance with specific models. Such data exchange formats can be defined by
any class co-located with a Service-derived class, so long as they are
decorated by *@remisc.dxm.isdxm*.

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

This is one of the most powerful behaviors of the *remisc* framework. The *_help*
operation returns documentation of all operations and data exchange models for
the current Service-derived object. Operations are determined by evaluating all
instance methods for the @isdxm decorator. Data exchange models are determined
by evaluating all classes co-located in the same module as the Service-derived
class for the @isdxm decorator. The response maps a JSON object to the
docstrings for each operation and data exchange model, so users can determine
what operations the service provides and how it may utilize them.

Serving
-------

By default, the *remisc* package includs a *server* module that utilizes the
core module *wsgiref*'s *simple_server* model to host a Service. All
Service-derived classes include a WSGI-compliant *app()* method invoked by the
server host process. For production runs, it is strongly advised to invoke that
methods from a production-level WSGI server instead.

Getting Started
---------------

In Action
~~~~~~~~~

When the *remisc.server.main* method is invoked directly, the reference WSGI
server in Python's core module *wsgiref* is used to host an instance of a given
*remisc.service.Service* class. (If no class is provided, the base class is used
instead.) This can be done procedurally::

 >>> from remisc import server
 >>> server.main()
 Serving "remisc.service.Service" with wsgiref.simple_server @ 127.0.0.1:8000

If you use your web browser to load *http://127.0.0.1:8000*, you will see the
default operation implemented by the *remisc.service.Service._root()* method
("Here is the base."). You will also see, in the Python environment where you
launched the server, how that request was mapped to an operation by the WSGI
application interface implemented by *remisc.service.Service.app()*::

 "http://127.0.0.1:8000/" => "_root"
 127.0.0.1 - - [{date} {time}] "GET / HTTP/1.1" 200 {response time}
 "http://127.0.0.1:8000/favicon.ico" => "_null"
 127.0.0.1 - - [{date} {time}] "GET /favicon.ico HTTP/1.1" 200 {response time}

Note that most browsers implicitly request *favicon.ico* with each page request;
this is one useful application of the *_null* method, which is hard-coded to
reply to such requests with an empty response.

You can view the base responses directly by browsing to the following URLs while
your test server is still running. Once you have seen the responses, press
CTRL-C in the Python environment to stop the server.

 - http://127.0.0.1:8000/_root
 - http://127.0.0.1:8000/_null
 - http://127.0.0.1:8000/_help

Your Own Service
~~~~~~~~~~~~~~~~

Subclassing *remisc.service.Service* will let you define your own operations and
override those already implemented. Make sure you decorate each method that
implements an operation with *@remisc.service.isop*. Such methods should take
two arguments: a *urlparse* object capturing the original request, and an args
dictionary constructed from the URL query string. The operation should return
the textual content of the response.

For example, let's implement a simple service *Joker* that implements a *joke*
operation::

 >>> from remisc import service
 >>> class Joker(service.Service):
 >>>     @service.isop
 >>>     def joke(self, urlobj, args):
 >>>         return 'Why did the spam cross the road?\n\nTo evade the dead parrot!'

We can host this service by passing the class to the *remisc.server.main*
function as the *Svc* parameter::

 >>> server.main(Svc=Joker)

Now, try browsing to http://127.0.0.1:8000/joke. For a bonus, note that your new
operation has automatically been added to the response at
http://127.0.0.1:8000/_help!
