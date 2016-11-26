from lucidaservice import lucida_service as lservice
import command_processor as c_processor


class MplayerHandler(lservice.Iface):

    def __init__(self):
        self.processor = c_processor.ComamndProcessor()

    def infer(self, LUCID, query):
        data = query.content[0].data[0]
        print "data received:" + data
        return self.processor.process(data)

    def learn(self, LUCID, knowledge):
        pass

    def create(self, LUCID, spec):
        pass
