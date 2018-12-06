import inspect

from sqlalchemy.inspection import inspect as sqlainspect
import pandas as pd

from kf_model_omop.model import models


def merge_without_duplicates(left, right, left_key='Left',
                             right_key='Right', **kwargs):
    """
    Merge two DataFrames and remove duplicate columns resulting from merge
    A merge of two DataFrames can result in duplicate columns suffixed with
    _x and _y. Choose the column with the most values.
    """
    df = None

    # Ensure both DataFrames exist
    error_messages = []
    if not isinstance(left, pd.DataFrame) and (not left.empty):
        error_messages.append('{} DataFrame is {}.'.format(left_key, left))
    if not isinstance(right, pd.DataFrame) and (not right.empty):
        error_messages.append('{} DataFrame is {}.'.format(right_key, right))
    # One or both DataFrames do not exist
    if error_messages:
        msg = 'Warning: Could not merge DataFrames. '
        additional_msgs = ' '.join(error_messages)
        print(msg + additional_msgs)
        return df

    # Save duplicate columns
    duplicate_cols = set(list(left.columns)).intersection(list(right.columns))

    # Merge
    try:
        df = pd.merge(left, right, **kwargs)
    # One of the DataFrames did not have the merge_col
    except KeyError as e:
        missing_col = str(e)
        bad_df = (left_key
                  if missing_col not in set(list(left.columns))
                  else right_key)
        print('Warning: Could not merge {0} DataFrame with {1} DataFrame '
              'on column "{2}". "{2}" not found in columns of {3}'
              .format(left_key, right_key, missing_col, bad_df))

        raise e

    # No common columns found to merge on
    except pd.errors.MergeError as e:
        print('Warning: Could not merge {0} DataFrame with {1} DataFrame. '
              'No common columns to perform merge on.'.format(left_key,
                                                              right_key))
        raise e

    # Replace NaN values with None
    df = df.where((pd.notnull(df)), None)

    for prefix in duplicate_cols:
        # Get duplicate columns
        col_x = prefix + '_x'
        col_y = prefix + '_y'

        if not ((col_x in df) and (col_y in df)):
            continue

        # Keep column with greatest # of unique values (excluding NaN/None)
        unique_vals_x = set(df[col_x].unique())
        unique_vals_x.discard(None)
        unique_vals_y = set(df[col_y].unique())
        unique_vals_y.discard(None)

        if len(unique_vals_x) >= len(unique_vals_y):
            keep_col = col_x
            drop_col = col_y
        else:
            keep_col = col_y
            drop_col = col_x

        # Reduce two duplicate columns to one
        df.drop(drop_col, axis=1, inplace=True)
        df.rename(columns={keep_col: prefix}, inplace=True)

    return df


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
