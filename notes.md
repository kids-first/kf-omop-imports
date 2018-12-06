
### Schema Description
Some of the column descriptions on the OMOP CDM wiki don't provide enough detail. Its tough to tell what should go in some columns.

### Column Length Too Short
Some source_value columns are fixed width strings (i.e. anatomic_site_source_value is a 50 char length string) and as a result the source data has to be truncated. Any source data cols should probably just be text columns.

### Mapping to unknown or not available
- There are no common concepts to represent things like Not Reported, Not available, Reported Unknown, etc.
- Each OMOP concept (an attribute like `gender` of an entity like a `person`) may or may not have its own corresponding concept in the standard concepts table to represent an unknown. For example to map to unknown for gender, you need to map to OMOP standard concept 8507, which is:

concept_id | concept_name | domain_id |vocabulary_id | concept_class_id | standard_concept | concept_code | valid_start_date | valid_end_date | invalid_reason
------ | ------ | ------ |------ | ------ | ------ | ------ | ------ | ------ | ------
8551 | UNKNOWN | Gender | Gender | Gender | S | M | 1970-01-01 | 2014-07-31

- This makes is a lot harder to fill in default values since now you have to look up the correct value by domain, concept class, concept_name, etc.


### Problematic Required Attributes

- Why *require* 2 standard concept fields?

    - I understand why you might want to require the mapping of an attribute (i.e. gender) to a standard concept, but why also *require* source_concept_id? Why assume that this is provided in the source data and make it required?
    - The source_concept_id might be useful for when the data contributor already has mapped their source value to an existing ontology term, but if they don't have this information then they are forced to provide something for source_concept_id.


Field|Required|Type|Description
:---------------------------|:--------|:------------|:-----------------------------------------------
person_id|Yes|integer|A unique identifier for each person.|
gender_concept_id|Yes|integer|A foreign key that refers to an identifier in the CONCEPT table for the unique gender of the person.|
gender_source_concept_id|Yes|Integer|A foreign key to the gender concept that refers to the code used in the source.|


- Why isn't the model **consistent with the use of source_concept_id**?
Shouldn't every field have both a concept_id and source_concept_id?

    Example: person table has `gender_concept_id` and `gender_source_concept_id`, but
    specimen table has `anatomic_site_concept_id` but not `anatomic_site_source_concept_id`


### Naming of Common Attributes

- Common table attributes should be named uniformly and without a table name prefix. For example, the I believe the column `person_source_value` is used to represent a person identifier in the source data. So then it should be called
 `source_value` or `source_id`. Similarly, `specimen_source_value` should just be called `source_value` or `source_id`. Table name prefixes on these columns make it harder to automate data ingest.

- Primary key columns should also be named uniformly and not depend on table name (i.e. person_id should be something like kf_id, omop_id, etc). There is less mental overhead in knowing that `id` in every table means primary key.

### Longitudinal Aspect
**OMOP can support absolute (identifiable) or relative (deidentified) time**
- Temporal attributes in OMOP are things like day of birth, year of birth, etc instead of relative values like days since birthdate at time of diagnosis.
- Since Kids First currently doesn't have identifiable data, I will use time 0 or epoch as the person's birthdate.
Given values representing age in days since birthdate, we can compute all datetime fields by adding the days delta to epoch datetime.

**Event representation is a little confusing/complex**
- I'm confused by the way events are represented in OMOP
    - Why do event type tables such as `condition_occurrence` have both a `start_datetime` and `start_date` and `end_date` and `end_datetime`?
    - I was expecting event tables to have only 1 timestamp type field that records the point in time
    when this event occurred. There should probably be a different way to identify aggregate or continuous time events (composed of a start event and stop event).

- There seem to be multiple event tables (`condition_occurrence`, `visit_occurrence`, `observation`, etc)
    - How does one query for all events for a particular person within a time period? Since there is no
    generic event table, we'd have to query all known event type tables for the person's primary key
    - You could put everything into the Observation event table since it is the catch all event table for events that can't be mapped to one of the other more specific event types


### Search and Mapping terms to standard concepts
- One of the most tedious parts of data ingestion is the harmonization component where we must map terms in the source data to standard concepts. I want a search engine that allows me to search for terms via full text search and filter by facets. It would also be nice to customize the ranking of search results.

    - For example if I'm searching for the term `Craniopharyngioma` for `condition_status` that is a part of my `condition_occurrence` table, then I want the results with domain equal to `Condition` or synonyms of Condition to be prioritized higher. Maybe I also want to filter for standard concepts rather than non-standard concepts.

- Not sure how Athena does implements concept search - it seems like it is just using ILIKE
- By default Athena returns results in ascending order via the concept ID.

- Perhaps I'm missing something but I think Athena attempts to accomplish what the EBI (European Bioinformatics Institute)'s Ontology Lookup Service already accomplishes fairly well. https://www.ebi.ac.uk/ols/index. OLS seems to use full text search and therefore the results are ranked with some relevancy. Additionally, OLS's web app provides a pretty nice user experience. It groups results by ontology, and provides a tree or graph viewer to see the term within the ontology hierarchy.

- There are multiple standard concept matches for a given term. How do you know which one to pick?
    - `Craniopharyngioma` matches to two standard concepts, one with a domain of `Observation` and one with a domain of `Clinical Finding`


### Other Random Thoughts
- With a detailed, feature rich dataset like cbttc, it is hard to capture
the desired amount of source data in the OMOP model and/or the Kids First model.
It either takes so long to figure out how to map the source data into the available fields on the model, OR we simply cannot map the source data to the available fields and must leave it out.

- Perhaps there should be a more flexible model or data store in Kids First that prioritizes capturing as much of the source data as possible, and searchability/explorability of the data (full text search on documents)

- In the flexible model make less things required and do less validation. Have a second model that contains harmonized, vetted data. Right now the Kids First data service seems to represent more of the harmonized data model.

- Another approach could be to stick with one model but allow people to help us define the model in real-time, as they are working on ingesting their data.

    - Allow a notes column in every table. Put stuff there that we can't
    map to our model but want to capture from source data. Allow full text search
    on the notes column so that this data isn't lost and is still searchable for end user researchers

    - And/or maybe also allow custom properties for each table -
    a user supplied key value list stored in a JSON column. This could be useful with a graphql endpoint.

    - We should observe over time what properties people are adding that
    the model doesn't support.
