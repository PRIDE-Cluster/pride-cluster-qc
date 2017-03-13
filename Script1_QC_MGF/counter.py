# -*- coding: utf-8 -*-

#Script to create frequency tables. 

#Modifications
from collections import Counter
with open('modifications_ide_final.txt') as f1,open('modifications_ide_table.txt','w') as f2:
    c=Counter(x.strip() for x in f1)
    for x in c:
        f2.write("%s\t%s\n" %  ( x,str(c[x])) )   #

#Sequences
from collections import Counter
with open('sequences_ide_final.txt') as f1,open('sequences_ide_table.txt','w') as f2:
    c=Counter(x.strip() for x in f1)
    for x in c:
        f2.write("%s\t%s\n" %  ( x,str(c[x])) )   
        
#Spectrum count:
from collections import Counter
with open('spectrum_ide.txt') as f1,open('spectrum_unide.txt') as f2, open('spectrum_table.txt','w') as f3:
    lines1 = f1.read().count('\n')
    lines2 = f2.read().count('\n')
    f3.write("%s\t%s\n" %  ( lines1, lines2 ))

        
#Taxonomy ide: 
from collections import Counter
with open('taxonomy_ide.txt') as f1,open('taxonomy_ide_table.txt','w') as f2:
    c=Counter(x.strip() for x in f1)
    for x in c:
        f2.write("%s\t%s\n" %  ( x,str(c[x])) )
        
#Taxonomy unide: 
from collections import Counter
with open('taxonomy_unide.txt') as f1,open('taxonomy_unide_table.txt','w') as f2:
    c=Counter(x.strip() for x in f1)
    for x in c:
        f2.write("%s\t%s\n" %  ( x,str(c[x])) )   