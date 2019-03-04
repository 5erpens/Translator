
from bin.transl import transl

lang_name = input("Please type your programming language: ")


t = transl(lang_name, ["/testinput.cpp"])

for output in t.write_output():
    print(output)


