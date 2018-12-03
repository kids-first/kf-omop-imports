# flake8: noqa
from pandas import read_csv

from kf_lib_data_ingest.etl.extract.operations import (
    value_map,
    keep_map,
    constant_map
)
from kf_lib_data_ingest.common import constants as kf_constants
from common import constants as omop_constants
from common.concept_schema import OMOP

source_data_url = (
    'file://~/Projects/kids_first/data/Vilain_2015/dbgap/3a_dbGaP_SampleAttributesDSproofed.txt'
)


source_data_loading_parameters = {
    'load_func': read_csv,
    'sep': '\t'
}


def body_site_map(x):
    m = {
        "B": omop_constants.CONCEPT.SPECIMEN.COMPOSITION.BLOOD,
        "FTL": omop_constants.CONCEPT.COMMON.NO_MATCH,
        "FTU": omop_constants.CONCEPT.COMMON.NO_MATCH,
        "S": omop_constants.CONCEPT.COMMON.NO_MATCH,
        "TP": omop_constants.CONCEPT.COMMON.NO_MATCH,
        "U": omop_constants.CONCEPT.COMMON.NO_MATCH,
        "default": omop_constants.CONCEPT.COMMON.NO_MATCH
    }
    return m.get(x, m.get('default'))


operations = [
    # specimen source id and external_id
    keep_map(
        in_col='SAMPLE_ID',
        out_col=OMOP.SPECIMEN.ID
    ),
    # specimen source value
    keep_map(
        in_col="BODY_SITE",
        out_col=OMOP.SPECIMEN.SOURCE_VALUE
    ),
    # specimen concept id
    value_map(
        in_col="BODY_SITE",
        m=lambda x: body_site_map(x),
        out_col=OMOP.SPECIMEN.CONCEPT_ID
    ),
    # specimen type concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.SPECIMEN.TYPE.CONCEPT_ID
    ),
    # specimen anatomic concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.SPECIMEN.ANATOMIC_SITE.CONCEPT_ID
    ),
    # specimen anatomic source value
    constant_map(
        m=kf_constants.COMMON.NOT_REPORTED,
        out_col=OMOP.SPECIMEN.ANATOMIC_SITE.SOURCE_VALUE
    ),
    # specimen disease status concept id
    constant_map(
        m=omop_constants.CONCEPT.COMMON.NO_MATCH,
        out_col=OMOP.SPECIMEN.DISEASE_STATUS.CONCEPT_ID
    ),
    # specimen disease status source value
    constant_map(
        m=kf_constants.COMMON.NOT_REPORTED,
        out_col=OMOP.SPECIMEN.DISEASE_STATUS.SOURCE_VALUE
    ),

]
