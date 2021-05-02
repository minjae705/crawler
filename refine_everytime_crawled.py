import csv
from urllib.request import urlopen
from urllib.parse import quote_plus

results = []
cnt = 0
while cnt<1210:
    s=input()
    s=s.replace("<p class=\"large\"\">",'\n')
    s=s.replace('<br/>','\n')
    s=s.replace('</p>','\n')
    print(s)
    results.append(s)
    cnt+=1

f = open(f'refine.txt', 'w', encoding = 'utf-8', newline='')
for i in results:
    # 한줄씩 써 내려감
    f.writelines(i)
f.close()
print("success")
