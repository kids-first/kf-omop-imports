# flake8: noqa
import datetime

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map,
    row_map
)
from kf_lib_data_ingest.common import constants as kf_constants
from common import constants as omop_constants
from common import athena
from common.concept_schema import OMOP
from common.athena import athena_cache

source_data_url = (
    'file://~/Projects/kids_first/data/CBTTC/proteomics/cbttc-proteomics.xlsx'
)


def post_load(df):
    return df[df['chemo'] == 'Yes']


source_data_loading_parameters = {
    'sheet_name': 'All Fields - Included - 11_05_2',
    'do_after_load': post_load
}


def procedure_occur_id(row):
    external_id = ''
    components = ['research_id', 'chemo_type',
                  'start_age_chemo', 'stop_age_chemo']

    external_id = '-'.join([f'{col}:{str(row[col])}' for col in components])

    return external_id


def chemo_start(row):
    x = row['start_age_chemo'].lower()
    if ('unavailable' not in x) and ('not applicable') in x:
        value = str(datetime.datetime.fromtimestamp(0) +
                    datetime.timedelta(float(x) - 1))
    else:
        value = str(
            datetime.datetime.fromtimestamp(0) +
            datetime.timedelta(float(row['age_of_initial_diagnosis']) - 1))

    return value


operations = [
    # procedure external_id
    row_map(
        m=lambda row: procedure_occur_id(row),
        out_col=OMOP.PROCEDURE.ID
    ),
    # person external_id
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.ID
    ),
    # procedure source value
    row_map(
        m=lambda row: ('Chemotherapy ' +
                       ':'.join([f'{col}: {row[col]}'
                                 for col in ['chemo_type',
                                             'like_protocol_name',
                                             'Chemo_agents',
                                             'Formulation']]
                                )
                       ),
        out_col=OMOP.PROCEDURE.SOURCE_VALUE
    ),
    # procedure concept id
    constant_map(
        m=athena_cache.lookup('chemotherapy',
                              query_params={'domain': 'Procedure',
                                            'standardConcept': 'Standard',
                                            'conceptClass': 'Procedure'}),
        out_col=OMOP.PROCEDURE.CONCEPT_ID
    ),
    # procedure type
    constant_map(
        m=athena_cache.lookup('radiation',
                              query_params={'standardConcept': 'Standard'}),
        out_col=OMOP.PROCEDURE.TYPE.CONCEPT_ID
    ),
    # procedure_start_datetime
    # consider epoch to be person's year of birth
    row_map(
        m=lambda row: chemo_start(row),
        out_col=OMOP.PROCEDURE.DATETIME
    ),
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.PROCEDURE.MODIFIER.CONCEPT_ID
    ),
    constant_map(
        m=omop_constants.CONCEPT.COMMON.UNAVAILABLE,
        out_col=OMOP.PROCEDURE.SOURCE_CONCEPT_ID
    )

]
