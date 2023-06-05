import re


def check_special_character(string):
    if re.search('[@_!#$%^&*()<>?/\|}{~:]',string):
        return True
    else:
        return False


def vallidate_password(string):
    mes = []
    has_spl = True
    has_upper = True
    has_lower = True
    has_digit = True
    has_eight_char = True
    spl = re.search('[@_!#$%^&*()<>?/\|}{~:]',string)
    upper = re.search('[A-Z]',string)
    lower = re.search('[a-z]',string)
    digit = re.search('[0-9]',string)

    if len(string) < 8:
        has_eight_char = False
        mes.append('Password must contain atleast 8 characters.')
    if not spl:
        has_spl = False
        mes.append('Password must contain special characters.')
    if not upper:
        has_upper = False
        mes.append('Password must contain uppercase.')
    if not lower:
        has_lower = False
        mes.append('Password must contain lowercase.')

    if not digit:
        has_digit = False
        mes.append('Password must contain digit')
    
    if not (has_digit and has_lower and has_spl and has_upper and has_eight_char):
        return [True, mes]
    else:
        return [False,mes]
    
    
print(vallidate_password('ajeetA@123')[0])