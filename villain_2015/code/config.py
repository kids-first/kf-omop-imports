import os
import inspect
from sqlalchemy.inspection import inspect as sqlainspect
from sqlalchemy.orm import (
    class_mapper,
    ColumnProperty
)

from kf_model_omop.model import models

STUDY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(STUDY_DIR, 'output')
CONFIG_DIR = os.path.join(STUDY_DIR, 'extract_configs')
ID_CACHE_FILE = os.path.join(STUDY_DIR, 'id_cache.json')


def _get_live_classes(module, full_module_name):
    """
    Return list of classes that are defined in the python module

    :param: an imported Python module
    :param: fully qualified name of Python module (ie. my_package.my_module)
    """
    return [getattr(module, m[0])
            for m in inspect.getmembers(module, inspect.isclass)
            if m[1].__module__ == full_module_name
            ]


def _make_omop_schema():
    """
    Build a dictionary, where keys are OMOP sqlalchemy model names and values
    are dictionaries of the model's attributes.
    Example:
        omop_schema = {
            'CareSite': {
                'care_site_id': None,
                 'care_site_name': None
            },
            ...
        }
    """
    omop_schema = {}
    classes = _get_live_classes(models, 'kf_model_omop.model.models')
    for cls in classes:
        d = {'_links': {},
             '_primary_key': {}}
        for c in sqlainspect(cls).columns:
            if c.foreign_keys and (not c.primary_key):
                d['_links'][c.name] = None
            elif c.primary_key:
                d['_primary_key'][c.name] = None
            else:
                d[c.name] = None
        omop_schema[cls.__name__] = d

    return omop_schema
