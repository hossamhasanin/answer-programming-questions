import re

txt = "i have an answer <basic_courses>(koko) <advanced_courses> <aksdjkal>(kasdj)"

f = re.findall(r"<\w+>[\(\w+\)]*", txt)

print("koko koko  koko".split(" "))

print(f)

for i in f:
    m = re.search("\(\w+\)", i)
    if m:
        h = re.findall("\((\w+)\)", i)
        print(h)

l = {"sss": "dd", "lll": "nnn"}

for o in l:
    print(o)
