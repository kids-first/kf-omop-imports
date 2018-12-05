
from common.concept_schema import OMOP
from common.utils import merge_without_duplicates


def transform(dfs):

    # Person
    persons = dfs['person']

    # Specimens
    specimens = dfs['specimen']

    # Diagnoses - condition occurrence
    diagnoses = dfs['diagnosis']

    # Outcomes
    outcomes = dfs['outcome']

    df_out = {
        'Person': persons,
        'ConditionOccurrence': diagnoses,
        'Speciman': specimens,
        'Observation': outcomes
    }

    return df_out
