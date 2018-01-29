import json
import os


def mkdirs(dirs):
    """ Create `dirs` if not exist. """
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def save_to_file(item, fname):
    """ input:
            item - a dict like object
            fname - where to save
    """
    with open(fname, 'w') as f:
        json.dump(dict(item), f)
