

from itertools import cycle

from ebs.linuxnode.core.background import BackgroundCoreMixin
from ebs.linuxnode.core.background import BackgroundSpec

from .persistence import BackgroundSequencePersistenceManager


class BackgroundSequenceMixin(BackgroundCoreMixin):
    def __init__(self, *args, **kwargs):
        super(BackgroundSequenceMixin, self).__init__(*args, **kwargs)
        self._bg_sequence = cycle([])
        self._bg_sequence_persistence = BackgroundSequencePersistenceManager(self)
        self._bg_sequence_active = False

    @property
    def bg_sequence(self):
        return self._bg_sequence

    @bg_sequence.setter
    def bg_sequence(self, value):
        self._bg_sequence = cycle(value)
        if not self._bg_sequence_active:
            self.bg_step()
        else:
            ntargets = []
            for item in value:
                if isinstance(item, BackgroundSpec):
                    ntargets.append(item.target)
                else:
                    ntargets.append(item)
            if self._bg_current in ntargets:
                curr = None
                while curr != self._bg_current:
                    curr = next(self._bg_sequence)
                    if isinstance(curr, BackgroundSpec):
                        curr = curr.target

    def bg_step(self, *_):
        target = next(self.bg_sequence)
        bgcolor, callback, duration = None, None, None
        if isinstance(target, BackgroundSpec):
            target, bgcolor, callback, duration = target

        if callback:
            self.log.warn("BG Sequence received an item with a callback. "
                          "This is not supported and is ignored. {}".format(target))

        callback = self.bg_step
        spec = BackgroundSpec(target, bgcolor, callback, duration)
        self.log.debug("BG Sequence Step : {}".format(spec))
        self._bg_sequence_active = True
        self.bg = spec

    def background_sequence_set(self, targets):
        if not targets:
            targets = []

        _targets = []
        for target in targets:
            if not isinstance(target, BackgroundSpec):
                target = BackgroundSpec(target=target)
            provider = self._get_provider(target.target)
            if not provider:
                self.log.warn("Provider not found for background {}. Not Using.".format(target.target))
            else:
                self.log.info(f"Using provider {provider} for background {target.target}")
                _targets.append(target)

        self.log.info(f"Updating background sequence persistence to {_targets}")
        self._bg_sequence_persistence.update(_targets)
        self.bg_update()

    def bg_update(self):
        sequence_targets = self._bg_sequence_persistence.get()
        if len(sequence_targets) > 1:
            self.bg_sequence = sequence_targets
        elif len(sequence_targets) == 1:
            bg = sequence_targets[0]
            if bg.duration or bg.callback:
                bg = BackgroundSpec(target=bg.target,
                                    bgcolor=bg.bgcolor,
                                    callback=None,
                                    duration=None)
            self._bg_sequence_active = False
            self.bg = bg
        else:
            self._bg_sequence_active = False
            super(BackgroundSequenceMixin, self).bg_update()
