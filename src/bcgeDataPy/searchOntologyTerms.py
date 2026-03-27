import tempfile
from pathlib import Path
from helpers import downloadZenFile
import pandas as pd

def searchNames(term, table):
    table = table[table['Preferred Label'].str.contains(term, case=False) | 
                  table['Synonyms'].str.contains(term, case=False)] 
    table.rename(columns={'Preferred Label': 'Name', "code": 'Code'}, inplace=True)
    return table

def searchDefinitions(term, table):
    table = table[table['Definitions'].str.contains(term, case=False)]
    table.rename(columns={'Preferred Label': 'Name', "code": 'Code'}, inplace=True)
    return table 

def searchURI(term, table):
    table = table[table['URI'] == term]
    table.rename(columns={'Preferred Label': 'Name', "code": 'Code'}, inplace=True)
    return table

def searchCode(term, table):
    table = table[table['code'] == term]
    table.rename(columns={'Preferred Label': 'Name', "code": 'Code'}, inplace=True)
    return table 



def searchOntologyTerms(term:str, term_type:str = "Name"):
    acceptable_terms = ["Name", "Definition", "URI", "Code"]
    if term_type not in acceptable_terms:
        raise ValueError("Invalid term type. Valid options are Name, Definition, URI, and Code.")
    
    ontology_identifiers = ["10.5281/zenodo.17488901", 
                      "NCIT_definitions_filtered.tsv.gz"]
    
    temp = tempfile.gettempdir()
    dirPath = Path(f"{temp}/{ontology_identifiers[1]}")
    if not dirPath.exists():
        downloadZenFile(ontology_identifiers[0], temp)
    
    termTable = pd.read_csv(f"{temp}/{ontology_identifiers[1]}", sep="\t")

    if term_type == "Name":
        return searchNames(term, termTable) 
    elif term_type == "Definition":
        return searchDefinitions(term, termTable)
    elif term_type == "URI":
        return searchURI(term, termTable) 
    else:
        return searchCode(term, termTable)
