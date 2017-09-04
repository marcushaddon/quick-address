import quick_address

matches = [
'{{field}}',
'{{field}}|natural',
'{{field}}|c_c'
]

case_flags = map(lambda match: quick_address.get_case_flag(match), matches)

print case_flags
