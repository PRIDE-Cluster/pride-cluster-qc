from itertools import groupby
import re

data = (k.rstrip().split("=Cluster=") for k in open("test1.txt", 'r'))
final = list(k for k,_ in groupby(list(data)))

with open("file_repeated_removed.txt", 'a') as f:
    for k in final:
        if k == ['','']:
            f.write("=Cluster=\n")
        elif k == ['']:
            f.write("\n\n")
        else:
            f.write("{}\n".join(k)+"\n")
        


with open("file_repeated_removed.txt", 'r') as f_in, open("file_repeated_removed_final.txt", 'w') as f_out:
    for line in f_in:
        file = re.sub(';+',';',line)
        f_out.write(file)
