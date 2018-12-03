"""
Delete stuff
"""
import os
import logging

from kf_lib_data_ingest.common.misc import read_json
from kf_model_omop.factory import scoped_session
from kf_model_omop.model import models


logger = logging.getLogger(__name__)

id_model_map = {
    'person_id': 'Person',
    'specimen_id': 'Speciman'
}


def delete_all(session):
    """
    Delete all instances of models in df_dict's keys
    """
    logger.info('Deleting all previously loaded OMOP instances')

    for model_cls_name in reversed(list(id_model_map.values())):
        model_cls = getattr(models, model_cls_name)
        results = session.query(model_cls).all()
        logger.info(f'{len(results)} {model_cls.__name__} deleted')
        for r in results:
            session.delete(r)
        session.commit()


def drop_study(session, id_cache):
    """
    Delete all study entities
    """
    model_name_list = reversed(list(id_model_map.values()))

    for model_cls_name in model_name_list:
        # Lookup model class by name
        model_cls = getattr(models, model_cls_name)

        # Primary Keys
        primary_keys = id_cache.get(model_cls_name, [])

        if (not primary_keys) or (session.query(model_cls).count() == 0):
            logger.info(f'0 {model_cls_name} found, nothing to delete!')
            continue

        # Query for obj then delete it
        for key in primary_keys.values():
            instance = session.query(model_cls).get(key)
            if instance:
                logger.info(f'Deleting {model_cls_name} {key} ...')
                session.delete(instance)

        session.commit()


def run(study_dir):
    """
    Entry point
    """
    logger.info(f'Deleting study {study_dir} entities')

    # Read id cache
    id_cache = {}
    id_cache_filepath = os.path.join(study_dir, 'id_cache.json')
    if os.path.isfile(id_cache_filepath):
        id_cache = read_json(id_cache_filepath)

    # Use the context managed session to interact with DB
    with scoped_session() as session:
        drop_study(session, id_cache)
