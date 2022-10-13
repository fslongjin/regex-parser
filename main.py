from regex_parser import Regex
# TRUE
st = 'THISISREGEXTEST'
pattern = '([A-Z]*|[0-9]+)'

# FALSE
# st = 'THISISREGEXTEST'
st = "2A2"
pattern = '([A-Z]*[0-9]+)'

reg = Regex(pattern)
reg.compile()
print(reg.match(st))
