# convert name list to bib type (TODO: support middle names)
txt_out = ''
name_list = txt.split(', ')
for i, full_name in enumerate(name_list):
  first, last = full_name.split(' ')
  txt_out += last + ', ' + first
  if i < len(name_list)-1:
    txt_out += ' and '
print(txt_out)