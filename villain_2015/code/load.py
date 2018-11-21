"""
OMOP Loader
"""
import os
import logging
from pprint import pformat, pprint
from copy import deepcopy

from kf_lib_data_ingest.common.misc import read_json, write_json
from kf_model_omop.factory import scoped_session

from config import ID_CACHE_FILE
from target_api_config import schema

logger = logging.getLogger(__name__)


def _resolve_links(model_name, params, id_cache):
    if id_cache and (model_name in id_cache):
        id_lookup = id_cache.get(model_name)

        key = '_links'
        for property, value in params[key].items():
            params[key][property] = id_lookup.get(value, value)

    params.update(params.pop('_links', None))

    return params


def _resolve_primary_key(model_name, result, id_cache):
    for k, v in result['_primary_key'].items():
        primary_key = k
        external_id = v
        primary_key_value = id_cache[model_name].get(external_id)

    result.pop('_primary_key', None)

    return primary_key, external_id, primary_key_value,


def _fill_values(target_schema, previous, row):
    """
    Helper for load
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
    for model_cls, df in df_dict.items():
        model_cls_name = model_cls.__name__

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
            params = _fill_values(target_schema, None, row)
            # Translate values of link properties to db IDs
            result = _resolve_links(model_cls, params, id_cache)

            (primary_key,
             external_id,
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
                id_cache[model_cls_name][external_id] = primary_key_value

        session.commit()


def delete_all(session, df_dict):
    logger.info('Deleting all previously loaded OMOP instances')
    for model_cls in df_dict.keys():
        results = session.query(model_cls).all()
        logger.info(f'{len(results)} {model_cls.__name__} deleted')
        for r in results:
            session.delete(r)
        session.commit()


def run(df_dict):
    logger.info('BEGIN LoadStage ...')

    # Read id cache
    id_cache = {}
    if os.path.isfile(ID_CACHE_FILE):
        id_cache = read_json(ID_CACHE_FILE)

    # Use the context managed session to interact with DB
    with scoped_session() as session:
        # delete_all(session, df_dict)
        load(session, df_dict, id_cache)

    # Write id cache
    write_json(id_cache, ID_CACHE_FILE)

    logger.info('END LoadStage ...')
