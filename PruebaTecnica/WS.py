import soaplib
import soaplib.core
import EncenderDispositivo
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.service import soap

class wsPlacaControladora(DefinitionBase):
    @soap(_returns=None)
    def encenderVentilador(self):
        print('prueba ws')
        rele= EncenderDispositivo.instanciarIK(134980)
        rele.waitForAttach(10000)
        EncenderDispositivo.encenderVentilador(rele)
        rele.closePhidget()
        
    @soap(_returns=None)
    def apagarVentilador(self):
        print('prueba ws')
        rele= EncenderDispositivo.instanciarIK(134980)
        rele.waitForAttach(10000)
        EncenderDispositivo.apagarVentilador(rele)
        rele.closePhidget()
   
if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([wsPlacaControladora], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server('192.168.0.102', 7789, wsgi_application)
        server.serve_forever()
    except ImportError:
        print ("Error: example server code requires Python >= 2.5")