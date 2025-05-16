# gotriple-data-utils

## Description

Code for extracting publication metadata (and optionally fulltexts) from the [GoTriple API](https://api.gotriple.eu/). As of today, GoTriple contains more than 19M publications from the Social Sciences and Humanities; GoTriple holds their metadata, while the fulltext needs to be fetched from the data providers.

## Installation

- To install the requirements to run this code:
```bash
pip install -r requirements.txt
```
or if you are using [`uv`](https://github.com/astral-sh/uv):
```bash
uv pip install -r requirements.txt
```

## Configuration

There are two bits of configuration to this script:
1. `.env` file: see [`.env.example`](./.env.example) for an example configuration and for explanation of each parameter.
2. `const.py` file: this specifies the disciplines to be included in the export as well as the languages that should be considered. 

## Usage & output

To execute the export script, simply run `python main.py`; the script checks for the presence of intermediary files, and if necessary builds them and extracts metadata from GoTriple fro the disciplines specified in `const.py`.

Each publication is described by the corresponding JSON document. Here below is an example of such documents. For the full explanation of the data semantics, please refer to this document: [TRIPLE Deliverable: D6.6 API's Development -RP3](https://doi.org/10.5281/zenodo.7371832).

<details>
    <summary>Show JSON example</summary>

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
</details>

Exported data are packaged as `.gzip` compressed JSON-lines files, where each file corresponds to one discipline. Thus, the names of output files will correspond to the identifiers of discipline selected in `const.py`.

Additionally, there are some helper functions in `helper.py` to query a document by its ID on GoTriple or to check if the PDF is valid, or to read a PDF which has been extracted.

## Credits

The code contained in this repository was developed by [Harshdeep Singh](https://github.com/Harshdeep1996) (Odoma) building upon code written by [Alessandro Bertozzi](https://github.com/AlessandroBertozzi) (Net7). This work was carried out in the context of the EU-funded [GRAPHIA project](https://graphia-ssh.eu/) (grant ID: [101188018](https://cordis.europa.eu/project/id/101188018)).