
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class LatexGenerator:

    latex_file = None

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # The ID and range of spreadsheets.
    SPREADSHEET_DICT = {'Acanthaceae': '1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw', 
                        'Aceraceae'  : '1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw',
                        'Agavaceae'  : '1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk',
                        'Alangiaceae': '1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE',
                        'Aizoiceae'  : '1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718'  }
    RANGE_NAME = 'Sheet1!A2:I'

    def normalize_row(self, row):
        TOTAL_COLS = 9
        for i in range(len(row), TOTAL_COLS):
            row.append('')
        return row

    def output_latex_string(self, str):
        strout = str
        strout = strout.replace('&', '\\&')
        strout = strout.replace('%', '\\%')
        strout = strout.replace(',', ', ')
        self.latex_file.write(strout)

    def output_latex_string_noreplace(self, str):
        self.latex_file.write(str)

    def output_citations(self, cite_string):
        cite_string = ''.join(cite_string.split())
        out_str = '\\citet{' + cite_string + '}\n\n'
        self.output_latex_string_noreplace(out_str)

    def format_scientific_name_list(self, in_str):
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

    def format_scientific_name(self, in_str):
        in_str = in_str.replace('\n', ' ')
        m = re.match(r'\s*(\w+\.?\s+\w+)(.*)', in_str, re.I) # match first two words
        if m:
            out_str = '{\\em ' + m.group(1) + '}' + self.__format_sc_post_str(m.group(2))
            return out_str
        else:
            raise Exception('Scientific name does not seem to be in correct format')

    def generate_latex_row_chr_num(self, row):
        # output chromosome numbers and citation as a separate row
        self.output_latex_string('\\noindent \\textbf{$' + row[4] + '$}: ')
        self.output_citations(row[5] + '\n\n')

    def generate_latex_row(self, row, isfirst):
        if (len(row) == 0): # skip if empty row
            return
        row = self.normalize_row(row)
        if (row[0] != ''):
            self.output_latex_string(
                '\\section{' + self.format_scientific_name(row[0]) + '}\n')
            if row[3] != '':
                self.output_latex_string(
                    '\\noindent \\textbf{Synonyms}: ' + 
                                    self.format_scientific_name_list(row[3]) + '\n\n')
            if row[1] != '':
                self.output_latex_string(
                    '\\noindent \\textbf{Common name(s) in use in Nepal}: \\begin{hindi} ' \
                    + row[1] + ' \\end{hindi}\n\n')
            if row[2] != '':
                self.output_latex_string(
                    '\\noindent \\textbf{Common name(s) in English language}: ' \
                    + row[2].title() + '\n\n')
            if row[7] != '':
                self.output_latex_string(
                    '\\noindent \\textbf{Uses}: ' + row[7] + '\n\n')
            if row[8] != '':
                self.output_latex_string(
                    '\\noindent \\textbf{Distribution/Locality (msl)}: ' \
                    + row[8] + '\n\n\\vspace{1em}\n\n')

        # output chromosome numbers and citation as a separate row
        self.generate_latex_row_chr_num(row)

    def generate_latex(self, family_name):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('output/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('output/credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SPREADSHEET_DICT[family_name],
                                    range=self.RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            self.latex_file = open('output/' + family_name + '.table.tex', 'w', encoding="utf-8")
            for i in range(0, len(values)):
                self.generate_latex_row(values[i], i==0)
            self.latex_file.close()
    
    def generate_latex_all_families(self):
        all_families_file = open('output/families.tex', 'w')
        for family in self.SPREADSHEET_DICT.keys():
            self.generate_latex(family)
            all_families_file.write('\\include{' + family + '}\n')
            family_tex_file = open('output/' + family + '.tex', 'w')
            family_tex_file.write('\\chapter{' + family + '}\n\n' +
                '\\input{' + family + '.table.tex}\n\n' + 
                                '\\bibliographystyle{plainnat}\n' + 
                                '\\bibliography{' + family + '}\n')
            family_tex_file.close()
        all_families_file.close()
            

if __name__ == '__main__':
    lgen = LatexGenerator()
    lgen.generate_latex_all_families()