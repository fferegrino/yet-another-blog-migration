import os
from shutil import copy
import ntpath

original_path = '/Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/postimages'
dst_path = '/Users/antonioferegrino/Documents/GitHub/yet-another-blog-migration/content/images'

image_types = set(['jpg', 'jpeg', '.gif', 'png'])
sources = set(['pxm', 'sketch', 'sketch'])


extensions =  set()
def traverse_tree(dir):
    for root, directories, files in os.walk(dir):
        for file in files:
            name, extension = os.path.splitext(file)
            extension = extension[1:]


            if extension.lower() in image_types:
                old_path = os.path.join(root, file)
                old_new_path = old_path[len(original_path) + 1:]
                new_name = '__'.join( old_new_path.split('/'))

                copy(old_path, dst_path)

                print(f'will copy {old_path} to {dst_path}')

                old_file = os.path.join(dst_path, file)
                new_file = os.path.join(dst_path, new_name)

                os.rename(old_file, new_file)

