import re

Tokens = [
    [r"\A\s+", "WHITESPACE"],
    [r"\A;" , ";"],
    [r'\A"""([\s\S]*?)"""', "BCOMMENT"],
    [r"\A\#.*$", "COMMENT"],
    [r"\A\bpregnancies\b", "DECLARATOR"],
    [r"\A\bdiagnosis\b", 'DECLARATOR'],
    [r"\A\btreatment\b", 'DECLARATOR'],
    [r"\A\bglucose\b", 'DECLARATOR'],
    [r"\A\bbloodPressure\b", 'DECLARATOR'],
    [r"\A\bskinThickness\b", 'DECLARATOR'],
    [r"\A\binsulin\b", 'DECLARATOR'],
    [r"\A\bbmi\b", 'DECLARATOR'],
    [r"\A\bdiabetesPedigreeFunction\b", 'DECLARATOR'],
    [r"\A\bage\b", 'DECLARATOR'],
    [r"\A\boutcome\b", 'DECLARATOR'],
    [r'\A=(?!=)', "DECLARATOR_OPERATOR"],
    [r"\A\d+", "NUMBER"],
    [r'\A"[^"]*"', "STRING"],
    [r"\A'[^'']*'", "STRING"]
    # [r'^\"(?:[^"\\]|\\.)*"', "STRING"],
    # [r"^\'(?:[^'\\]|\\.)*'", "STRING"],
]



class Tokenizer:
    def __init__(self, string):
        self._string = string
        self._coursor = 0
    
    def hasMoreTokens(self):
        return self._coursor < len(self._string)
    
    def getNextToken(self):
        if not self.hasMoreTokens():
            return None
        
        curr_string = self._string[self._coursor:]

        for regex, literal_type in Tokens:
            match = re.findall(regex, curr_string, flags=re.MULTILINE)
            
            if len(match) == 0:
                continue

            self._coursor += len(match[0])

            if literal_type in ["WHITESPACE", "BCOMMENT","COMMENT", "NEWLINE"]:
                if literal_type == "BCOMMENT":
                    # This is done, because it finds only the text inside the """ """,
                    # but we also need to account for len("""""") == 6.
                    self._coursor += 6

                return self.getNextToken()
            
            return {
                "type": literal_type,
                "value": match[0]
            }
