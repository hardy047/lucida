from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import mplayer_handler as m_handler
from lucidaservice import lucida_service


if __name__ == '__main__':
    handler = m_handler.MplayerHandler()
    processor = lucida_service.Processor(handler)
    transport = TSocket.TServerSocket(port=8088)
    tfactory = TTransport.TFramedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()
