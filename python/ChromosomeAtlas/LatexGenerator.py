import re

class LatexGenerator:

    def __emphasis_first_word(self, in_str):
        if in_str == '':
            raise Exception("Expecting non-empty string")

        m = re.match("\s*(\w+)(.*)", in_str, re.I)
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
