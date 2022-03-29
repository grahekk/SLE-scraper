library(readxl)
library(Rcpp)
library(tidyverse)
library(janitor)
library("r2excel")
install.packages("devtools")
devtools::install_github("kassambara/r2excel")
install.packages("writexl")
library(writexl)
install.packages("writexl")
#list.files(pattern = "loviste_lgo1")
#loviste_lgo1_fajlovi <- list.files(pattern = "loviste_lgo1")
#lgo1 <- map(loviste_lgo1_fajlovi, read_xlsx)

x <- read_xlsx("vugrovec_loviste_lgo1.xlsx")
x <- x %>% row_to_names(row_number = 1)
x <- x[-c(1,2),-1]
x$Ha <- x$Ha %>% as.numeric()

x %>% 
  filter(`Naziv površine`!= "Sveukupno lovište  prema vlasništvu" &
           `Naziv površine`!= "Sveukupne lovne površine" & 
           `Naziv površine`!= "Površine opisane granicom lovišta" &
         `Zemljovlasničko razmjerje` != '∑') %>% 
  group_by(`Naziv površine`,`Vrsta površine`) %>% summarise(Ha = sum(Ha)) -> y

x %>% 
  filter(`Zemljovlasničko razmjerje` != '∑')%>% 
  group_by(`Naziv površine`) %>% 
  drop_na %>% 
  summarise(Ha = sum(Ha)) %>% 
  slice(1) %>% 
  rename("Vrsta površine" = `Naziv površine`, "Ha"= "Ha") -> y

x %>% 
  filter(`Zemljovlasničko razmjerje` != '∑')%>%
  group_by(`Vrsta površine`) %>% 
  drop_na() %>% 
  summarise(Ha = sum(Ha)) %>% 
  arrange(`Vrsta površine`) %>% 
  slice(c(5,11)) %>%
  adorn_totals("row", name = "Ukupno") %>% 
  add_row(y) -> y

x %>% 
  filter(`Vrsta površine` == "Šumsko" |
        `Vrsta površine` == "Poljoprivredno" | 
        `Vrsta površine` == "Tekućice" | 
        `Vrsta površine` == "Stajaćice") %>% 
  filter(`Zemljovlasničko razmjerje` != '∑')%>% 
  group_by(`Vrsta površine`) %>% 
  drop_na() %>% 
  summarise(Ha = sum(Ha)) %>% 
  adorn_totals("row", name = "Ukupno") %>% 
  add_row(y) -> y

#finally
y %>% slice(c(3,6,7)) %>% summarise(`Vrsta površine`="Sveukupno", Ha = sum(Ha)) %>% add_row(y,.) -> y
y %>% mutate(`% Površine lovišta` = round((Ha/unlist(y[8,2])),4)*100) -> z

#excel export
write_xlsx(z, "loviste_lgo1.xlsx")
