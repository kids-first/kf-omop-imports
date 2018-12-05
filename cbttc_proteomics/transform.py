
from common.concept_schema import OMOP
from common.utils import merge_without_duplicates


def transform(dfs):

    # Person
    persons = dfs['person']

    # Specimens
    # TODO

    # Diagnoses - condition occurrence
    diagnoses = dfs['diagnosis']

    df_out = {
        'Person': persons,
        'ConditionOccurrence': diagnoses
        # 'Speciman': specimens
    }

    return df_out
