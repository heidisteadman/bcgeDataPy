import tempfile
from pathlib import Path
import pandas as pd
from ZenodoObj import ZenObj

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



def searchOntologyTerms(term:str, term_type:str = "Name") -> pd.DataFrame:
    """
    Function that searches for ontology terms.

    Accepts a string to search by and which ontology field to search 
    ontology terms associated with that string. This could
    be the name of the term itself, the term's definition,
    the unique identifier (code) associated with that term,
    or its URL. The function returns a tibble with information
    about the matching ontology term(s).

    Args:
        term (str): The term to search for
        term_type (str): Ontology field to search: Name, URI, Code, or
                         Definition. When Name (default) is provided, it also searches
                         based on synonyms.
    
    Returns:
        pd.DataFrame: A data frame with a row for each matching ontology term.
        
    Examples:
        >>> searchOntologyTerms("Progesterone Receptor Status")
        A pandas dataframe object
    
    """

    acceptable_terms = ["Name", "Definition", "URI", "Code"]
    if term_type not in acceptable_terms:
        raise ValueError("Invalid term type. Valid options are Name, Definition, URI, and Code.")
    
    ontology_identifiers = ["10.5281/zenodo.17488901", 
                      "NCIT_definitions_filtered.tsv.gz"]
    
    zenFile = ZenObj(ontology_identifiers[0])
    temp = tempfile.gettempdir()
    dirPath = Path(f"{temp}/definitionsFile")
    filePath = dirPath / ontology_identifiers[1]
    if not filePath.exists():
        download_link = zenFile.parse_json()
        zenFile.download_file(download_link, dirPath)
    
    termTable = pd.read_csv(filePath, sep="\t")

    if term_type == "Name":
        return searchNames(term, termTable) 
    elif term_type == "Definition":
        return searchDefinitions(term, termTable)
    elif term_type == "URI":
        return searchURI(term, termTable) 
    else:
        return searchCode(term, termTable)