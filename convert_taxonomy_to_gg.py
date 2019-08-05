#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd


# In[109]:


taxonomy_dict = {"Kingdom": "k__", "Phylum": "p__", "Class": "c__", "Order": "k__", "Family": "f__", "Genus": "g__", "Species": "s__" }

def read_file(filename):
     """Reads in file
    Parameters
    ----------
    filename: str
        filename of OTU table/taxonomy file"""
    df = pd.read_csv(filename, sep="\t", index_col=0, header=0)
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

def convert_to_gg(df, original_col, new_col, read_files=False, filename=None):
    """Converts SILVA formatted taxonomy into greengenes and output df with 
    single taxonomy column
    Parameters
    ----------
    df: Pandas Dataframe
        Pandas dataframe containing taxonomy
    original_col: str
        column name of silva-formatted taxonomy
    new_col: str
        column name to use for gg formatted taxonomy
    read_files: bool (optional)
        whether to read in file or use existing df
    filename: str (optional)
        filename if read_files is used"""
    if read_files and filename:
            df = read_file(filename)
    df_split_taxa = split_taxonomy(df, original_col)
    df_prefixes = add_all_prefixes(df_split_taxa)
    df_prefixes[new_col] = df_prefixes[df_prefixes.columns[1:]].apply(lambda x: '; '.join(x.dropna().astype(str)),
    axis=1)
    df_out = df_prefixes[[new_col]]
    return df_out


# In[111]:


GG_taxonomy = convert_to_gg(data, "taxonomy", "gg_taxonomy", read_files=True, filename="OTUs-Table.tab")


# In[ ]:





# In[ ]:




