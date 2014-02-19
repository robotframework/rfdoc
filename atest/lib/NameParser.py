def get_names(namestr):
    if namestr and namestr[0] == namestr[-1] == '"':
        namestr = namestr[1:-1]
    return namestr.replace(' and ', ', ').split('", "')

def get_library_name(library_name):
    return library_name.split()[0]

def get_library_version(library_name):
    return library_name.split()[-1]