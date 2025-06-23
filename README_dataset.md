# GoTriple metadata

## Description

This dataset contains metadata about all publications in GoTriple with a full-text link. 
The dataset was created on {date}, thus it contains anything ingested into GoTriple before that date.
It was created by means of the [`gotriple-data-utils`](https://github.com/odoma-ch/gotriple-data-utils), a collection of Python scripts to query the GoTriple API.

## Data packaging

Publication metadata are represented as a JSON document, with one JSON document corresponding to one publication. 
Metadata are grouped by disciplines into a JSON-lines gzipped archive. Each filename is prefixed with the discipline label as per the [GoTriple vocabulary](https://gotriple.eu/ontology/triple/disciplines#). Here below is the full list of files contained in this dataset.

[TODO: Table with discipline ID, discipline desc, filename.]

## Credits

This dataset was created by [Harshdeep Singh](https://github.com/Harshdeep1996) (Odoma) in the context of the EU-funded [GRAPHIA project](https://graphia-ssh.eu/) (grant ID: [101188018](https://cordis.europa.eu/project/id/101188018)).