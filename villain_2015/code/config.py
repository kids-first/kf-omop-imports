import os
import inspect
from sqlalchemy.orm import (
    class_mapper,
    ColumnProperty
)

from kf_model_omop.model import models

STUDY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(STUDY_DIR, 'output')
CONFIG_DIR = os.path.join(STUDY_DIR, 'extract_configs')


def get_live_classes(module, full_module_name):
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
    classes = get_live_classes(models, 'kf_model_omop.model.models')
    for cls in classes:
        mapper = class_mapper(cls)
        d = dict()
        for prop in mapper.iterate_properties:
            if isinstance(prop, ColumnProperty):
                d[prop.key] = None
        omop_schema[cls.__name__] = d

    return omop_schema
