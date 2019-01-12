import re

class LatexGenerator:
    def parse_scientific_name(self, in_str):
        in_str = in_str.replace('\n', ' ')
        matchObj = re.match( r'\s*(\w+\s+\w+)\s+var\.\s+(\w+)(\s+.*)?', in_str, re.I)
        if matchObj:
            out_str = '{\\em ' + matchObj.group(1) + '} var. {\\em ' \
                    + matchObj.group(2) + '}' + matchObj.group(3)
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