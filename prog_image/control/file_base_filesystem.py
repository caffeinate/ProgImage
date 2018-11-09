'''
Created on 9 Nov 2018

@author: si
'''
import json
import os

from prog_image.control.file_base import FileBase

class FileBaseFilesystem(FileBase):
    """
    File system implementation.
    Can use local or network filesystems.
    """
    def file_exists(self):
        return os.access(self.stored_location, os.R_OK)

    @property
    def _stored_parts(self):
        """
        don't make big directories, spread it
        :returns: tuple (new_base_path, filename)
        """
        sf = self.stored_file
        path = self.base_path + sf[0] + '/' + sf[1] + '/'
        return (path, self.stored_file)

    @property
    def stored_location(self):
        """
        :returns: (str) full path to file
        """
        sf = self._stored_parts
        # don't make big directories, spread it
        return sf[0]+sf[1]

    def save(self, file_like):
        os.makedirs(self._stored_parts[0], exist_ok=True)
        file_like.save(self.stored_location)
        
        if self.meta_data:
            meta_file = self.stored_location+'.meta'
            with open(meta_file, 'w') as f:
                f.write(json.dumps(self.meta_data))
