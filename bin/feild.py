from bin.transl import transl
from libs.jsonInterface import Language

#"""
lang_name = input("Please type your programming language: ")
t = transl(lang_name, ["/testinput.cpp"])
for output in t.write_output():
    print(output)
#"""

"""
t = transl('python', ["/testinput.cpp"])
l = Language('/bin/language.config')
for lang in l.get_all():
    t.set_lang(lang)
    print()
    print(lang)
    for output in t.write_output():
        print(output)
"""
