import re

class LatexGenerator:
    def format_scientific_name(self, in_str):
        in_str = in_str.replace('\n', ' ')
        matchObj = re.match( r'\s*(\w+\.?\s+\w+)\s+(var|ssp|subsp)\.\s+(\w+)(\s+.*)?', in_str, re.I)
        if matchObj:
            num_groups = len(matchObj.groups())
            if num_groups == 4:
                final_string = matchObj.group(4)
            else:
                final_string = ''
            out_str = '{\\em ' + matchObj.group(1) + '} ' + matchObj.group(2) \
                + '. {\\em ' + matchObj.group(3) + '}' + final_string
        else:
            matchObj = re.match( r'\s*(\w+\s+\w+)(.*)', in_str, re.I)
            if matchObj:
                out_str = '{\\em ' + matchObj.group(1) + '}' + matchObj.group(2)
            else:
                matchObj = re.match( r'\s*(\w.\s+\w+)(.*)', in_str, re.I)
                if matchObj:
                    return '{\\em ' + matchObj.group(1) + '}' + matchObj.group(2)
                else:
                    out_str = in_str
        return out_str