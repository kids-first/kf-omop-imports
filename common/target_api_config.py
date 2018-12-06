# flake8: noqa

"""
OMOP Target Model config
"""

from common.concept_schema import OMOP


schema = {
    "CareSite": {
        "_links": {
            "location_id": None,
            "place_of_service_concept_id": None
        },
        "_primary_key": {
            "care_site_id": None
        },
        "care_site_name": None,
        "care_site_source_value": None,
        "place_of_service_source_value": None
    },
    "Concept": {
        "_links": {
            "concept_class_id": None,
            "domain_id": None,
            "vocabulary_id": None
        },
        "_primary_key": {
            "concept_id": None
        },
        "concept_code": None,
        "concept_name": None,
        "invalid_reason": None,
        "standard_concept": None,
        "valid_end_date": None,
        "valid_start_date": None
    },
    "ConceptAncestor": {
        "_links": {
            "ancestor_concept_id": None,
            "descendant_concept_id": None
        },
        "_primary_key": {},
        "max_levels_of_separation": None,
        "min_levels_of_separation": None
    },
    "ConceptClass": {
        "_links": {
            "concept_class_concept_id": None
        },
        "_primary_key": {
            "concept_class_id": None
        },
        "concept_class_name": None
    },
    "ConceptRelationship": {
        "_links": {
            "concept_id_1": None,
            "concept_id_2": None,
            "relationship_id": None
        },
        "_primary_key": {},
        "invalid_reason": None,
        "valid_end_date": None,
        "valid_start_date": None
    },
    "ConditionEra": {
        "_links": {
            "condition_concept_id": None,
            "person_id": None
        },
        "_primary_key": {
            "condition_era_id": None
        },
        "condition_era_end_datetime": None,
        "condition_era_start_datetime": None,
        "condition_occurrence_count": None
    },
    "ConditionOccurrence": {
        "_links": {
            "condition_concept_id": OMOP.CONDITION.CONCEPT_ID,
            "condition_source_concept_id": OMOP.CONDITION.SOURCE_CONCEPT_ID,
            "condition_status_concept_id": OMOP.CONDITION.STATUS.CONCEPT_ID,
            "condition_type_concept_id": OMOP.CONDITION.TYPE.CONCEPT_ID,
            "person_id": OMOP.PERSON.ID,
            "provider_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "condition_occurrence_id": OMOP.CONDITION.ID
        },
        "condition_end_date": None,
        "condition_end_datetime": None,
        "condition_source_value": OMOP.CONDITION.SOURCE_VALUE,
        "condition_start_date": None,
        "condition_start_datetime": OMOP.CONDITION.DATETIME,
        "condition_status_source_value": OMOP.CONDITION.STATUS.SOURCE_VALUE,
        "stop_reason": None
    },
    "Cost": {
        "_links": {
            "cost_concept_id": None,
            "cost_source_concept_id": None,
            "cost_type_concept_id": None,
            "currency_concept_id": None,
            "drg_concept_id": None,
            "payer_plan_period_id": None,
            "person_id": None,
            "revenue_code_concept_id": None
        },
        "_primary_key": {
            "cost_id": None
        },
        "billed_date": None,
        "cost": None,
        "cost_event_field_concept_id": None,
        "cost_event_id": None,
        "cost_source_value": None,
        "drg_source_value": None,
        "incurred_date": None,
        "paid_date": None,
        "revenue_code_source_value": None
    },
    "DeviceExposure": {
        "_links": {
            "device_concept_id": None,
            "device_source_concept_id": None,
            "device_type_concept_id": None,
            "person_id": None,
            "provider_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "device_exposure_id": None
        },
        "device_exposure_end_date": None,
        "device_exposure_end_datetime": None,
        "device_exposure_start_date": None,
        "device_exposure_start_datetime": None,
        "device_source_value": None,
        "quantity": None,
        "unique_device_id": None
    },
    "Domain": {
        "_links": {
            "domain_concept_id": None
        },
        "_primary_key": {
            "domain_id": None
        },
        "domain_name": None
    },
    "DoseEra": {
        "_links": {
            "drug_concept_id": None,
            "person_id": None,
            "unit_concept_id": None
        },
        "_primary_key": {
            "dose_era_id": None
        },
        "dose_era_end_datetime": None,
        "dose_era_start_datetime": None,
        "dose_value": None
    },
    "DrugEra": {
        "_links": {
            "drug_concept_id": None,
            "person_id": None
        },
        "_primary_key": {
            "drug_era_id": None
        },
        "drug_era_end_datetime": None,
        "drug_era_start_datetime": None,
        "drug_exposure_count": None,
        "gap_days": None
    },
    "DrugExposure": {
        "_links": {
            "drug_concept_id": None,
            "drug_source_concept_id": None,
            "drug_type_concept_id": None,
            "person_id": None,
            "provider_id": None,
            "route_concept_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "drug_exposure_id": None
        },
        "days_supply": None,
        "dose_unit_source_value": None,
        "drug_exposure_end_date": None,
        "drug_exposure_end_datetime": None,
        "drug_exposure_start_date": None,
        "drug_exposure_start_datetime": None,
        "drug_source_value": None,
        "lot_number": None,
        "quantity": None,
        "refills": None,
        "route_source_value": None,
        "sig": None,
        "stop_reason": None,
        "verbatim_end_date": None
    },
    "DrugStrength": {
        "_links": {
            "amount_unit_concept_id": None,
            "denominator_unit_concept_id": None,
            "drug_concept_id": None,
            "ingredient_concept_id": None,
            "numerator_unit_concept_id": None
        },
        "_primary_key": {},
        "amount_value": None,
        "box_size": None,
        "denominator_value": None,
        "invalid_reason": None,
        "numerator_value": None,
        "valid_end_date": None,
        "valid_start_date": None
    },
    "Location": {
        "_links": {},
        "_primary_key": {
            "location_id": None
        },
        "address_1": None,
        "address_2": None,
        "city": None,
        "country": None,
        "county": None,
        "latitude": None,
        "location_source_value": None,
        "longitude": None,
        "state": None,
        "zip": None
    },
    "LocationHistory": {
        "_links": {
            "location_id": None,
            "relationship_type_concept_id": None
        },
        "_primary_key": {
            "location_history_id": None
        },
        "domain_id": None,
        "end_date": None,
        "entity_id": None,
        "start_date": None
    },
    "Measurement": {
        "_links": {
            "measurement_concept_id": None,
            "measurement_source_concept_id": None,
            "measurement_type_concept_id": None,
            "operator_concept_id": None,
            "person_id": None,
            "provider_id": None,
            "unit_concept_id": None,
            "value_as_concept_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "measurement_id": None
        },
        "measurement_date": None,
        "measurement_datetime": None,
        "measurement_source_value": None,
        "measurement_time": None,
        "range_high": None,
        "range_low": None,
        "unit_source_value": None,
        "value_as_number": None,
        "value_source_value": None
    },
    "Note": {
        "_links": {
            "encoding_concept_id": None,
            "language_concept_id": None,
            "note_class_concept_id": None,
            "note_type_concept_id": None,
            "person_id": None,
            "provider_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "note_id": None
        },
        "note_date": None,
        "note_datetime": None,
        "note_event_field_concept_id": None,
        "note_event_id": None,
        "note_source_value": None,
        "note_text": None,
        "note_title": None
    },
    "NoteNlp": {
        "_links": {
            "note_id": None,
            "note_nlp_concept_id": None,
            "note_nlp_source_concept_id": None,
            "section_concept_id": None
        },
        "_primary_key": {
            "note_nlp_id": None
        },
        "lexical_variant": None,
        "nlp_date": None,
        "nlp_datetime": None,
        "nlp_system": None,
        "offset": None,
        "snippet": None,
        "term_exists": None,
        "term_modifiers": None,
        "term_temporal": None
    },
    "Observation": {
        "_links": {
            "observation_concept_id": OMOP.OBSERVATION.CONCEPT_ID,
            "observation_source_concept_id": OMOP.OBSERVATION.SOURCE_CONCEPT_ID,
            "observation_type_concept_id": OMOP.OBSERVATION.TYPE.CONCEPT_ID,
            "person_id": OMOP.PERSON.ID,
            "provider_id": None,
            "qualifier_concept_id": None,
            "unit_concept_id": None,
            "value_as_concept_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None,
            "obs_event_field_concept_id": OMOP.OBSERVATION.EVENT_FIELD.CONCEPT_ID,
        },
        "_primary_key": {
            "observation_id": OMOP.OBSERVATION.ID
        },
        "observation_date": None,
        "observation_datetime": OMOP.OBSERVATION.DATETIME,
        "observation_event_id": None,
        "observation_source_value": OMOP.OBSERVATION.SOURCE_VALUE,
        "qualifier_source_value": None,
        "unit_source_value": None,
        "value_as_datetime": None,
        "value_as_number": None,
        "value_as_string": None
    },
    "ObservationPeriod": {
        "_links": {
            "period_type_concept_id": None,
            "person_id": None
        },
        "_primary_key": {
            "observation_period_id": None
        },
        "observation_period_end_date": None,
        "observation_period_start_date": None
    },
    "PayerPlanPeriod": {
        "_links": {
            "contract_concept_id": None,
            "contract_person_id": None,
            "contract_source_concept_id": None,
            "payer_concept_id": None,
            "payer_source_concept_id": None,
            "person_id": None,
            "plan_concept_id": None,
            "plan_source_concept_id": None,
            "sponsor_concept_id": None,
            "sponsor_source_concept_id": None,
            "stop_reason_concept_id": None,
            "stop_reason_source_concept_id": None
        },
        "_primary_key": {
            "payer_plan_period_id": None
        },
        "contract_source_value": None,
        "family_source_value": None,
        "payer_plan_period_end_date": None,
        "payer_plan_period_start_date": None,
        "payer_source_value": None,
        "plan_source_value": None,
        "sponsor_source_value": None,
        "stop_reason_source_value": None
    },
    "Person": {
        "_links": {
            "care_site_id": None,
            "ethnicity_concept_id": OMOP.ETHNICITY.CONCEPT_ID,
            "ethnicity_source_concept_id": OMOP.ETHNICITY.SOURCE_CONCEPT_ID,
            "gender_concept_id": OMOP.GENDER.CONCEPT_ID,
            "gender_source_concept_id": OMOP.GENDER.SOURCE_CONCEPT_ID,
            "location_id": None,
            "provider_id": None,
            "race_concept_id": OMOP.RACE.CONCEPT_ID,
            "race_source_concept_id": OMOP.RACE.SOURCE_CONCEPT_ID
        },
        "_primary_key": {
            "person_id": OMOP.PERSON.ID
        },
        "birth_datetime": None,
        "day_of_birth": None,
        "death_datetime": None,
        "ethnicity_source_value": OMOP.ETHNICITY.SOURCE_VALUE,
        "gender_source_value": OMOP.GENDER.SOURCE_VALUE,
        "month_of_birth": None,
        "person_source_value": OMOP.PERSON.SOURCE_VALUE,
        "race_source_value": None,
        "year_of_birth": OMOP.MEASUREMENT.YEAR_OF_BIRTH
    },
    "ProcedureOccurrence": {
        "_links": {
            "modifier_concept_id": OMOP.PROCEDURE.MODIFIER.CONCEPT_ID,
            "person_id": OMOP.PERSON.ID,
            "procedure_concept_id": OMOP.PROCEDURE.CONCEPT_ID,
            "procedure_source_concept_id": OMOP.PROCEDURE.SOURCE_CONCEPT_ID,
            "procedure_type_concept_id": OMOP.PROCEDURE.TYPE.CONCEPT_ID,
            "provider_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "procedure_occurrence_id": OMOP.PROCEDURE.ID
        },
        "modifier_source_value": None,
        "procedure_date": None,
        "procedure_datetime": OMOP.PROCEDURE.DATETIME,
        "procedure_source_value": None,
        "quantity": None
    },
    "Provider": {
        "_links": {
            "care_site_id": None,
            "gender_concept_id": None,
            "gender_source_concept_id": None,
            "specialty_concept_id": None,
            "specialty_source_concept_id": None
        },
        "_primary_key": {
            "provider_id": None
        },
        "dea": None,
        "gender_source_value": None,
        "npi": None,
        "provider_name": None,
        "provider_source_value": None,
        "specialty_source_value": None,
        "year_of_birth": None
    },
    "Relationship": {
        "_links": {
            "relationship_concept_id": None,
            "reverse_relationship_id": None
        },
        "_primary_key": {
            "relationship_id": None
        },
        "defines_ancestry": None,
        "is_hierarchical": None,
        "relationship_name": None
    },
    "SourceToConceptMap": {
        "_links": {
            "source_vocabulary_id": None,
            "target_concept_id": None,
            "target_vocabulary_id": None
        },
        "_primary_key": {
            "source_code": None,
            "valid_end_date": None
        },
        "invalid_reason": None,
        "source_code_description": None,
        "source_concept_id": None,
        "valid_start_date": None
    },
    "Speciman": {
        "_links": {
            "person_id": OMOP.PERSON.ID,
            "specimen_concept_id": OMOP.SPECIMEN.CONCEPT_ID,
            "anatomic_site_concept_id": OMOP.SPECIMEN.ANATOMIC_SITE.CONCEPT_ID,
            "disease_status_concept_id": OMOP.SPECIMEN.DISEASE_STATUS.CONCEPT_ID,
            "specimen_type_concept_id": OMOP.SPECIMEN.TYPE.CONCEPT_ID,
            "unit_concept_id": None,
        },
        "_primary_key": {
            "specimen_id": OMOP.SPECIMEN.ID
        },
        "anatomic_site_source_value": OMOP.SPECIMEN.ANATOMIC_SITE.SOURCE_VALUE,
        "disease_status_source_value": OMOP.SPECIMEN.DISEASE_STATUS.SOURCE_VALUE,
        "quantity": None,
        "specimen_date": None,
        "specimen_datetime": OMOP.SPECIMEN.DATETIME,
        "specimen_source_id": OMOP.SPECIMEN.ID,
        "specimen_source_value": OMOP.SPECIMEN.SOURCE_VALUE,
        "unit_source_value": None
    },
    "SurveyConduct": {
        "_links": {
            "assisted_concept_id": None,
            "collection_method_concept_id": None,
            "person_id": None,
            "provider_id": None,
            "respondent_type_concept_id": None,
            "response_visit_occurrence_id": None,
            "survey_concept_id": None,
            "survey_source_concept_id": None,
            "timing_concept_id": None,
            "validated_survey_concept_id": None,
            "visit_detail_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "survey_conduct_id": None
        },
        "assisted_source_value": None,
        "collection_method_source_value": None,
        "respondent_type_source_value": None,
        "survey_end_date": None,
        "survey_end_datetime": None,
        "survey_source_identifier": None,
        "survey_source_value": None,
        "survey_start_date": None,
        "survey_start_datetime": None,
        "survey_version_number": None,
        "timing_source_value": None,
        "validated_survey_source_value": None
    },
    "VisitDetail": {
        "_links": {
            "admitted_from_concept_id": None,
            "care_site_id": None,
            "discharge_to_concept_id": None,
            "person_id": None,
            "preceding_visit_detail_id": None,
            "provider_id": None,
            "visit_detail_concept_id": None,
            "visit_detail_parent_id": None,
            "visit_detail_source_concept_id": None,
            "visit_detail_type_concept_id": None,
            "visit_occurrence_id": None
        },
        "_primary_key": {
            "visit_detail_id": None
        },
        "admitted_from_source_value": None,
        "discharge_to_source_value": None,
        "visit_detail_end_date": None,
        "visit_detail_end_datetime": None,
        "visit_detail_source_value": None,
        "visit_detail_start_date": None,
        "visit_detail_start_datetime": None
    },
    "VisitOccurrence": {
        "_links": {
            "admitted_from_concept_id": None,
            "care_site_id": None,
            "discharge_to_concept_id": None,
            "person_id": None,
            "preceding_visit_occurrence_id": None,
            "provider_id": None,
            "visit_concept_id": None,
            "visit_source_concept_id": None,
            "visit_type_concept_id": None
        },
        "_primary_key": {
            "visit_occurrence_id": None
        },
        "admitted_from_source_value": None,
        "discharge_to_source_value": None,
        "visit_end_date": None,
        "visit_end_datetime": None,
        "visit_source_value": None,
        "visit_start_date": None,
        "visit_start_datetime": None
    },
    "Vocabulary": {
        "_links": {
            "vocabulary_concept_id": None
        },
        "_primary_key": {
            "vocabulary_id": None
        },
        "vocabulary_name": None,
        "vocabulary_reference": None,
        "vocabulary_version": None
    }
}
