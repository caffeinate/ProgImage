'''
Created on 9 Nov 2018

@author: si
'''
from PIL import Image

class ImageAnvil:
    """
    Transform source image into output image.
    """
    def _get_transform_method(self, transform_name):
        if transform_name == 'thumbnail':
            return self._transform_to_thumbnail
        
        return None

    def is_valid_transform(self, transform_name, args=None):
        if self._get_transform_method(transform_name):
            return True
        else:
            return False
    
    def transform(self, transform_name, input_file, output_file,
                  transform_args=None):
        
        transform_method = self._get_transform_method(transform_name)
        assert transform_method is not None
        return transform_method(input_file, output_file, transform_args)
        
    def _transform_to_thumbnail(self, input_file, output_file, transform_args):
        if transform_args:
            size = int(transform_args), int(transform_args)
        else:
            size = 128, 128

        im = Image.open(input_file)
        im.thumbnail(size)
        im.save(output_file, "JPEG")
