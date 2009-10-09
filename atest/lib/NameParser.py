def get_names(namestr):
    if namestr and namestr[0] == namestr[-1] == '"':
        namestr = namestr[1:-1]
    return namestr.replace(' and ', ', ').split('", "')