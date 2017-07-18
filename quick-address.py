import click
import re

# TODO: provide options for camelCase, CamelCase, snake_case, and lower
# TODO: (set globally with flags and also flag individually to override)
# TODO: provide method for overrideing values (ie 'First' instead of 'FirstName')
# TODO: provide defaults settings and option to save templates
# TODO: provide meta template for shipping/billing sections

def case_string(string, case):
    # Default is CC
    if case == 'CC': return string
    if case == 'cc': return string.lower()

    # Split by uppercase letters
    matches = re.finditer('[A-Z][a-z]+', string)
    words = [m.group(0) for m in matches]

    if case == 'cC':
        cased_string = words[0].lower() + ''.join(words[1:])

    if case == 'C_C':
        cased_string = '_'.join(words)

    if case == 'c_c':
        words = [word.lower() for word in words]
        cased_string = '_'.join(words)

    if case == 'c-c':
        words = [word.lower() for word in words]
        cased_string = '-'.join(words)

    if case == 'natural':
        cased_string = ' '.join(words)

    return cased_string

def replace_vars(template, inline=False, casing='CC'):
    sections = [
    'Shipping',
    'Billing'
    ]

    values = [
    'FirstName',
    'LastName',
    'Address1',
    'Address2',
    'City',
    'State',
    'Zip',
    'Country'
    ]

    results = []

    if inline:
        for value in values:
            formatted_template = re.sub('\{\{shipping\}\}',
                                        case_string("Shipping" + value, casing),
                                        template)
            formatted_template = re.sub('\{\{billing\}\}',
                                        case_string("Billing" + value, casing),
                                        formatted_template)
            results.append(formatted_template)
    else:
        for section in sections:
            for value in values:
                formatted_template = re.sub('\{\{field\}\}',
                                            case_string(section + value, casing),
                                            template)
                results.append(formatted_template)

    return results

@click.command()
@click.option('--inline', default=False, help='Shipping and Billing on same line')
@click.option(
'--casing',
default='CC',
help='''
Casing for field values.
(Can also be overridden like {{field|cC}} / {{billing|c-c}})

CC=CamelCase,
cC=camelCase,
cc=lowercase
c_c=snake_case,
C_C=Snake_Case,
c-c=WHATS THIS CALLED?,
natural=Natural Case
''')
@click.option(
'--section_template',
default=False,
help='Provide additional template to wrap each shipping/billing {{section}}')
def quick_address(inline, casing, section_template):
    if section_template:
        print "Provide template to wrap each section:"
        outer_template_lines = []
        outer_line_no = 1
        inputting = True
        while inputting:
            outer_line = raw_input(str(outer_line_no) + ": ")
            if len(outer_line) == 0:
                inputting = False
            else:
                outer_template_lines.append(outer_line)
                outer_line_no += 1
        section_template_string = '\n'.join(outer_template_lines)

    print "Provide template for each section:"
    template_lines = []
    inputting = True
    line_no = 1
    while inputting:
        this_line = raw_input(str(line_no) + ": ")
        if len(this_line) == 0:
            inputting = False
        else:
            template_lines.append(this_line)
            line_no += 1

    template = '\n'.join(template_lines)
    replaced_lines = replace_vars(template, inline, casing)
    results= '\n'.join(replaced_lines)

    if section_template:
        results = re.sub('\{\{section\}\}', results, section_template_string)

    print results

if __name__ == '__main__':
    quick_address()
