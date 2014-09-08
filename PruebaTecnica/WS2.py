from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array

class HelloWorldService(SimpleWSGISoapApp):
    @soapmethod(String,Integer,_returns=Array(String))
    def say_hello(self,name,times):
        results = []
        for i in range(0,times):
            results.append('Hello, %s'%name)
        return results

if __name__=='__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 7789, HelloWorldService())
    server.serve_forever()