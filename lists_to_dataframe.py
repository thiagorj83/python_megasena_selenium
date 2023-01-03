import pandas as pd
import time
import re
import csv
joined_lists=pd.read_csv('C:\\Users\\thiag\\Desktop\\new_data\\csv from parallel computing\\megasena_data0.csv')

joined_lists=list(joined_lists)

for i in range(1,10):
    n_lists=pd.read_csv('C:\\Users\\thiag\\Desktop\\new_data\\csv from parallel computing\\megasena_data'+str(i)+'.csv')
    joined_lists.extend(list(n_lists))
    time.sleep(3)

print(len(joined_lists))

megasena_data=[]
for i in range(0,len(joined_lists)):
    if joined_lists[i]==' \n' or joined_lists[i]=='\n' or joined_lists[i]==' ':
        joined_lists[i]='empty'
    all_items = joined_lists[i].split(", ")
    megasena_data.append(all_items[0])
print(megasena_data)


# Busca pelos campos Unnamed
for i in range(0,len(megasena_data)):
    if re.match('[A-Za-z]*[\:][0_9]*',megasena_data[i]):
        print(megasena_data[i])

# Substituição de Unamed: xx por "no data"
for i in range(0,len(megasena_data)):
    if re.match('[A-Za-z]*[\:][\s][0-9]',megasena_data[i]):
        megasena_data[i]='No data'
print(megasena_data)

# Procurar por campos onde só existam siglas de estados v1
for i in range(0,len(megasena_data)):
    if re.match('^([A-Z]{2})([\s][\W])([A-Z]{2})*([\s]*)',megasena_data[i]):
        megasena_data[i]=megasena_data[i].split()

print(megasena_data)

for i in range(0,len(megasena_data)):
    megasena_data[i]=str(megasena_data[i])
    if re.match("(.+)\\.{1}([0-9]+)\Z",megasena_data[i]):
        megasena_data[i]=re.sub("(\\.{1}[0-9]+)\Z",'',megasena_data[i])

print(megasena_data)

with open("C:\\Users\\thiag\\Desktop\\new_data\\HEADERS_test.txt", "r") as megasena_headers:
    header = megasena_headers.readlines()
    print(header)

cols=[]
for h in header:
    cols.append(h.replace('\n',''))
print(cols)

x=[]
rows=[]
for i in range(0,len(megasena_data),21):
    for z in range(0,21): 
                x.append([megasena_data[i+z]])
    rows.append(x)
    x=[]
print(rows)

megasena_dataframe=pd.DataFrame(rows,columns=cols)
print(megasena_dataframe)

for i in range(0,len(megasena_dataframe)):
    for z in range(0,21):
        megasena_dataframe.iloc[i][z]=str(megasena_dataframe.iloc[i][z]).replace('[','').replace(']','').replace('\'','').replace('\'','')
print(megasena_dataframe)


megasena_dataframe.to_csv('C:\\Users\\thiag\\Desktop\\new_data\\megasena_dataframe.csv', sep='\t', encoding='utf-8')