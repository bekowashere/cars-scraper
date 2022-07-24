import os

dir_path = os.path.join(os.getcwd())
res = []

for path in os.listdir(dir_path):
    res.append(path)

print(res)
# connect_types.py
# merge_types.py
# varsa da önceden oluşturulan jsonı çıkar
