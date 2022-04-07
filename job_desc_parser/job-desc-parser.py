import os
import pandas as pd
import utils

print("Starting...")

location = "C:/Users/Josh/Stash/job-desc-parser/data/"
location2 = "C:/Users/Josh/Stash/job-desc-parser/data/New Folder/Quality Coordinator job description.docx"

obj = os.scandir(location)

df_final = pd.DataFrame()

for entry in obj:
    if entry.is_file():
        temp_ext = utils.extract_ext(location + entry.name)
    else:
        temp_ext = ""

    if temp_ext in [".docx", ".doc"]:
        raw_text = utils.extract_text(location + entry.name, temp_ext)
        df_final = pd.concat([df_final, utils.pHR_tmplt_to_tbl(raw_text.body)])

df_final.to_csv(
    "C:/Users/Josh/Stash/job-desc-parser/output/data_table.csv", index=False
)

print("done")
print(
    "saved output to {0}".format(
        "C:/Users/Josh/Stash/job-desc-parser/output/data_table.csv"
    )
)

print(utils.docx_to_info(location2))
