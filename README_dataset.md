# GoTriple metadata corpus

## Description

This dataset contains metadata of all publications in GoTriple having a full-text link (as of 18.5.2025). 
The dataset was created on 18.5.2025, thus it contains anything ingested into GoTriple before that date.
It was created by means of the [`gotriple-data-utils`](https://github.com/odoma-ch/gotriple-data-utils), a collection of Python scripts to query the GoTriple API.

## Data format & packaging

Publication metadata are represented as a JSON document, with one JSON document corresponding to one publication. Here below is an example of such documents. For the full explanation of the data semantics, please refer to this document: [TRIPLE Deliverable: D6.6 API's Development -RP3](https://doi.org/10.5281/zenodo.7371832).

```json
{
    "@id": "/documents/ftunivlausanne:oai:serval.unil.ch:BIB_76F5A7C85EB7",
    "@type": "Document",
    "id": "ftunivlausanne:oai:serval.unil.ch:BIB_76F5A7C85EB7",
    "abstract": [],
    "additional_type": [
        "typ_article"
    ],
    "cluster_children_count": null,
    "cluster_id": [],
    "conditions_of_access": [
        "acr_closed-access"
    ],
    "contributor": [],
    "date_published": "2024-07-11",
    "date_facets": "2024-07-11",
    "datestamp": "2025-02-28T22:42:35Z",
    "doi": [
        "10.1111/asap.12410"
    ],
    "full_text": null,
    "headline": [
        {
            "@type": "CommonTranslatedLabel",
            "@id": "_:1488",
            "lang": "en",
            "original_lang": "",
            "text": "Rethinking climate change vulnerabilities after COVID\u201019: Recommendations for social science\u2010based interventions drawn from research on Conspiracy Theories and Diversity Science",
            "detected_lang": "true",
            "translated": "false"
        }
    ],
    "identifier": [],
    "in_language": [
        "en"
    ],
    "is_cluster": false,
    "is_duplicate": false,
    "keywords": [],
    "discarded_keywords": [],
    "discarded_authors": [],
    "knows_about": [],
    "license": [
        "undefined"
    ],
    "main_entity_of_page": [
        "https://serval.unil.ch/notice/serval:BIB_76F5A7C85EB7"
    ],
    "mentions": [
        "Analyses of Social Issues and Public Policy"
    ],
    "original_conditions_of_access": [
        "0"
    ],
    "original_document_types": [
        "121"
    ],
    "original_languages": [
        "eng"
    ],
    "original_license": [],
    "producer": [],
    "provider": [
        "base"
    ],
    "publisher": [],
    "spatial_coverage": [],
    "temporal_coverage": [],
    "topic": [
        {
            "@type": "Topic",
            "@id": "_:1482",
            "id": "socio",
            "confidence": 0.16331824660301208
        },
        {
            "@type": "Topic",
            "@id": "_:1489",
            "id": "hist",
            "confidence": 0.09965535998344421
        }
    ],
    "url": [
        "https://serval.unil.ch/resource/serval:BIB_76F5A7C85EB7.P001/REF.pdf"
    ],
    "author": [
        {
            "agg": "aurelien_graton_10xqB113zF40fwp6fFsuN__SEP__aurelien graton__SEP__aurelien_graton__SEP__graton_aurelien",
            "fullname": "Graton, Aur\u00e9lien",
            "id": "aurelien_graton_10xqB113zF40fwp6fFsuN"
        },
        {
            "agg": "oriane_sarrasin_1jZ7_P5wE12HHpXoeeUc9__SEP__oriane sarrasin__SEP__oriane_sarrasin__SEP__sarrasin_oriane",
            "fullname": "Sarrasin, Oriane",
            "id": "oriane_sarrasin_1jZ7_P5wE12HHpXoeeUc9"
        },
        {
            "agg": "olivier_klein_MbVqC2a5twxvXK4gkKJYU__SEP__olivier klein__SEP__olivier_klein__SEP__klein_olivier",
            "fullname": "Klein, Olivier",
            "id": "olivier_klein_MbVqC2a5twxvXK4gkKJYU"
        },
        {
            "agg": "jonathon_p_schuldt_ZrwE1yqEfQQNLscz1OjlK__SEP__jonathon p. schuldt__SEP__jonathon_p_schuldt__SEP__jonathon_schuldt_p__SEP__schuldt_jonathon_p__SEP__schuldt_p_jonathon__SEP__p_schuldt_jonathon__SEP__p_jonathon_schuldt",
            "fullname": "Schuldt, Jonathon P.",
            "id": "jonathon_p_schuldt_ZrwE1yqEfQQNLscz1OjlK"
        }
    ]
}
```




Metadata are grouped by disciplines into a JSON-lines gzipped archive. Each filename is prefixed with the discipline label as per the [GoTriple vocabulary](https://gotriple.eu/ontology/triple/disciplines#). Here below is the full list of files contained in this dataset.

| GoTriple discipline ID  | Discipline | Filename |
| ------------- | ------------- |-----------|
| `anthro-bio`  | Biological Anthropology  |`anthro-bio_merged.jsonl.gz`|
| `anthro-se`  | Social Anthropology and Ethnology  | `anthro-se_merged.jsonl.gz` | 
|`archeo`|Archaeology and Prehistory| `archeo_merged.jsonl.gz`|
|`archi`|Architecture and Space Management|`archi_merged.jsonl.gz`|
|`art`|Art and Art History|`art_merged.jsonl.gz`|
|`class`|Classical Studies|`class_merged.jsonl.gz`|
|`demo`|Demography|`demo_merged.jsonl.gz`|
|`droit`|Law|`droit_merged.jsonl.gz`|
|`eco`|Economies and Finances|`eco_merged.jsonl.gz`|
|`edu`|Education|`edu_merged.jsonl.gz`|
|`envir`|Environmental studies|`envir_merged.jsonl.gz`|
|`genre`|Gender Studies|`genre_merged.jsonl.gz`|
|`geo`|Geography|`geo_merged.jsonl.gz`|
|`hisphilso`|History, Philosophy and Sociology of Sciences|`hisphilso_merged.jsonl.gz`|
|`hist`|History|`hist_merged.jsonl.gz`|
|`info`|Communication Sciences|`info_merged.jsonl.gz`|
|`lang`|Linguistics|`lang_merged.jsonl.gz`|
|`litt`|Literature|`litt_merged.jsonl.gz`|
|`manag`|Management|`manag_merged.jsonl.gz`|
|`museo`|Cultural Heritage and Museology|`museo_merged.jsonl.gz`|
|`musiq`|Musicology and Performing Arts|`musiq_merged.jsonl.gz`|
|`phil`|Philosophy|`phil_merged.jsonl.gz`|
|`psy`|Psychology|`psy_merged.jsonl.gz`|
|`relig`|Religions|`relig_merged.jsonl.gz`|
|`scipo`|Political Science|`scipo_merged.jsonl.gz`|
|`socio`|Sociology|`socio_merged.jsonl.gz`|
|`stat`|Methods and Statistics|`stat_merged.jsonl.gz`|

## Credits

This dataset was created by [Harshdeep Singh](https://github.com/Harshdeep1996) (Odoma) in the context of the EU-funded [GRAPHIA project](https://graphia-ssh.eu/) (grant ID: [101188018](https://cordis.europa.eu/project/id/101188018)).