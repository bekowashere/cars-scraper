import os

dir_path = os.path.join(os.getcwd())
res = []

for path in os.listdir(dir_path):
    res.append(path)

print(res)
# merge_specifications.json
# connect_specifications.py
# varsa da önceden oluşturulan jsonı çıkar