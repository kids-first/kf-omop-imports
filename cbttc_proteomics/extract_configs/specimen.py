# flake8: noqa

import logging
import datetime

import pandas as pd

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map,
    melt_map
)
from kf_lib_data_ingest.common import constants as kf_constants
from common import constants as omop_constants
from common.concept_schema import OMOP
from common.athena import athena_cache

logger = logging.getLogger(__name__)

source_data_url = (
    'file://~/Projects/kids_first/data/CBTTC/proteomics/cbttc-proteomics.xlsx'
)


def post_load(df):
    # reshape
    value_vars = ['normal_dna_biospecimen_id',
                  'tumor_dna_biospecimen_id',
                  'tumor_rna_biospecimen_id']
    id_vars = set(df.columns) - set(value_vars)
    new_df = pd.melt(df, id_vars=id_vars,
                     value_vars=value_vars,
                     var_name='disease_status',
                     value_name='specimen_id')

    return new_df


source_data_loading_parameters = {
    'sheet_name': 'All Fields - Included - 11_05_2',
    'do_after_load': post_load
}


def anatomic_site(x):
    x = x.strip()

    if 'Brain Stem- Midbrain' in x:
        value = omop_constants.CONCEPT.SPECIMEN.ANATOMIC_SITE.BRAIN_STEM_PART
    elif 'Spinal Cord- Thoracic' in x:
        value = (
            omop_constants.CONCEPT.SPECIMEN.ANATOMIC_SITE.SPINAL_CORD.THORACIC
        )
    elif 'Spinal Cord- Cervical' in x:
        value = (
            omop_constants.CONCEPT.SPECIMEN.ANATOMIC_SITE.SPINAL_CORD.CERVICAL
        )
    elif 'Spinal Cord- Lumbar' in x:
        value = (
            omop_constants.CONCEPT.SPECIMEN.ANATOMIC_SITE.SPINAL_CORD.CERVICAL
        )
    else:
        value = athena_cache.lookup(x.split('/')[0].split(',')[0])

    return value


operations = [
    # specimen source value
    keep_map(
        in_col='specimen_id',
        out_col=OMOP.SPECIMEN.ID
    ),
    # specimen source value
    keep_map(
        in_col='sample_subject_name',
        out_col=OMOP.SPECIMEN.SOURCE_VALUE
    ),
    # person external_id
    keep_map(
        in_col='research_id',
        out_col=OMOP.PERSON.ID
    ),
    # specimen concept id
    constant_map(
        m=omop_constants.CONCEPT.SPECIMEN.COMPOSITION.BRAIN_TISSUE,
        out_col=OMOP.SPECIMEN.CONCEPT_ID
    ),
    # specimen type concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.SPECIMEN.TYPE.CONCEPT_ID
    ),
    # specimen anatomic concept id
    value_map(
        in_col='tumor_primary_location_in',
        m=lambda x: int(anatomic_site(x)),
        out_col=OMOP.SPECIMEN.ANATOMIC_SITE.CONCEPT_ID
    ),
    # specimen anatomic source value
    value_map(
        in_col='tumor_primary_location_in',
        m=lambda x: x[:50],
        out_col=OMOP.SPECIMEN.ANATOMIC_SITE.SOURCE_VALUE
    ),
    # specimen disease status source value
    value_map(
        in_col='disease_status',
        m=lambda x: '-'.join(x.split('_')[0:2]),
        out_col=OMOP.SPECIMEN.DISEASE_STATUS.SOURCE_VALUE
    ),
    # specimen disease status concept id
    value_map(
        in_col='disease_status',
        m=lambda x: (omop_constants.CONCEPT.DISEASE_STATUS.NORMAL
                     if 'normal' in x else
                     omop_constants.CONCEPT.DISEASE_STATUS.ABNORMAL),
        out_col=OMOP.SPECIMEN.DISEASE_STATUS.CONCEPT_ID
    ),
    # specimen datetime, assume birthdate of person is epoch
    value_map(
        in_col='age_of_initial_diagnosis',
        m=lambda x: str(datetime.datetime.fromtimestamp(0) +
                        datetime.timedelta(float(x) - 1)),
        out_col=OMOP.SPECIMEN.DATETIME
    )
]
