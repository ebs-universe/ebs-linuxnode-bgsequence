

from twisted.internet import reactor
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gui.kivy.mediaplayer.mixin import MediaPlayerGuiMixin
from ebs.linuxnode.bgsequence.mixin import BackgroundSequenceMixin
from kivy_garden.ebs.clocks.digital import SimpleDigitalClock
from ebs.linuxnode.core.background import BackgroundSpec

try:
    from ebs.linuxnode.gui.kivy.mediaplayer.omxplayer import OMXPlayerGuiMixin
    BaseNode = OMXPlayerGuiMixin
except ImportError:
    BaseNode = MediaPlayerGuiMixin


class ExampleNode(BackgroundSequenceMixin, BaseNode, BaseIoTNodeGui):
    def _set_bg_sequence(self, targets):
        self.bg_sequence = targets

    @property
    def clock(self):
        return SimpleDigitalClock()

    def _background_series_example(self):
        bgseries = [
            BackgroundSpec('1.0:0.5:0.5:1.0', duration=10),
            BackgroundSpec('image.jpg', duration=10),
            'video.mp4',
            BackgroundSpec('structured:clock', duration=10),
            'pdf.pdf',
            BackgroundSpec(None, duration=10),
        ]
        reactor.callLater(5, self._set_bg_sequence, bgseries)

    def start(self):
        super(ExampleNode, self).start()
        self._background_series_example()
