# gotriple-data-utils

Repository for extracting GoTriple data (metadata and PDF)

- To install the requirements for the code: `pip install -r requirements.txt` or if you are using `uv`: add the former command as suffix.
- To format the code before pushing into the repository, run the following command: `black .`
- The code for the following project has been run on Runpod. Install the `runpodctl` command for transferring the data to and fro from Runpod.
- To run the code in the current way: `python main.py` - this checks if there are some intermediary files and if not builds them and extracts metadata from GoTriple fro the selected disciplines which are currently selected in `const.py`.
- There are some helper functions in `helper.py` to query a document by its ID on GoTriple or check if the PDF is valid, or read a PDF which has been extracted.