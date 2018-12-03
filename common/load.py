"""
OMOP Loader
"""
import os
import logging
from pprint import pformat, pprint
from copy import deepcopy

from kf_lib_data_ingest.common.misc import read_json, write_json
from kf_model_omop.factory import scoped_session
from kf_model_omop.model import models

from common.target_api_config import schema

logger = logging.getLogger(__name__)

id_model_map = {
    'person_id': 'Person',
    'specimen_id': 'Speciman'
}


def _resolve_links(params, id_cache):
    """
    Look up the value of foreign key properties in the id_cache by the source
    ID or the value used to uniquely identify instances of model_name in the
    source data

    :param model_name: the SQLAlchemy model class name
    :param params: the dict of properties and values needed to create an
    instance of model
    :param id_cache: a dict storing the mapping of source IDs to primary keys
    """
    key = '_links'
    for property, value in params[key].items():
        foreign_model = id_model_map.get(property)
        id_fk_map = id_cache.get(foreign_model)
        if id_fk_map:
            params[key][property] = id_fk_map.get(value, value)

    params.update(params.pop('_links', None))

    return params


def _resolve_primary_key(model_name, params, id_cache):
    """
    Look up the value of the primary key in the id_cache by its source ID
    or the value used to uniquely identify instances of model_name in the
    source data

    :param model_name: the SQLAlchemy model class name
    :param params: the dict of properties and values needed to create an
    instance of model
    :param id_cache: a dict storing the mapping of source IDs to primary keys
    """
    for k, v in params['_primary_key'].items():
        primary_key = k
        source_id = v
        primary_key_value = id_cache[model_name].get(source_id)

    params.pop('_primary_key', None)

    return primary_key, source_id, primary_key_value,


def _fill_values(target_schema, row):
    """
    Helper for load. Fills values of properties in the target schema given
    values from a row in the mapped dataframe
    """
    params = deepcopy(target_schema)

    for key, value in params.items():
        if key not in {'_links', '_primary_key'}:
            params[key] = row.get(value)

    for key in {'_links', '_primary_key'}:
        if params.get(key) is None:
            continue
        for property, value in params[key].items():
            params[key][property] = row.get(value)

    return params


def load(session, df_dict, id_cache):
    """
    Create instances of SQLAlchemy models populated with data from df_dict
    and update or insert them in the OMOP database

    :param session: the current db session
    :param df_dict: dict of dataframes keyed by model_name
    :param id_cache: dict storing source ID to primary key mapping
    """
    for model_cls_name, df in df_dict.items():
        # Lookup model class by name
        model_cls = getattr(models, model_cls_name)

        # Init id cache if needed
        if model_cls_name not in id_cache:
            id_cache[model_cls_name] = {}

        total = df.shape[0]
        logger.info(f'Loading {total} {model_cls_name} instances ...')

        # Get schema for target model
        target_schema = deepcopy(schema.get(model_cls_name))

        # Make model instances
        for i, row in df.iterrows():
            # Fill property values
            params = _fill_values(target_schema, row)
            # Translate values of link properties to db IDs
            result = _resolve_links(params, id_cache)

            (primary_key,
             source_id,
             primary_key_value) = _resolve_primary_key(model_cls_name,
                                                       result,
                                                       id_cache)

            logger.info(f'\t{i} of {total} {model_cls_name}: '
                        f'\n{pformat(result)}')

            # Update model instance
            if primary_key_value:
                instance = session.query(model_cls).get(primary_key_value)
                if instance:
                    for property, value in result.items():
                        setattr(instance, property, value)
                session.flush()
            # Insert model instance
            else:
                instance = model_cls(**result)
                session.add(instance)
                session.flush()
                primary_key_value = getattr(instance, primary_key)

                # Update id cache
                id_cache[model_cls_name][source_id] = primary_key_value

        session.commit()


def delete_all(session, df_dict):
    """
    Delete all instances of models in df_dict's keys
    """
    logger.info('Deleting all previously loaded OMOP instances')
    for model_cls in df_dict.keys():
        results = session.query(model_cls).all()
        logger.info(f'{len(results)} {model_cls.__name__} deleted')
        for r in results:
            session.delete(r)
        session.commit()


def run(df_dict, id_cache_filepath):
    """
    Entry point into the loader
    """
    logger.info('BEGIN LoadStage ...')

    # Read id cache
    id_cache = {}
    if os.path.isfile(id_cache_filepath):
        id_cache = read_json(id_cache_filepath)

    # Use the context managed session to interact with DB
    with scoped_session() as session:
        # delete_all(session, df_dict)
        load(session, df_dict, id_cache)

    # Write id cache
    write_json(id_cache, id_cache_filepath)

    logger.info('END LoadStage ...')