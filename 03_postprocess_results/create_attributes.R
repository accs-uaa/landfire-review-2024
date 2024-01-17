main_file = 'D:/ACCS_Work/Projects/VegetationEcology/Landfire_BpS/Documents/AKVEG_TO_EVT.xlsx'
join_file = 'D:/ACCS_Work/Projects/VegetationEcology/Landfire_BpS/Documents/EVT_Types_Error_Flags.xlsx'
output_file = 'D:/ACCS_Work/Projects/VegetationEcology/Landfire_BpS/Documents/Revised_EVT_Types_20240116.csv'

library(readxl)
library(dplyr)

main_data = read_xlsx(main_file, 'new_attributes')
join_data = read_xlsx(join_file, 'original_attributes')

output_data = main_data %>%
  left_join(join_data, by = c('EVT_NEW' = 'Value')) %>%
  select(-EVT_NAME.y, review_block, block_name, Count, LFRDB) %>%
  rename(EVT_NAME = EVT_NAME.x)

write.csv(output_data, file = output_file, fileEncoding = 'UTF-8', row.names = FALSE)

