
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string
from enum import Enum
import time

class CapStyle(Enum):
    AS_IS     = 0
    LOWER     = 1
    CAP_WORDS = 2

class LatexGenerator:

    latex_file = None
    current_genus = ''
    num_species_in_fam = 0
    num_genus_in_fam = 0

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID and range of spreadsheets.     

    SPREADSHEET_DICT = {
        'Acanthaceae': '1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw', 
        'Aceraceae'  : '1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw',
        'Agavaceae'  : '1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk',
        'Aizoiceae'  : '1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718',  
        'Alangiaceae': '1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE',
        'Alismataceae': '1Vq-Z6vmNsLbQzu3ISfae3vmG3xMPg3HcAeH7dZsSA_8',
        'Amaranthaceae': '1UpAvdWhzjti04YIXxa5_FWbbfCQC2Z3hVcryn-VA9xQ',
        'Amaryllidaceae': '1tbM4IdBSmJRT2NN0AThbW5WNW0eVYHJWOFL0TvI5iYQ',
        'Anacardiaceae': '1zCHts6_bkNaD7P-m3MDcGAEzLC9Df_CuvYxzi4amYN0',
        'Annonaceae': '1bN4I6az_ISWVTPD3qEu6Xxm6m07dLhNonnWgTuiaKko',
        'Apiaceae': '1oI_jKwBDmhcRRuQey3YNAEDDKgQbGY6-qStlGN_WkcI',
        'Apocynaceae': '1PHe5lXT6eR6KkMnb0iAXo1_HjQJD8k2yiRashA3uMX8',
        'Aponogetonaceae': '1-UZdVUrah1ZgOXHyUKz3iBvKCgPRVzalI2NxHYlbGdM',
        'Aquifoliaceae': '1TkEFy28X1iCL0fbb4JuvNeFdUjyeG4wGhcXDfHj8J5Q',
        'Aracaceae': '1JwrLcL5oJQQJFPxXY-y-rNOrqrLic1Zb7iGRslLeVf4',
        'Araceae': '1bwrFv_iPJ89UGx115ZoRSqjGRY_m1_p1PifbHRiuPtA',
        'Araliaceae': '18eVtHUVzH9_X-uBAgCUoDVOeLlEHOmjJdYNzxZEvIUQ',
        'Aristrolochiaceae': '1eWGC74p0g-hw9ctUqxYaJExlsUUlS9w_TdMYG7aPfR4',
        'Asclepiadaceae': '1It_JAnjSrSl6qDXckqy67JldjgzqXndA7JUZu-h3Rc0',
        'Asteraceae': '1R26HJFoGIvVyQDebvN0T_lUZLxP07YHQtl-yt1cinJI',
        'Balsaminaceae': '1swLGYE7r6xcO_2RBXC8Bk7-urWk4CL9c5CmAwlrKpZE',
        'Basellaceae': '1B-TLV6aKrp3eyqSvdHuG6z-YoHjvMI1JrC-aRji76ao',
        'Begoniaceae': '1v-X3D708YPf5mcwaNMhQ6GOazG2UjWKJfZsUSic2omQ',
        'Berberidaceae':'1WwCvMDnWxNF58cgKR-plJmF_fgnxidTC_XSmBb4UFfA',
        'Betulaceae':'12dpTJwd0ymeb2ssCFB9g1IzkiHTdhZZ-wMtX0rgmYI0',
        'Bignoniaceae':'1zzZ7XG4Alxwf5RX6mNPT3K6gTGM5xegF2xhidmsn6Bo',
        'Bombacaceae':'1ICUvGYuTzUEwFGfzVpqX2l6dZ22GRePWMLEIIIuU4nI',
        'Boraginaceae':'1ICLaRsV4LUvwSUQLSwbrJQSgrDiGa8-20aFujs9UogI',
        'Brassicaceae':'1TKt9hILyc7Iapfp9T_jQo0whcPbFffQySTqrN1qspm0',
        'Bromelliaceae':'1_Vu4eUkaknzNT8C4d7zVKJCVE_qdljOPP8gkdHoaZH4',
        'Burseraceae':'1zVgTT8fOYECUhUN0tqmKgIgUv5-_C95CYQBWkAfCgtU',
        'Callistricaceae':'11vu_Od9dwv9yDFPs4TI4NuUhn2iZu86Not1KpbMD0Ck',
        'Campanulaceae':'1_bS45r9lEXeN9GkMT8s0C6byOjoM9VNiausNUUlKqsg',
        'Cannabaceae':'1EUf_M38fr2Fa6J20OqS1jQqtHHgcUnLm7AvgJQW3ghA',
        'Caprifoliaceae':'1rrH8RnMypK7Rgyg0kcrSOiu0kojkBfycfFNHDn32J7g',
        'Caricaceae':'1jfuUUy74rPzWm4Zl9E7DzFghSF2PzraMw0vMPDrM1js',
        }

    RANGE_NAME = 'Sheet1!A2:L'
    
    DONE_CODE_INDEX = 0
    SPECIES_INDEX = 1
    NEPAL_NAMES_INDEX = 2
    NEPAL_NAMES_BIB_INDEX = 3
    ENGLISH_NAMES_INDEX = 4
    ENGLISH_NAMES_BIB_INDEX = 5
    USE_CODE_INDEX = 6
    USE_CODE_BIB_INDEX = 7
    CHR_NUM_INDEX = 8
    CITATION_INDEX = 9
    NEPAL_DIST_INDEX = 10
    NEPAL_DIST_BIB_INDEX = 11
    
    NEPAL_SEARCH_WORDS = ['Godawari', 'Patan', 'Kuleswor']

    def normalize_row(self, row):
        TOTAL_COLS = 12
        for i in range(len(row), TOTAL_COLS):
            row.append('')
        return row

    def output_latex_string(self, str):
        strout = str
        strout = strout.replace('&', '\\&')
        strout = strout.replace('%', '\\%')
        strout = strout.replace(',', ', ')
        self.latex_file.write(strout)

    def is_heading_row(self, row):
        return (row[self.SPECIES_INDEX] != '')

    def output_latex_string_noreplace(self, str):
        self.latex_file.write(str)

    def output_citations(self, cite_string):
        cite_string = ''.join(cite_string.split())
        out_str = '\\citet{' + cite_string + '}\n\n'
        self.output_latex_string_noreplace(out_str)

    def output_citations_p(self, cite_string):
        cite_string = ''.join(cite_string.split())
        out_str = '\\citep{' + cite_string + '}\n'
        self.output_latex_string_noreplace(out_str)

    def format_scientific_name_list(self, in_str):
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        str_lst = in_str.split(',')
        for i in range(0, len(str_lst)):
            str_lst[i] = self.format_scientific_name(str_lst[i])
        return ','.join(str_lst)
                
    def __emphasis_first_word(self, in_str):
        if in_str == '':
            raise Exception("Expecting non-empty string")

        m = re.match(r"\s*(\w+)(.*)", in_str, re.I)
        if m:
            # print(in_str)
            # print(m.groups())
            return '{\\em ' + m.group(1) + '}' +  self.__format_sc_post_str(m.group(2))
        else:
            return in_str

    def __format_var_sep(self, sep_str, split_str):
        out_str = split_str[0]
        for i in range(1, len(split_str)):
            out_str += sep_str + ' ' + self.__emphasis_first_word (split_str[i]) 
        return out_str

    def __format_sc_post_str(self, in_str):
        if in_str == '':
            return in_str
        # see if we can match subsp.
        split_str = in_str.split('subsp.')
        if len(split_str) > 1: 
            return self.__format_var_sep('subsp.', split_str)
        # see if we can match ssp.
        split_str = in_str.split('ssp.')
        if len(split_str) > 1: 
            return self.__format_var_sep('ssp.', split_str)
        # see if we can match var.
        split_str = in_str.split('var.')
        if len(split_str) > 1: 
            return self.__format_var_sep('var.', split_str)
        
        return in_str

    def get_genus(self, in_str):
        print(f'get_genus({in_str})')
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        return in_str.partition(' ')[0]

    def format_scientific_name(self, in_str):
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        print(f'format_scientific_name({in_str})')
        m = re.match(r'\s*(\w+\.?\s+[-\w]+)(.*)', in_str, re.I) # match first two words
        if m:
            out_str = '{\\em ' + m.group(1) + '}' + self.__format_sc_post_str(m.group(2))
            return out_str
        else:
            raise Exception(f'Scientific name {in_str} does not seem to be in correct format')

    def generate_latex_row_chr_num(self, row):
        # output chromosome numbers and citation as a separate row
        chr_num = row[self.CHR_NUM_INDEX].strip(',. ')
        citations = row[self.CITATION_INDEX].strip(',. ')
        self.output_latex_string('\\begin{hangparas}{0.5cm}{1}\\noindent \\textbf{$' + chr_num + '$} ')
        self.output_citations_p(citations)
        self.output_latex_string('\\end{hangparas}\n')

    def generate_latex_subheading(
            self, row, str_heading, content, bib_index, capstyle):
        if (capstyle == CapStyle.CAP_WORDS):
            content = string.capwords(content)
        elif (capstyle == CapStyle.LOWER):
            content = content.lower()
        self.output_latex_string(
                    '\\begin{hangparas}{0.5cm}{1}\n'
                    f'\\noindent \\textbf{{\small {str_heading}}}: ' \
                    + '\\begin{otherlanguage}{hindi} ' \
                    + '{' \
                    + content + '} \\end{otherlanguage}\n')
        bib = row[bib_index].strip(',. ')
        self.output_latex_string('{\\small ')
        self.output_citations_p(bib + '\n\n')
        self.output_latex_string('}\\end{hangparas}\n\n\\vspace{2mm}')
    
    def generate_latex_row(self, row):
        # print(f'generate_latex_row({row})')
        if self.is_heading_row(row):
            self.output_latex_string('\\vspace{5mm}')
            self.output_latex_string(
                '\\section{' + self.format_scientific_name(row[self.SPECIES_INDEX]) + '}\n')
            if row[self.NEPAL_NAMES_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Common Name(s) in use in Nepal",
                    row[self.NEPAL_NAMES_INDEX], self.NEPAL_NAMES_BIB_INDEX,
                    CapStyle.LOWER)
                
            if row[self.ENGLISH_NAMES_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Common Name(s) in English",
                    row[self.ENGLISH_NAMES_INDEX], self.ENGLISH_NAMES_BIB_INDEX,
                    CapStyle.CAP_WORDS)

            if row[self.USE_CODE_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Uses",
                    row[self.USE_CODE_INDEX], self.USE_CODE_BIB_INDEX,
                    CapStyle.AS_IS)
            
            if row[self.NEPAL_DIST_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Distribution in Nepal",
                    self.add_msl(row[self.NEPAL_DIST_INDEX]), 
                    self.NEPAL_DIST_BIB_INDEX,
                    CapStyle.AS_IS)
            
            self.output_latex_string('\\vspace{4mm}\n\n') 
            
        # output chromosome numbers and citation as a separate row
        self.generate_latex_row_chr_num(row)
        
    def add_msl(self, in_str):
       return re.sub(r'([0-9]+)', r'\1 msl', in_str)

    def generate_latex(self, family_name):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret_563563514748-486lji2ouvg2svb016j2gbe65135ks9r.apps.googleusercontent.com.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        sheet = service.spreadsheets()
        sheet_id = self.SPREADSHEET_DICT[family_name]
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=self.RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            self.latex_file = open('output/' + family_name + '.table.tex', 'w', encoding="utf-8")
            for i in range(0, len(values)):
                row = values[i]
                if (len(row) == 0): # skip if empty row
                    continue
                row = self.normalize_row(row)
                if (self.is_heading_row(row)):
                    self.num_species_in_fam += 1
                    row_genus = self.get_genus(row[self.SPECIES_INDEX])
                    if row_genus != self.current_genus:
                        self.num_genus_in_fam += 1
                        self.current_genus = row_genus
                    done_code = row[self.DONE_CODE_INDEX]
                self.generate_latex_row(row)
            self.latex_file.close()
    
    def move_dist_data(self, row, move_str):
        if not (row[self.NEPAL_DIST_INDEX].isspace()):
            row[self.NEPAL_DIST_INDEX] += ', '
        row[self.NEPAL_DIST_INDEX] += move_str
        row[self.NEPAL_DIST_INDEX] = row[self.NEPAL_DIST_INDEX].strip(',. ')

    def generate_latex_all_families(self):
        all_families_file = open('output/families.tex', 'w')
        for family in sorted(self.SPREADSHEET_DICT):
            self.current_genus = ''
            self.num_genus_in_fam = 0
            self.num_species_in_fam = 0
            self.generate_latex(family)
            all_families_file.write('\\include{' + family + '}\n')
            family_tex_file = open('output/' + family + '.tex', 'w')
            family_tex_file.write('\\chapter{' + family + '}\n\n' +
                '\\input{' + family + '.count.tex}\n\n' +   
                '\\input{' + family + '.table.tex}\n\n' + 
                '\\vspace{5mm}'
                                '\\bibliographystyle{plainnat}\n' + 
                                '\\bibliography{Bibliography}\n')
            family_tex_file.close()
            family_count_file = open('output/' + family + '.count.tex', 'w')
    
            if self.num_genus_in_fam == 1:
                genus_article = 'is a single'
                genus_word = 'genus'
                
            else:
                genus_article = f'are {self.num_genus_in_fam}'
                genus_word = 'genera'

            if self.num_species_in_fam == 1:
                fam_article = 'a single'
            else:
                fam_article = f'{self.num_species_in_fam}'

            family_count_file.write(
                'There %s %s and %s species reported with chromosome counts  '
                'of plants found in Nepal in this family.\\vspace{-5mm}'%
                    (genus_article, genus_word, fam_article)
            )
            family_count_file.close()
            time.sleep(0.1)
        all_families_file.close()
            

if __name__ == '__main__':
    lgen = LatexGenerator()
    lgen.generate_latex_all_families()
