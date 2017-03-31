
"""This program takes different information from .MGF files in order to generate different outputs that will be used by the R Script.
IMPORTANT INFORMATION. In the release of 2014, we didn't used any filter previusly, because of that we'll not have two folders (Identify and
unidentify files). For futures releases (Ex. 2017 and 2018, ), remove the # from PATH_RELEASE_UNID and remove the line: PATH_RELEASE1_UNIDE = None

Remember to change the PATH with the new release in future QCs and uncomment the function in main() in order to compare futures releases with filters (Ex. 2017 and 2018)"""


import glob
import os
import re
from collections import Counter


def file_checker():
    """The PATH of these function must be changed in each release"""

    PATH_RELEASE1_IDEN = os.getcwd()+'/archive_all_2014-10/'
    PATH_RELEASE1_UNIDE = None
    #PATH_RELEASE1_UNIDE = os.getcwd()+'/archive_all_2014-10/'

    PATH_RELEASE2_IDEN = os.getcwd()+'/archive_all_2016-10/archive_identified_2016-10/'
    PATH_RELEASE2_UNIDE = os.getcwd() + '/archive_all_2016-10/archive_unidentified_2016-10/'


    #From here don't change anything.
    #This global function finds the .mgf files in paths
    list_of_files_release1_ide = glob.glob(PATH_RELEASE1_IDEN+'*.mgf')
    list_of_files_release1_unide = None #REMOVE THIS PART AND UNCOMMENT NEXT LINE IN NEXT RELEASES.

    #list_of_files_release1_unid = glob.glob(PATH_RELEASE1_UNID'+*.mgf')

    list_of_files_release2_ide = glob.glob(PATH_RELEASE2_IDEN+'*.mgf')
    list_of_files_release2_unide = glob.glob(PATH_RELEASE2_UNIDE+'*.mgf')


    #Check if exist cache folder. If not will make it. 
    #RELEASE 1    
    if not os.path.exists(PATH_RELEASE1_IDEN+'cache'):
        os.makedirs(PATH_RELEASE1_IDEN+'cache')

    # if not os.path.exists(PATH_RELEASE1_UNIDE'+cache'):
    #     os.makedirs(PATH_RELEASE1_UNIDE'+cache')

    #RELEASE2
    if not os.path.exists(PATH_RELEASE2_IDEN+'cache'):
        os.makedirs(PATH_RELEASE2_IDEN+'cache')

    if not os.path.exists(PATH_RELEASE2_UNIDE+'cache'):
        os.makedirs(PATH_RELEASE2_UNIDE+'cache')
    

    return PATH_RELEASE1_IDEN, \
           PATH_RELEASE2_IDEN, \
           PATH_RELEASE2_UNIDE, \
           list_of_files_release1_ide, \
           list_of_files_release2_ide, \
           list_of_files_release2_unide



def read_files(list_of_files, path):

    "This function creates a list in order to classificate different releases between identify and unidentify. This also create outputs with different information that will be used in the R script"
    results = {True:[], False:[]}

    for fileName in list_of_files:
        results = {True: [], False: []}
        with open(fileName) as fp:
            register = {}
            identified = False
            for line in fp:
                line = line.rstrip()
                if (line.find('TITLE') != -1 or line.find('PEPMASS') != -1 or line.find('CHARGE') != -1 or line.find('SEQ') != -1 or line.find('USER03') != -1 or line.find('TAXONOMY') != -1):
                    if(line.find('TITLE=id')!=-1):
                        parts = line.split(';')
                        elements = parts[0].split('=')
                        spectrum = parts[2].split('=')
                        composition = {}
                        composition['id'] = elements[2]
                        composition['file'] = parts[1]
                        composition['spectrum'] = spectrum[1]

                        register[elements[0]] = composition
                    else:
                        elements = line.split('=')
                        register[elements[0]] = elements[1]
                    if(line.find('SEQ') != -1):
                        identified = True
                elif (line.find('END IONS') != -1):
                    results[identified].append(register)
                    identified = False
                    register = {}
        fp.close()

        for result in results:
            if result:
                if len(results[True]) != 0:
                    with open(os.path.join(path + 'ID_identify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['id'] + "\n")
                    output.close()

                    with open(os.path.join(path + 'spectrum_identify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['spectrum'] + "\n")
                    output.close()

                    with open(os.path.join(path + 'taxonomy_identify.txt'), 'a') as output:
                        for register in results[result]:
                            if 'TAXONOMY' in register:
                                output.write(register['TAXONOMY'] + "\n")
                            else:
                                 continue
                    output.close()

                    if (result):
                        with open(os.path.join(path + 'SEQ.txt'), 'a') as output:
                            for register in results[result]:
                                output.write(register['SEQ'] + "\n")
                        output.close()

                        with open(os.path.join(path + 'modifications.txt'), 'a') as output:
                            for register in results[result]:
                                if bool(re.match('MS:', register["USER03"])):
                                    with open(path + 'MS_files.txt', 'a') as MS_file:
                                        MS_file.write(register['USER03'] + "\n")
                                    MS_file.close()
                                line1 = re.sub("MS:" + "\d+", "", register['USER03'])
                                line2 = line1.replace(";", ",").replace("\n", ",")
                                new_string = re.sub(',+', ',', line2)
                                new_string2 = new_string.replace(",", "\n")
                                new_string3 = re.sub('\d+\-', '', new_string2)

                                if not new_string3.strip():
                                    continue
                                if new_string3:
                                    output.write(new_string3 + "\n")
                        output.close()


            else:
                if len(results[False]) != 0:
                    with open(os.path.join(path + 'ID_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['id'] + "\n")
                    output.close()

                    with open(os.path.join(path + 'spectrum_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['spectrum'] + "\n")
                    output.close()


                    with open(os.path.join(path + 'taxonomy_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            if 'TAXONOMY' in register:
                                output.write(register['TAXONOMY'] + "\n")
                            else:
                                continue
                    output.close()

                    # if (result):
                    #     with open(os.path.join(path + 'SEQ.txt'), 'a') as output:
                    #         for register in results[result]:
                    #             output.write(register['SEQ'] + "\n")
                    #     output.close()
                    #
                    #     with open(os.path.join(path + 'modifications.txt'), 'a') as output:
                    #         for register in results[result]:
                    #             output.write(register['USER03'] + "\n")
                    #     output.close()

    # for result in results:
    #     if result:
    #         print('identified')
    #     else:
    #         print('DESidentified')
    #     for register in results[result]:
    #         print(" > ID: "+register['TITLE']['id'])
    #         print(" > Spectrum: "+register['TITLE']['spectrum'])
    #         print(" > XML: "+register['TITLE']['file'])
    #         if(result):
    #             print(" > SEQ: "+register['SEQ'])
    #             print(" > USER:"+register['USER03'])
    #             print(" > TAXONOMY:"+register['TAXONOMY'])
    #         print('')

    #
    # print('TOTAL OF REGISTERS')
    # print('IDENTIFY    : '+str(len(results[True]))+" registers")
    # print('UNIDENTIFY : '+str(len(results[False]))+" registers")

#"""This part creates the output files"""



def column_creator(path):

    """This function creates a table with the frequency of each element"""
    if not os.path.exists(path+'tables'):
        os.makedirs(path+'tables')


    # Sequences
    if os.path.exists(path+'SEQ.txt'):
        with open(os.path.join(path+'SEQ.txt')) as f1, open(os.path.join(path+'tables/sequences_table.txt'), 'a') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

    # Modifications
    if os.path.exists(path + 'modifications.txt'):

        with open(os.path.join(path+'modifications.txt')) as f1, open(os.path.join(path+'tables/modifications_table.txt'), 'a') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

    # Spectrum identify:
    if os.path.exists(path + 'spectrum_identify.txt'):

        with open(os.path.join(path+'spectrum_identify.txt')) as f1, open(path+'tables/spectrum_ide_table.txt', 'a') as f3:
            lines1 = f1.read().count('\n')
            f3.write("%s\n%s\n" % ("Spectrum Number",lines1))
        f1.close()
        f3.close()

    if os.path.exists(path + 'spectrum_unidentify.txt'):
        with open(os.path.join(path+'spectrum_unidentify.txt')) as f2, open(path+'tables/spectrum_unide_table.txt', 'a') as f3:
            lines2 = f2.read().count('\n')
            f3.write("%s\n%s\n" % ("Spectrum Number",lines2))
        f2.close()
        f3.close()

    if os.path.exists(path+'taxonomy_identify.txt'):
        # Taxonomy ide:
        with open(os.path.join(path+'taxonomy_identify.txt')) as f1, open(os.path.join(path+'tables/taxonomy_ide_table.txt'), 'a') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()


    if os.path.exists(path + 'taxonomy_unidentify.txt'):
        # Taxonomy unide:
        with open(os.path.join(path+'taxonomy_unidentify.txt')) as f1, open(os.path.join(path+'tables/taxonomy_unide_table.txt'), 'a') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

def main():


#Generate the path that we're going to use in the next function
    (PATH_RELEASE1_IDEN,
     PATH_RELEASE2_IDEN,
     PATH_RELEASE2_UNIDE,
     list_of_files_release1_ide,
     list_of_files_release2_ide,
     list_of_files_release2_unide) = file_checker()


#Create main files.
    read_files(list_of_files_release1_ide, PATH_RELEASE1_IDEN+'cache/') #RELEASE1_identify
    #read_files(list_of_files_release1_unide, PATH_RELEASE1_+'cache/') #RELEASE1_unidentify
    read_files(list_of_files_release2_ide, PATH_RELEASE2_IDEN+'cache/') #RELEASE2_identify
    read_files(list_of_files_release2_unide, PATH_RELEASE2_UNIDE+'cache/') #RELEASE2_unidentify

#Create frequency tables
    column_creator(PATH_RELEASE1_IDEN+'cache/')
    #column_creator(PATH_RELEASE1_IDEN + 'cache/')
    column_creator(PATH_RELEASE2_IDEN + 'cache/')
    column_creator(PATH_RELEASE2_UNIDE + 'cache/')

if __name__ == "__main__":
    main()