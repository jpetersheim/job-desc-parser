import os
import pandas as pd
import utils

print("Starting...")

location = "C:/Users/Josh/Stash/job-desc-parser/data/"

obj = os.scandir(location)

df_final = pd.DataFrame()

for entry in obj:
    if entry.is_file():
        temp_ext = utils.extract_ext(location + entry.name)

    if temp_ext in [".docx", ".pdf", ".doc"]:
        raw_text = utils.extract_text(location + entry.name, temp_ext)
        df_final = pd.concat([df_final, utils.pHR_tmplt_to_tbl(raw_text.body)])

df_final.to_csv(
    "C:/Users/Josh/Stash/job-desc-parser/output/data_table.csv", index=False
)

print("done")
