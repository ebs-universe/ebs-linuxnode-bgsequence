

from twisted.internet import reactor
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gui.kivy.mediaplayer.mixin import MediaPlayerGuiMixin
from ebs.linuxnode.bgsequence.mixin import EffectiveBackgroundMixin
from kivy_garden.ebs.clocks.digital import SimpleDigitalClock
from ebs.linuxnode.core.background import BackgroundSpec

try:
    from ebs.linuxnode.gui.kivy.mediaplayer.omxplayer import OMXPlayerGuiMixin
    BaseNode = OMXPlayerGuiMixin
except ImportError:
    BaseNode = MediaPlayerGuiMixin


class ExampleNode(EffectiveBackgroundMixin, BaseNode, BaseIoTNodeGui):
    def _set_bg_sequence(self, targets):
        self.bg_sequence = targets

    @property
    def clock(self):
        return SimpleDigitalClock()

    _bgseries = [
        BackgroundSpec('1.0:0.5:0.5:1.0', duration=10),
        BackgroundSpec('image.jpg', duration=10),
        'video.mp4',
        'pdf.pdf',
        BackgroundSpec('structured:clock', duration=10),
        BackgroundSpec(None, duration=10),
    ]

    _bgseries_2 = [
        BackgroundSpec('1.0:0.5:0.5:1.0', duration=10),
        'video.mp4',
        BackgroundSpec('structured:clock', duration=10),
        BackgroundSpec(None, duration=10),
    ]

    def _background_sequence_example(self):
        reactor.callLater(5, self._set_bg_sequence, self._bgseries)

    def _background_sequence_set_example(self):
        reactor.callLater(5, self.background_sequence_set, self._bgseries)
        reactor.callLater(42, self.background_sequence_set, self._bgseries_2)

    def start(self):
        super(ExampleNode, self).start()
        self._background_sequence_set_example()
