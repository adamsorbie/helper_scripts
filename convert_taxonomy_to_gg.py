# Author: Adam Sorbie
# 2020-01-28
import pandas as pd


taxonomy_dict = {"Kingdom": "k__", "Phylum": "p__", "Class": "c__", "Order": "k__", "Family": "f__", "Genus": "g__", "Species": "s__" }

def read_file(filename):
    """Reads in file
    Parameters
    ----------
    filename: str
        filename of OTU table/taxonomy file"""
    # sep = None tries to infer delimiter but it may be better to write something for this just in case
    df = pd.read_csv(filename, sep=None, index_col=0, header=0, engine="python")
    df_taxa = df[["taxonomy"]]
    return df_taxa
def split_taxonomy(df, col):
    """Splits taxonomy into separate columns by ; delimiter
    Parameters
    ----------
    df: Pandas Dataframe
        Pandas dataframe containing taxonomy
    col: str
        taxonomy column"""
    df[['Kingdom','Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']] = df[col].str.split(';',expand=True)
    return df

def add_taxa_prefix(df, col, prefix):
    """Adds greengenes format prefix to each taxonomy
    Parameters
    ----------
    df: Pandas Dataframe
        Pandas dataframe containing output from split taxonomy
    col: str
        column name of taxonomic level
    prefix: str
        gg prefix to add e.g. "k__" for kingdom"""
    df[col] = prefix + df[col].astype(str)
    return df
def add_all_prefixes(df):
    """Adds all prefixes at once
    Parameters
    ----------
    df: Pandas Dataframe
        Pandas dataframe containing output from split taxonomy"""
    for key, value in taxonomy_dict.items():
        add_taxa_prefix(df, key, value)
    return df

def convert_to_gg(file, original_col, new_col, delim):
    """Converts SILVA formatted taxonomy into greengenes and output df with 
    single taxonomy column
    Parameters
    ----------
    file: OTU table/Taxonomy file
        txt or csv containing taxonomy
    original_col: str
        column name of silva-formatted taxonomy
    new_col: str
        column name to use for gg formatted taxonomy"""
    df = read_file(file)
    # split taxa column by delim 
    df_split_taxa = split_taxonomy(df, original_col)
    df_prefixes = add_all_prefixes(df_split_taxa)
    df_prefixes[new_col] = df_prefixes[df_prefixes.columns[1:]].apply(lambda x: delim.join(x.dropna().astype(str)),
    axis=1)
    df_out = df_prefixes[[new_col]]
    return df_out


# GG_taxonomy = convert_to_gg("OTUs-Table.tab", "taxonomy", "gg_taxonomy", delim=";")






