import os
import json
import gzip
import logging
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path


def merge_discipline_jsons_to_jsonl(root_dir: str) -> None:
    """
    Merge JSON files from language-year directories into a single gzipped discipline JSONLines file.
    Reference: https://jsonlines.org

    Args:
        root_dir: str, the root directory to merge the JSON files from
    """
    root = Path(root_dir)
    disciplines = [d for d in root.iterdir() if d.is_dir()]
    
    with ProcessPoolExecutor() as executor:
        list(executor.map(process_discipline, disciplines))


def process_discipline(discipline_dir: str) -> None:
    """Helper function to process a single discipline directory"""
    discipline = discipline_dir.name
    output_file = discipline_dir.parent / f"{discipline}_merged.jsonl.gz"
    logging.info(f"Processing discipline: {discipline}")
    
    try:
        # write results directly to gzipped output
        with gzip.open(output_file, "wt", encoding="utf-8") as outfile:
            json_files = []
            for lang_dir in sorted(p for p in discipline_dir.iterdir() if p.is_dir()):
                for year_dir in sorted(p for p in lang_dir.iterdir() if p.is_dir() and p.name.isdigit()):
                    # get all the json files in the language-year hierarchy
                    for json_path in lang_dir.glob(f"{year_dir.name}/**/*.json"):
                        json_files.append(json_path)
                    
                    logging.info(f"Found {len(json_files)} JSON files for {lang_dir.name} {year_dir.name}")
            
            # process the json files in batches
            batch_size = 100
            for i in range(0, len(json_files), batch_size):
                batch = json_files[i:i+batch_size]
                logging.info(f"Processing batch {i//batch_size + 1}/{(len(json_files) + batch_size - 1)//batch_size}")
                
                # Read and process each file
                for file_path in batch:
                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            data = json.load(infile)
                            for item in data:
                                outfile.write(json.dumps(item) + "\n")
                    except Exception as e:
                        logging.error(f"Error processing file {file_path}: {e}")
        
        logging.info(f"Successfully created gzipped JSONLines file for {discipline}: {output_file}")
    
    except Exception as e:
        logging.error(f"Error processing discipline {discipline}: {e}")
