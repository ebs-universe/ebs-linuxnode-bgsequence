

from .models import BackgroundModel
from .models import metadata

from ebs.linuxnode.db.sequence import GenericSequencePersistenceManager


class BackgroundSequencePersistenceManager(GenericSequencePersistenceManager):
    _db_name = 'background'
    _db_model = BackgroundModel
    _db_metadata = metadata

    def _insert_item(self, seq, item):
        # Item is to be inserted into the resource_manager by the caller.
        # The caller should also ensure the resources are downloaded and
        # available before it is set.
        pass

    def _clear_item(self, item):
        if self._actual.resource_manager.has(item.target):
            r = self._actual.resource_manager.get(item.target)
            r.rtype = None
            r.commit()
