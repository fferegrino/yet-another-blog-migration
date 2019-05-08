import os
from shutil import copy

import click

image_types = set(['jpg', 'jpeg', '.gif', 'png'])
sources = set(['pxm', 'sketch', 'sketch'])

extensions = set()


@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False))
@click.argument('destiny', type=click.Path(exists=True, file_okay=False))
@click.option('--verbose', is_flag=True)
def migrate_images(source, destiny, verbose):
    for root, directories, files in os.walk(source):
        for file in files:
            name, extension = os.path.splitext(file)
            extension = extension[1:]

            if extension.lower() in image_types:
                old_path = os.path.join(root, file)
                old_new_path = old_path[len(source):]
                new_name = '__'.join(old_new_path.split('/'))

                if verbose:
                    print(f'Will copy {old_path} to {destiny}')

                copy(old_path, destiny)

                old_file = os.path.join(destiny, file)
                new_file = os.path.join(destiny, new_name)

                if verbose:
                    print(f'Will rename {old_file} to {new_file}')

                os.rename(old_file, new_file)


if __name__ == "__main__":
    migrate_images()
