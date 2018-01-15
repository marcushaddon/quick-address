import click
import re

# TODO: provide method for overrideing values (ie 'First' instead of 'FirstName')
# TODO: provide defaults settings and option to save templates
# TODO: fix outer template flag with inline templating even though thats
# probably useless?

t_styles = {
"handlebars": {
"open": "\{\{", "close":"\}\}"
},
"ejs": {
"open": "\<\%", "close":"\%\>"
}
}

def get_case_flag(pattern_match):
    flag_match = re.search('\|[\w|\-]+', pattern_match)
    if flag_match is not None:
        return flag_match.group(0)[1:]

    return None

def case_string(string, case):
    """ Return the specified casing of an AddressField """
    # Default is CC
    if case == 'CC': return string
    if case == 'cc': return string.lower()

    # Res of options require spliting by uppercase letters, casing and recombining
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

def replace_vars(template, inline=False, casing='CC', template_style='handlebars'):
    """ Return list of template with {{field}}s replace by
    each combination of Shipping/Billing + each address field
    """
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
            # Make our pattern
            t_open = t_styles[template_style]['open']
            t_close = t_styles[template_style]['close']
            pattern = t_open + '[^(' + t_close + ')]+' + t_close

            # Find fields that need to be replaced
            matches = re.finditer(pattern, template)
            act_matches = [m.group(0) for m in matches]
            strings_flags = map(lambda act_match: (act_match, get_case_flag(act_match)), act_matches)

            formatted_template = template
            for string_flag in strings_flags:
                # See if it's a shipping or billing field
                section = 'Billing' if string_flag[0].find('billing') > -1 else 'Shipping'
                local_case = string_flag[1] if string_flag[1] is not None else casing
                field = case_string(section + value, local_case)
                formatted_template = formatted_template.replace(string_flag[0], field)

            results.append(formatted_template)

    else:
        pattern = (
                t_styles[template_style]['open'] +
                '[^(' + t_styles[template_style]['close'] + ')]+' +
                t_styles[template_style]['close'])
        # pattern = '\{\{[^(\}\})]+\}\}'
        for section in sections:
            for value in values:
                # We should do this earlier and reuse the results
                matches = re.finditer(pattern, template)
                act_matches = [m.group(0) for m in matches]
                strings_flags = map(lambda act_match: (act_match, get_case_flag(act_match)), act_matches)
                formatted_template = template
                for string_flag in strings_flags:
                    local_case = string_flag[1] if string_flag[1] is not None else casing
                    field = case_string(section + value, local_case)
                    formatted_template = formatted_template.replace(string_flag[0], field)
                results.append(formatted_template)

    return results

@click.command()
@click.option('--inline/--serial',
              default=False,
              help='Shipping and Billing on same line')
@click.option(
'--template-style',
default='handlebars',
help='''
Templating style. Default is {{value}},
but if you are using this to generate HTML for a mustache/angular
project, you can use ejs style templating like <%value%>
''')
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
c-c=spinal-case/kebab-case/train-case/lisp-case,
natural=Natural Case
''')
@click.option(
'--section-template',
default=False,
help='Provide additional template to wrap each shipping/billing {{section}}')
def quick_address(inline, casing, section_template, template_style):
    """ Take input from user and return rendered form/code """

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
    replaced_lines = replace_vars(template, inline, casing, template_style)
    results= '\n'.join(replaced_lines)

    if section_template:
        results = re.sub('\{\{section\}\}', results, section_template_string)

    print results

if __name__ == '__main__':
    quick_address()
