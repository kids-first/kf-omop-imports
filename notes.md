# OMOP CDM / FHIR

## Goals
The initial goal was to research other popular industry data models and determine whether we should adopt one of these as the Kids First data model. After working with an OMOP database and comparing that with the FHIR spec, it is clear that we cannot just use another data model as is, but rather we should borrow the good concepts, learn from the bad concepts, and discard/modify the bad parts of the Kids First model.

We explored the OMOP Common Data Model through the process of mapping and ingesting a CBTTC (Children's Brain Tumor Tissue Consortium) proteomics dataset. We tried to get a feel for the following:

- How well does the model capture the "things" we care about in Kids First (i.e. participants, specimens, files, etc.) and how those "things" relate to each other
- How well does the model accommodate longitudinal data
- How easy is it to answer questions we care about

# OMOP CDM

### Designed for research (maybe). Minimal (definitely).

"The CDM aims to provide data organized in a way optimal for analysis, rather than for the purpose of addressing the operational needs of health care providers or payers."

There is a clear focus on participants and specimens and the data that has been gathered about them.

## The two stage vocabulary

#### This representation preserves the record and also records its intent.

Example use of their mechanism:

| Exact source code/text | Source intent ID | Target "standard" ID |
|-|-|-|
|ICD 14.9|OMOP_11223344|OMOP_12345678|
|ICD 149|OMOP_11223344|OMOP_12345678|
|Extra Nostril|null|OMOP_12345678|
|Cleft Elbow|null|OMOP_87654321|

Where (for this example):
* OMOP_11223344 is defined to mean ICD10 14.9, which means (let's pretend) "extra nostril"
* OMOP_12345678 is defined to mean SNOMEDCT \<whatever1\>, which means (still pretending) "extra nostril"
* OMOP_87654321 is defined to mean SNOMEDCT \<whatever2\>, which means (definitely pretending) "cleft elbow"

They call their target "standard", but that's problematic because nobody can agree what a standard should be, so let's call it "target" or something similar instead. By accumulating terms from many sources, the OMOP vocabulary, like UMLS (or whatever), lets you best-effort match all terms to wherever they happen to exist.

* This model is intended for mixing codes and terms from official sources.
* It doesn't help fix hand-entered free text that doesn't match an ontological source string, so we'll always need curation.
* They assign additional intermediate identifiers instead of referring to the ontology.

Similar mechanism without intermediate identifiers and without standardizing on SNOMEDCT:

| Exact source text | Intended source ontology (if applicable) | Intended code within source ontology (if applicable) | Target ontology | Target ontology code | (optional) target term text |
|-|-|-|-|-|-|
|ICD 14.9|ICD10|14.9|ICD10|14.9|Extra nostril|
|ICD 149|ICD10|14.9|ICD10|14.9|Extra nostril|
|Extra nostril|null|null|ICD10|14.9|Extra nostril|
|Cleft Elbow|null|null|SNOMEDCT|12345|Cleft elbow|

If they give us a code and that code maps to other codes, then we can just use the given code and present all of the different related codes on the UI end when they're needed.

#### Good

* Preserving original, preserving intent.
* Drug vocabulary structure focused on helping you get to the active ingredients from specific brands/doses.

#### Bad

* Using the word "standard" and then pointing directly at SNOMEDCT leaves a bad taste.
* The OMOP vocabulary effort is basically the same as the UMLS but different. Why?
* Doesn't include any of the Monarch ontologies in their vocabulary.
*  **EBI-OLS** (for example) provides a much better aggregate lookup experience than OHDSI Athena and similarly links to synonyms and drug components where available.

#### Takeaway

* Forget picking the "right" ontology(ies). A two-stage storage allows you to use whatever you want and then just indicate where the code came from or even to present all of the available ones later.

## Supports Generic storage + Generic relationship

The generic OBSERVATION and FACT_RELATIONSHIP tables would allow us to immediately dump everything in, whatever we find, however we find it and then improve from there.

**OBSERVATION**  *can* be interpreted as **"A thing that happened"**. It is our basic event container.

**FACT_RELATIONSHIP**  *can* be interpreted as **"How these two things relate"**.

We don't **have** to use only these two tables, but techncially we could, and having the option to wedge any edge cases in somewhere is nice.

**Category divisions that don't need to exist get in the way of finding relationships, so avoid them.** Categorically separating Tylenol hypersensitivity, having green hair, and cancer introduces unnecessary barriers to querying for defining attributes. All three are observed deviations from the norm, and we're looking for possible genetic causes for those deviations. It doesn't matter that Tylenol hypersensitivity describes a cause rather than a manifestation.

* Was a drug administered? *That is a thing that happened.*
* Did a person die? *That is a thing that happened.*
* Was the person seen to be alive? *That is a thing that happened.*
* Was a person observed to have a particular trait? *That is a thing that happened.*
* Did a person get XRAYed? *That is a thing that happened.*
* Did a person receive a diagnosis? *That is a thing that happened.*
* Is one person someone else's father? *That is a relationship.*
* Was a diagnosis given specifically because of a particular radiology report? *That is a relationship between observations.*
* and so on...

If you review the research questions that people want to answer, most of them can be summarized as: "I want the data for people where thing happened, and thing happened, and thing happened, possibly in a particular order, possibly where some other thing did not happen."

## Model Ambiguities

They differentiate between OBSERVATION/MEASUREMENT and OBSERVATION/CONDITION_OCCURRENCE, but it's not clear why.

The OBSERVATION/CONDITION_OCCURRENCE tables are very similar, and their chosen description for CONDITION_OCCURRENCE even includes the word **"observed"** with the context as **"records suggesting the presence of a disease or medical condition"**.

Their blurb on MEASUREMENT says **"Measurements differ from Observations in that they require a standardized test or some other activity"**, but that's not a particularly significant reason. You could just as easily have a "How this observation was made" field in the OBSERVATION table.

### Small Model Relies on Agreement/Conventions

We track more things than just people, observations, and specimens. We also track study metadata, sequencing equipment metadata, and raw files. It's not clear where to put some of these. Is sequencing metadata a set of observations about a genomic file, which is itself an observation about a specimen? It certainly *could* be.

Their lack of a STUDY table makes it clear that they're defining a model for one study's worth of data. We could add basic containers for organizational entities like studies, investigators, institutions, sequencing centers, and so forth, but there is a proposal to just add trial membership as an observation: https://github.com/OHDSI/Themis/issues/37

## The OMOP CDM isn't originally for bioinformatics/genomics/imaging, but some groups have made extensions for that

See maybe:

* https://github.com/OHDSI/Radiology-CDM
* http://www.ohdsi.org/web/wiki/doku.php?id=projects:workgroups:genetics-sg

Unfortunately, ad-hoc splinter groups often break down quickly after initial interest.

## Longitudinal Modeling

All three models - OMOP, FHIR and Kids First have a decent handle on modeling "things" and "events", but none of the three models adequately model relationships between events. Both OMOP and FHIR try to, but there are unnecessary complexities that make things confusing.

#### All events are observations. All observations are events.

"I observed at time T that person P's [trait type] **cleft lip characteristic** status was True/False."

	subject: P
	type of thing: characteristic
	thing being observed: cleft lip
	observational value: True / False

"I observed at time T that person P's [procedure type] **nephrectomy surgery** status was True/False."
"I observed at time T that person P's [drug type] **drug D administration** was True/False."
"I observed at time T that sample S's [trait type] **some kind of cancer characteristic** status was True/False."
"I observed at time T that person P's [trait type] **oxygen level characteristic** status was 50.1."

#### Ideas

* An event should be modeled as an occurrence that happens at a single point in time
* Events can be implicitly related by time windows
* Events can also be explicitly related by being part of **event groups**

All events should only have have 1 timestamp field to mark the single point in time when that event occurred.
An event should never have both a start and and end timestamp. If you try to squish both the start and end time of something occurring you may lose important distinct information about the start event and the stop event of that something that happened. However, on the flip side, we still want to be able to link an end event with its corresponding start event so that we know these events are part of the same thing happening over a period of time.

We can use event groups to model multi-part processes or to model relationships (Treatment A was administered at time T0 specifically because Diagnosis A was observed at time T1).

## Additional Nit Picks That Have a Big Impact

### Missing, Unknown, or Negative Data

- How well does OMOP capture missing values in the source data?
- How well does OMOP capture other "negatives" - reported unknowns, reported not applicable, etc?  

#### Goodish - Unavailable for Missing Values

The concept `Unavailable, concept_id = 45884388` is an OK general concept that can be used for any attribute in the source data that has no available value.

concept_id | concept_name | domain_id |vocabulary_id | concept_class_id | standard_concept | concept_code | valid_start_date | valid_end_date | invalid_reason
------ | ------ | ------ |------ | ------ | ------ | ------ | ------ | ------ | ------
45884388 | Unavailable | Meas Value | LOINC | Answer | Standard | LA7287-1 | 1970-01-01 | 2014-07-31

#### Bad - Multiple concepts for unavailable

There should probably just be one set of values to represent unknown or missing data. These values should be able to apply to any concept regardless of domain, class, etc.

Some OMOP concepts have their own particular concept for `Unavailable` that can be used to report data that is does not exist in the source data. I think this makes things more confusing.

For example when mapping for gender, you could map to OMOP standard concept 8551, which is:

concept_id | concept_name | domain_id |vocabulary_id | concept_class_id | standard_concept | concept_code | valid_start_date | valid_end_date | invalid_reason
------ | ------ | ------ |------ | ------ | ------ | ------ | ------ | ------ | ------
8551 | UNKNOWN | Gender | Gender | Gender | S | M | 1970-01-01 | 2014-07-31

But which do you choose, the more general `Unavailable, concept_id = 45884388` or the gender specific one, `Unavailable, concept_id = 8551`?

#### Bad - No set of common concepts for "Negatives"

In addition to Unavailable, there should be a set of concepts for other "negatives" like: Not Applicable, Reported Unknown, Not Allowed to Report etc. We should be able to use these for any concept, regardless of which domain, concept class, or vocabulary the concept belongs to. These are important distinctions from Unavailable, and we want to capture them.

### Constraints and Integrity

Were the constraints under or over restrictive?

#### Constraints were a bit too restrictive

**Required columns that could not be filled because source data did not supply it**
- Almost all `<something>_source_concept_id` columns
-  `procedure_occurrence.modifier_concept_id`

**Required columns that we wish were not required**
- All `<something>_source_concept_id` columns
-  `procedure_occurrence.modifier_concept_id`
- The `<something>_source_concept_id` might be useful for when the data contributor already has mapped their source value to an existing ontology term, but they may not have this information.

**Columns that need to be free text instead of varchar to accommodate source data**
- All `<something>_source_value` columns
- Some source value columns had to be truncated because the value was longer than the max char length.

### Naming Conventions and Consistency (Table and Column)
Common table attributes should be named uniformly and without a table name prefix.

#### Source Value Columns
For example, I believe the column `person_source_value` is used to represent a person identifier in the source data. So then it should be called: `source_value` or `source_id`. Similarly, `specimen_source_value` should just be called `source_value` or `source_id`. Table name prefixes on these columns make it harder to automate data ingest.

#### Primary key Columns
Primary key columns should also be named uniformly and not depend on table name (i.e. person_id should be something like kf_id, omop_id, etc). There is less mental overhead in knowing that `omop_id` in every table means primary key.

#### Consistent Use  of `<something>_source_concept_id`
Why isn't the model **consistent with the use of source_concept_id**? Shouldn't every field have both a concept_id and source_concept_id?

    Example: person table has `gender_concept_id` and `gender_source_concept_id`, but
    specimen table has `anatomic_site_concept_id` but not `anatomic_site_source_concept_id`

# FHIR

### Still Needs Further Exploration
So far we've just read the FHIR spec and browsed various company/org's FHIR tooling. We need to evaluate FHIR the same way we evaluated OMOP. Spin up a FHIR database and try ingesting an example dataset like CBTTC.


### FHIR is a LOT of things - more than a data model or API specification
Employs verbosity rather than generality. (Also the documentation is 80% filler, but we can give that a pass.)

-   Used less as a standalone data model and more as a way to interchange data from existing EHR systems

-   Includes a defined information model of the medical world

-   Defines a specification for extending the model

-   Defines a specification for adding constraints to the model

	-   Specify required attributes of Resources AND how Resources relate (foreign keys).

-   Defines a very detailed specification for creating, updating, deleting, and finding FHIR entities (or Resources) via RESTful web services

-   Defines a specification for a RESTful query language - allows more advanced querying to search for FHIR Resources    
	-   Example query: Patient that is Asian or White and Female and is at least 30 years old with more than one 		DiagnosisReport
	-  Good because defining the syntax and grammar for a RESTful query language is hard and not a standardized thing


### Defines resources for more things and more details than OMOP (outside of splinter groups)

OMOP has only a basic set of *things*, whereas FHIR also covers by default:

* Imaging and other file metadata
* Sequencing data
* Study details

FHIR also allows for participants to be a species other than human.

### FHIR Has similar model ambiguities as OMOP CDM

Some of the distinctions seem unnecessary and likely exist for EHR billing reasons rather than scientific ones.
See e.g.

* the overlap between OBSERVATION and CONDITION
* the overlap between IMAGING STUDY, MEDIA, BINARY, and DOCUMENT REFERENCE

### There are a lot of orgs/companies providing FHIR services/apps … what exactly does each provide?

#### SMART on FHIR

-   Primarily geared towards helping people build apps that access existing “SMART on FHIR” backends.

-   Tough to tell what a “SMART on FHIR” backend is vs just a REST API that implements the FHIR specification

-   Aims to get people to build apps within their ecosystem and provide a “marketplace” of apps  
-   Does not seem to focus on building your own FHIR data and REST API

#### FHIRbase
-   Provides a set of tools to easily create your own database with the FHIR database model and interact with the FHIR data via a SQL  data access layer  
-   Significantly lowers the barrier to entry for standing up a FHIR database - great documentation and tutorials along with docker images to get up and running quickly
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5ODE0ODc3MzcsMTM0NTk5NTI1OSw1MT
MyMjQwMDgsLTExNjY5NTg4OTEsLTk0OTAzMDI0OSwtNTY2MDI5
NjQxLC0yMDMzMTkwMTkxLDEwOTk0Mzc4NywxNjI0OTQxNzkzLC
03MjI3MjM5MjEsLTE1MDA2NTk0NjUsLTQzNzMzMDY1MiwtMTk5
MDI0MTAxMSwxMjk1OTM5MDIxLC0xMDc2ODE0NDk5LC0xMjgzMz
EwMzg3LC00MjIyNzU5MDYsMTMyMzQyMDY4MCwxOTIzMTAwNzIw
LC03MjY1NDkzODddfQ==
-->
