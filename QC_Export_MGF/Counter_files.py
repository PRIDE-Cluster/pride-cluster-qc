#This program takes different information from .MGF files in order to generate different outputs that will be used by the R Script.

# IMPORTANT INFORMATION. In the release of 2014, we didn't used any filter previusly, because of that we'll not have two folders (Identify and
# unidentify files). For futures releases (Ex. 2017 and 2018, ), remove the # from PATH_RELEASE_UNID and remove None. 
#Remember to change the PATH with the new release in future QCs.
import glob
import os 

def file_checker():
    ################################################################
    """The PATH of these function must be changed in each release"""
    PATH_RELEASE1_IDEN = os.getcwd()+'/archive_all_2014-10/'
    PATH_RELEASE1_UNIDE = None
    #PATH_RELEASE1_UNIDE = os.getcwd()+'/archive_all_2014-10/'

    PATH_RELEASE2_IDEN = os.getcwd()+'/archive_all_2016-10/archive_identified_2016-10/'
    PATH_RELEASE2_UNIDE = os.getcwd() + '/archive_all_2016-10/archive_unidentified_2016-10/'
    ################################################################

    #This global function finds the .mgf files
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
    results = {True:[], False:[]}

    for fileName in list_of_files:

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

#METER UN IF COMO EN EL ANTERIOR CASO PARA QUE TE IMPRIMA AQUELLOS QUE SON FALSOS Y LOS QUE SON VERDADEROS.

    for result in results:
        if result:
            if len(results[True]) != 0:
                with open(os.path.join(path+'ID_identify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TITLE']['id']+"\n")
                    output.close()

                with open(os.path.join(path+'spectrum_identify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TITLE']['spectrum']+"\n")
                    output.close()

                with open(os.path.join(path + 'taxonomy_identify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TAXONOMY'] + "\n")
                    output.close()

                if (result):
                    with open(os.path.join(path+'SEQ.txt'), 'w') as output:
                        for register in results[result]:
                            output.write(register['SEQ']+"\n")
                        output.close()

                    with open(os.path.join(path+'USER03.txt'), 'w') as output:
                        for register in results[result]:
                            output.write(register['USER03']+"\n")
                        output.close()
        else:
            if len(results[False])!=0:
                with open(os.path.join(path+'ID_unidentify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TITLE']['id']+"\n")
                    output.close()

                with open(os.path.join(path+'spectrum_unidentify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TITLE']['spectrum']+"\n")
                    output.close()

                with open(os.path.join(path + 'taxonomy_unidentify.txt'), 'w') as output:
                    for register in results[result]:
                        output.write(register['TAXONOMY'] + "\n")
                    output.close()

                if (result):
                    with open(os.path.join(path+'SEQ.txt'), 'w') as output:
                        for register in results[result]:
                            output.write(register['SEQ']+"\n")
                        output.close()

                    with open(os.path.join(path+'USER03.txt'), 'w') as output:
                        for register in results[result]:
                            output.write(register['USER03']+"\n")
                        output.close()



def main():


    (PATH_RELEASE1_IDEN,
     PATH_RELEASE2_IDEN,
     PATH_RELEASE2_UNIDE,
     list_of_files_release1_ide,
     list_of_files_release2_ide,
     list_of_files_release2_unide) = file_checker()

    read_files(list_of_files_release1_ide, PATH_RELEASE1_IDEN+'cache/')
    
    #read_files(list_of_files_release1_unide, PATH_RELEASE1_+'cache/')

    read_files(list_of_files_release2_ide, PATH_RELEASE2_IDEN+'cache/')

    read_files(list_of_files_release2_unide, PATH_RELEASE2_UNIDE+'cache/')





if __name__ == "__main__":
    main()