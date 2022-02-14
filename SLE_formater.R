library(readxl)
library(dplyr)
library(stringr)
library(magrittr)

loviste_lgo1 <- list.files(pattern= "loviste_lgo1") %>% read_xlsx
