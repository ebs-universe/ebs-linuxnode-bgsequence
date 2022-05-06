

import faulthandler

from ebs.linuxnode.gui.kivy.utils.launcher import prepare_config
from ebs.linuxnode.gui.kivy.utils.launcher import prepare_environment
from ebs.linuxnode.gui.kivy.utils.launcher import prepare_kivy


def run_node():
    nodeconfig = prepare_config('iotnode-bgsequence-example')

    prepare_environment(nodeconfig)
    prepare_kivy(nodeconfig)

    from ebs.linuxnode.core import config
    config.current_config = nodeconfig

    from app import ExampleApplication

    print("Creating Application : {}".format(ExampleApplication))
    app = ExampleApplication(config=nodeconfig)
    app.run()


if __name__ == '__main__':
    print("Starting faulthandler")
    faulthandler.enable()
    run_node()
