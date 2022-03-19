import io
import os

# import nltk
# import spacy
import pandas as pd
from docx2python import docx2python

# from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords


def extract_text_from_pdf(pdf_path):
    """
    Helper function to extract the plain text from .pdf files
    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    """
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    with open(pdf_path, "rb") as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(
                resource_manager, fake_file_handle, codec="utf-8", laparams=LAParams()
            )
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def extract_text_from_doc(doc_path):
    """
    Helper function to extract plain text from .doc or .docx files
    :param doc_path: path to .doc or .docx file to be extracted
    :return: string of extracted text
    """
    temp = docx2python(doc_path, html=True)
    # temp = docx2txt.process(doc_path)
    # text = [line.replace("\t", " ") for line in temp.split("\n") if line]
    # return " ".join(text)
    return temp


def extract_text(file_path, extension):
    """
    Wrapper function to detect the file extension and call text extraction function
    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    """
    text = ""
    if extension == ".pdf":
        for page in extract_text_from_pdf(file_path):
            text += " " + page
    elif extension == ".docx" or extension == ".doc":
        text = extract_text_from_doc(file_path)
    else:
        print("File extension not compatible: " + file_path)
        text = ""
    return text


def extract_ext(file_path):
    if not isinstance(file_path, io.BytesIO):
        ext = os.path.splitext(file_path)[1].split(".")[1]
    else:
        ext = file_path.name.split(".")[1]
    return "." + ext


def pHR_tmplt_to_tbl(text_list):
    # print(text_list)
    client = "".join(text_list[1][0][1])
    role = "".join(text_list[1][0][3])
    dept = "".join(text_list[1][1][1])
    role_type = "".join(text_list[1][1][3])

    l_jd = []
    l_h4 = []
    l_h5 = []
    ct_segment = 0

    for x in text_list[2][0][0]:
        if "h4" in x:
            l_h4.append(x)
        elif "h5" in x:
            l_h5.append(x)

    for indx, x in enumerate(text_list[2][0][0]):
        temp_r = []

        if any(x in i for i in l_h4):
            ct_segment += 10
            ct_section = 0
            ct_item = 0
            c_h4 = x
            if not any(text_list[2][0][0][indx + 1] in i for i in l_h5):
                c_h5 = "NONE"

        elif any(x in i for i in l_h5):
            ct_item = 0
            ct_section += 10
            c_h5 = x

        else:
            ct_item += 10
            temp_r = [c_h4, c_h5, x, ct_segment, ct_section, ct_item]
            l_jd.append(temp_r)

    temp_df = pd.DataFrame(
        l_jd,
        columns=[
            "segment",
            "section",
            "item",
            "segment_sequence",
            "section_sequence",
            "item_sequence",
        ],
    )
    temp_df.insert(loc=0, column="client", value=client)
    temp_df.insert(loc=1, column="department", value=dept)
    temp_df.insert(loc=2, column="role", value=role)
    temp_df.insert(loc=3, column="role_type", value=role_type)

    temp_df["segment"] = temp_df["segment"].str.replace("<h4>", "")
    temp_df["segment"] = temp_df["segment"].str.replace("</h4>", "")
    temp_df["section"] = temp_df["section"].str.replace("<h5>", "")
    temp_df["section"] = temp_df["section"].str.replace("</h5>", "")
    return temp_df
