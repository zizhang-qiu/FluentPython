import locale
import pyuca
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
# locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
coll = pyuca.Collator()
print(sorted(fruits))
print(sorted(fruits, key=coll.sort_key))
# print(sorted(fruits, key=locale.strxfrm))