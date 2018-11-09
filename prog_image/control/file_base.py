'''
Created on 9 Nov 2018

@author: si
'''
class FileBase:
    """
    Informal abstract class.

    Files don't belong in a database. They could be in an object store like S3
    or file system.

    This class looks after a single file.
    """
    def __init__(self, base_path):
        """
        :param: base_path (str) base location which is meaningful to subclasses.
         e.g. base url
        """
        self.base_path = base_path
        self.stored_file = None # file name without path
        self._meta_data = None # anything useful could be stored in meta data.
                            # for now, just original filename must be JSON
                            # serialisable.

    def file_exists(self):
        raise NotImplementedError()

    @property
    def stored_location(self):
        """
        :returns: (str) absolute path to file, meaning depends on subclass
        """
        raise NotImplementedError()

    def save(self, file_like):
        """
        save raw data to disk and meta data if there is any.

        :param: file_like has the save() method
        """
        raise NotImplementedError()

    def get_meta_data(self):
        raise NotImplementedError()

    def set_meta_data(self, md):
        self._meta_data = md

    meta_data = property(get_meta_data, set_meta_data)
