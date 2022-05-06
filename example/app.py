

from ebs.linuxnode.gui.kivy.utils.application import BaseIOTNodeApplication
from node import ExampleNode


class ExampleApplication(BaseIOTNodeApplication):
    _node_class = ExampleNode
