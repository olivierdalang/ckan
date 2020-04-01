"""
Tool to quickly replace "groups" or "organisation" to some other string using i18n files.

For the "en" locale, it will only keep strings that require overrides.

Usage :

1. create/update the i18n files for the required locales :

$> python setup.py init_catalog --locale en

2. (optional) git stage modifications, so you'll better see next step's result

3. adapt the REPLACES dict below according to your needs

4. run this script

5. compile the locale
$> python setup.py compile_catalog --locale en
$> python setup.py compile_catalog --locale fr

"""

import os
import re
import babel.messages.pofile
import io

REPLACES = {
    'en': {
        'group': 'project',
        'Group': 'Project',
        'groups': 'projects',
        'Groups': 'Projects',
    },
    'fr': {
        'groupe': 'projet',
        'Groupe': 'Projet',
        'groupes': 'projets',
        'Groupes': 'Projets',
    }
}

I18N_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ckan', 'i18n')

for locale, replace_dict in REPLACES.items():

    path = os.path.join(I18N_PATH, locale, 'LC_MESSAGES', 'ckan.po')
    input_locale = open(path)

    if locale != 'en':
        # if locale is existing, we replace strings in mgstr sections
        # we can't use babel parsing as it messes with file format and makes diff unreadable
        output = []

        msgstr_section = False
        for line in input_locale.readlines():
            if line.startswith("msgstr "):
                msgstr_section = True
            elif line.startswith('#'):
                msgstr_section = False

            if msgstr_section:
                # we only do the replace in the msgstr sections
                for before, after in replace_dict.items():
                    pattern = r'(?<!\{)\b'+before+r'\b(?![\w\s]*[\}])'
                    line = re.sub(pattern, after, line)

            output.append(line)

        output_locale = open(path, 'w')
        output_locale.writelines(output)

    else:
        # if locale is english (empty) we use babel to parse the file and write it

        catalog = babel.messages.pofile.read_po(input_locale)

        for entry in list(catalog):

            new_string = entry.id

            found = False
            for before, after in replace_dict.items():

                # FIXME : add support for tuples (for plurals)
                if isinstance(entry.id, tuple):
                    continue

                # we don't want to replace if in brackets
                pattern = r'(?<!\{)\b'+before+r'\b(?![\w\s]*[\}])'
                if re.search(pattern, new_string):
                    found = True
                    new_string = re.sub(pattern, after, new_string)

            if found:
                entry.string = new_string
            else:
                # for the default en locale, we only keep messages that are modified
                catalog.delete(entry.id)

        output_locale = open(path, 'wb')
        # FIXME : this doesn't respect the output format exactly because of newlines, making changes difficult to spot
        babel.messages.pofile.write_po(output_locale, catalog, width=80)

