

import os
import re
import shutil
from twisted.internet.defer import inlineCallbacks
from twisted.internet.threads import deferToThread

from ebs.linuxnode.exim.mixin import LocalEximMixin
from ebs.linuxnode.exim.local import ImportSpec
from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.core.background import BackgroundSpec

from .basic import BackgroundSequenceMixin


class BackgroundSequenceImporterMixin(BackgroundSequenceMixin, LocalEximMixin):
    _regex_duration = re.compile(r".(?P<numeric>\d+)(?P<unit>[smh]).")
    _regex_structured = re.compile(r"^(\d+_)?(?P<target>structured:\S*?)(?P<duration>\.(?P<numeric>\d+)(?P<unit>[smh]))?$")  # noqa
    _multipliers = {'s': 1, 'm': 60, 'h': 3600}
    _force_duration_ext = ('.png', '.jpg', '.bmp', '.gif', '.jpeg')

    def __init__(self, *args, **kwargs):
        super(BackgroundSequenceImporterMixin, self).__init__(*args, **kwargs)
        self._allowed_structured_backgrounds = []

    def register_structured_background(self, background):
        self._allowed_structured_backgrounds.append(background)

    @property
    def _bg_local_path(self):
        return os.path.join(self.cache_dir, 'bg')

    @inlineCallbacks
    def _import_backgrounds(self, source_path):
        self.log.info("Importing Backgrounds from '{}' to '{}'"
                      "".format(source_path, self._bg_local_path))
        if not os.path.exists(self._bg_local_path):
            os.makedirs(self._bg_local_path, exist_ok=True)
        yield self.exim.clear_directory(self._bg_local_path)
        _targets = []
        for filename in sorted(os.listdir(source_path)):
            source_filepath = os.path.join(source_path, filename)
            dest_filepath = os.path.join(self._bg_local_path, filename)
            if not os.path.isfile(source_filepath):
                continue

            self.log.info("Copying {} from {} to {}"
                          "".format(filename, source_path, self._bg_local_path))
            yield deferToThread(shutil.copy, source_filepath, dest_filepath)

            _duration = None

            structured = self._regex_structured.match(filename)
            if structured:
                target = structured.groupdict()['target']
                if filename.split(':')[1] in self._allowed_structured_backgrounds:
                    dest_filepath = target
                else:
                    continue
                if structured.groupdict()['duration']:
                    unit = structured.groupdict()['unit']
                    multiplier = self._multipliers[unit]
                    _duration = structured.groupdict()['numeric'] * multiplier
                else:
                    _duration = 30

            if not _duration:
                _duration = self._regex_duration.search(filename, re.IGNORECASE)
                if _duration:
                    unit = _duration.groupdict()['unit']
                    multiplier = self._multipliers[unit]
                    _duration = _duration.groupdict()['numeric'] * multiplier

            if not _duration:
                ext = os.path.splitext(filename)[1]
                if ext and ext in self._force_duration_ext:
                    _duration = 10

            if _duration:
                _target = BackgroundSpec(dest_filepath, duration=_duration)
            else:
                _target = dest_filepath
            _targets.append(_target)
        self.background_sequence_set(_targets)

    def install(self):
        super(BackgroundSequenceImporterMixin, self).install()
        _elements = {
            'exim_local_background': ElementSpec('exim', 'local_background',
                                                 ItemSpec(bool, read_only=False, fallback=False)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)
        target_path = self._bg_local_path
        if self.config.exim_local_background:
            spec = ImportSpec(target_path, source='[id]?',
                              writer=self._import_backgrounds,
                              contexts=['startup'])
            self.exim.register_import('bg', spec)
