
### Mapping to unknown or not available
- There are no common concepts to represent things like Not Reported, Not available, Reported Unknown, etc.
- Each OMOP concept (some entity attribute) may or may not have its own corresponding
concept instance in the standard concepts table to represent unknown. For example to map to unknown for gender, you need to map to OMOP concept_id=8507, which is:

concept_id | concept_name | domain_id |vocabulary_id | concept_class_id | standard_concept | concept_code | valid_start_date | valid_end_date | invalid_reason
------ | ------ | ------ |------ | ------ | ------ | ------ | ------ | ------ | ------
8551 | UNKNOWN | Gender | Gender | Gender | S | M | 1970-01-01 | 2014-07-31

- This makes is a lot harder to fill in default values since now you have to look up the correct value by domain, concept_name, etc.


### Problematic Required Attributes

- **some\_domain\_source\_concept\_id**

    - I understand why you might require the mapping of a field (i.e. gender) to a standard concept's concept_id
    but why also *require* source_concept_id? Why assume this is provided in the source data and make it required?

    Example: Person table requires both gender_concept_id and gender_source_concept_id

    - Why isn't the model consistent with source_concept_id?
    Shouldn't every field have both a concept_id and source_concept_id?

    Example: person table has gender_concept_id and gender_source_concept_id, but
    specimen table has anatomic_site_concept_id but not anatomic_site_source_concept_id



- **year\_of\_birth**
