# GoTriple metadata corpus

## Description

This dataset contains metadata of all publications in GoTriple having a full-text link (as of 18.5.2025). 
The dataset was created on 18.5.2025, thus it contains anything ingested into GoTriple before that date.
It was created by means of the [`gotriple-data-utils`](https://github.com/odoma-ch/gotriple-data-utils), a collection of Python scripts to query the GoTriple API.

## Data packaging

Publication metadata are represented as a JSON document, with one JSON document corresponding to one publication. 
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