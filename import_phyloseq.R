#' Author Adam Sorbie
#' Date: 2019-08-01
library(tidyverse)
library(phyloseq)
library(zoo)

# replaces name but needs to append unkown first

#while(length(ind <- which(df$a == "")) > 0){
 # df$a[ind] <- df$a[ind -1]
#}

# can you look at na.locf function and basically make a version which adds unknown also ? 
# needs to append unknown!
append_nas <- function(taxa_split) {
  taxa_nas <- taxa_split %>% mutate_all(na_if,"")
  #taxa_out <- data.frame(t(apply(taxa_nas, 1, na.locf)))
  return(taxa_nas)
}

split_taxonomy <- function(otu) {
  # select taxa column and split taxonomy column into separate columns using ; delimiter
   taxonomy_phylo <- select(otu, "taxonomy") %>%
    separate("taxonomy", c("Kingdom", "Phylum", "Class", "Order", "Family", "Genus"), sep = ";")
   taxonomy_phylo_out <- append_nas(taxonomy_phylo)
  return(taxonomy_phylo_out)
}

read_tab_delim <- function(df) {
  # read all tab delimited files using these params
  df_out <- read.table(df, row.names = 1, header = 1, sep="\t", comment.char = "", check.names = F )
  return(df_out)
}

load_phylo <- function(otu, taxa, mapping) {
  # convert to phyloseq and return list
  phylo_otu <- otu_table(otu, taxa_are_rows = T)

  phylo_tax <- tax_table(as.matrix(taxa))

  phylo_map <- sample_data(mapping) # should re-write this to return phyloseq obj using merge_phyloseq

  return(merge_phyloseq(phylo_otu, phylo_tax, phylo_map))
}

prep_4_phyloseq <- function(otu, mapping){
  # read files
  otu_taxa <- read_tab_delim(otu)
  metadata <- read_tab_delim(mapping)
  # convert otu into matrix and drop taxonomy col
  count_matrix <- as.matrix(subset(otu_taxa, select=-taxonomy))
  # split taxonomy
  taxonomy_phylo <- split_taxonomy(otu_taxa)
  # make sure taxa table row names match otu
  rownames(taxonomy_phylo) <- rownames(otu_taxa)
  # use load phylo function to convert all files to phyloseq objs
  out <- load_phylo(count_matrix, taxonomy_phylo, metadata)

  return(out)
}
