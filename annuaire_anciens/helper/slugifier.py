# coding=utf-8
"""
Module pour transformer transformer des strings en slugs.
Les caractères valides sont [a-z0-9-@]. Pour obtenir un slug, on prend une string, on la passe en lowercase, et on
remplace tout caractère non valide par un dash -
"""
import re
import unicodedata

def slugify(string):
    """
    Transforme une string en slug = replace tout caractère non alphanumérique par un dash (-)
    @param string: la string à slugger
    @return string: la string slugged
    """
    if string is None:
        return None
    string = string.lower().strip()
    if string == '':
        return None
    string = string.encode('utf-8','ignore').decode('utf-8', 'ignore')
    slug = unicodedata.normalize('NFKD', string)
    slug = slug.encode('ascii','ignore')
    slug = re.sub(r'[^a-z0-9-@]+', '-', slug) 
    return slug

    
    
def clean_normal_search(raw_input):
    """
    Methode pour extraire tous les inputs de type normal (= sans guillemets), et les retourner slugged, dans une liste
    @param raw_input: un input str quelconque
    @return: une liste de toutes string non contenues entre guillemets, slugged
    """
    result = []
    pattern_exact = r'(\'[^\']*\')|(\"[^\']*\")'
    if raw_input is None or raw_input == '' or raw_input == ' ':
        return result
    else:
        # virer tout ce qui est entre guillements
        raw_input = re.sub(pattern_exact, '',raw_input)
        
        for e in raw_input.strip().split():
                result.append(slugify(e))
            
    return result
    
    
def clean_exact_search(raw_input):
    """
    Methode pour extraire tous les inputs de type exact (= entre guillemets), et les retourner slugged, dans une liste
    @param raw_input: un input str quelconque
    @return: une liste de toutes string contenues entre guillemets, slugged
    """
    result = []
    pattern_exact = r'\'[^\']*\''
    pattern_exact2 = r'"[^"]*"'

    if raw_input is None or raw_input == '' or raw_input == ' ':
        return result
    else:
        # ne prendre que ce qui est entre guillemets
    
        for e in re.findall(pattern_exact, raw_input):
            result.append(slugify(e.strip('\'')))
         
        for e in re.findall(pattern_exact2, raw_input):
            result.append(slugify(e.strip('"')))
            
    return result
    
    
def is_valid_integer(input):
    """
    Methode pour verifier qu'un input est bien un entier, que ce soit un int, une str ou un unicode

    @param input: an input
    @return: boolean, true if integer or string cast-able to int, false if not
    """
    result = False
    pattern = r'^[0-9]+$'
    if input is not None:
        if type(input) is int:
            result = True
        elif (type(input) is str or type(input) is unicode) and re.match(pattern, input.strip()):
            result = True
    
    return result