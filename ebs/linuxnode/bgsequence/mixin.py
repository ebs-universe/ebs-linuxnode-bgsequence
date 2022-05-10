

try:
    from .importer import BackgroundSequenceImporterMixin
    EffectiveBackgroundMixin = BackgroundSequenceImporterMixin
except ImportError:
    from .basic import BackgroundSequenceMixin
    EffectiveBackgroundMixin = BackgroundSequenceMixin
