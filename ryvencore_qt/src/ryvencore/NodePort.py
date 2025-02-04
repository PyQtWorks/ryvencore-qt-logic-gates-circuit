from .Base import Base

from .RC import PortObjPos, FlowAlg
from .dtypes import DType
from .tools import serialize
from .InfoMsgs import InfoMsgs


class NodePort(Base):
    """The base class for inputs and outputs of nodes with basic functionality."""

    def __init__(self, node, io_pos, type_, label_str):
        Base.__init__(self)

        self.val = None
        self.node = node
        self.io_pos = io_pos
        self.type_ = type_
        self.label_str = label_str
        self.connections = []


    def get_val(self):
        pass

    def connected(self):
        pass

    def disconnected(self):
        pass

    def config_data(self):
        data_dict = {
            'type': self.type_,
            'label': self.label_str
        }

        return data_dict


class NodeInput(NodePort):

    def __init__(self, node, type_, label_str='', add_config=None, dtype: DType = None):
        super().__init__(node, PortObjPos.INPUT, type_, label_str)

        # add_config can be used to store additional config data for enhanced data input ports
        self.add_config = add_config

        # optional dtype
        self.dtype: DType = dtype

    def disconnected(self):
        super().disconnected()
        if self.type_ == 'data' and self.node.flow.alg_mode == FlowAlg.DATA:
            self.node.update(self.node.inputs.index(self))

    def get_val(self):
        InfoMsgs.write('getting value of node input')

        if self.node.flow.alg_mode == FlowAlg.DATA or len(self.connections) == 0:
            return self.val
        else:  # len(self.connections) > 0:
            return self.connections[0].get_val()

    def update(self, data=None):
        """called from another node or from connected()"""
        if self.type_ == 'data':
            self.val = data  # self.get_val()
            InfoMsgs.write('Data in input set to', data)

        self.node.update(inp=self.node.inputs.index(self))

    def config_data(self):
        data = super().config_data()

        if len(self.connections) == 0:
            data['val'] = serialize(self.get_val())

        if self.dtype:
            data['dtype'] = str(self.dtype)
            data['dtype state'] = serialize(self.dtype.get_state())

        return data



class NodeOutput(NodePort):
    def __init__(self, node, type_, label_str=''):
        super().__init__(node, PortObjPos.OUTPUT, type_, label_str)

    def exec(self):
        for c in self.connections:
            c.activate()

    def get_val(self):
        InfoMsgs.write('getting value in node output')

        if self.node.flow.alg_mode == FlowAlg.EXEC:
            self.node.update()
        return self.val

    def set_val(self, val):

        # in case val isn't of complex type
        self.val = val

        if self.node.flow.alg_mode == FlowAlg.DATA:
            for c in self.connections:
                c.activate(data=val)

    def connected(self):
        super().connected()
        if self.type_ == 'data' and self.node.flow.alg_mode == FlowAlg.DATA:
            self.set_val(self.val)  # update output
