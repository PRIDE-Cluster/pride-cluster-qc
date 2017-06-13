"""
This program takes different information from .MGF files in order to generate different outputs that will be used by the R
Script.
"""
import glob
import os
import re
import sys, getopt
from collections import Counter


def file_checker(pathCurrentRelease, pathPreviousRelease, pathOutput):
    """
    The PATH of these function must be changed in each release
    :param pathCurrentRelease:
    :param pathPreviousRelease:
    :param pathOutput:
    :return:
    """

    listCurrentReleaseFiles = glob.glob(pathCurrentRelease + "/" + '*.mgf')
    listPreviousReleaseFiles = glob.glob(pathPreviousRelease + "/" + '*.mgf')

    # Check if exist cache folder. If not will make it.
    # RELEASE 1
    if not os.path.exists(pathOutput + '/cache'):
        os.makedirs(pathOutput + '/cache')

    return listCurrentReleaseFiles, listPreviousReleaseFiles


def read_files(list_of_files, path, tagCache):
    """
     This function creates a list in order to classificate different releases between identify and unidentify.
     This also create outputs with different information that will be used in the R script

    :param list_of_files:
    :param path:
    :return:
    """

    results = {True: [], False: []}

    for fileName in list_of_files:
        results = {True: [], False: []}
        with open(fileName) as fp:
            register = {}
            identified = False
            for line in fp:
                line = line.rstrip()
                if (line.find('TITLE') != -1 or line.find('PEPMASS') != -1 or line.find('CHARGE') != -1 or line.find(
                        'SEQ') != -1 or line.find('USER03') != -1 or line.find('TAXONOMY') != -1):
                    if line.find('TITLE=id') != -1:
                        parts = line.split(';')
                        elements = parts[0].split('=')
                        spectrum = parts[2].split('=')
                        composition = {'id': elements[2], 'file': parts[1], 'spectrum': spectrum[1]}

                        register[elements[0]] = composition
                    else:
                        elements = line.split('=')
                        register[elements[0]] = elements[1]
                    if (line.find('SEQ') != -1):
                        identified = True
                elif line.find('END IONS') != -1:
                    results[identified].append(register)
                    identified = False
                    register = {}
        fp.close()

        for result in results:
            if result:
                if len(results[True]) != 0:
                    with open(os.path.join(path + tagCache + 'ID_identify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['id'] + "\n")
                    output.close()

                    with open(os.path.join(path + tagCache + 'spectrum_identify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['spectrum'] + "\n")
                    output.close()

                    with open(os.path.join(path + tagCache + 'taxonomy_identify.txt'), 'a') as output:
                        for register in results[result]:
                            if 'TAXONOMY' in register:
                                output.write(register['TAXONOMY'] + "\n")
                            else:
                                continue
                    output.close()

                    if (result):
                        with open(os.path.join(path + tagCache + 'SEQ.txt'), 'a') as output:
                            for register in results[result]:
                                output.write(register['SEQ'] + "\n")
                        output.close()

                        with open(os.path.join(path + tagCache + 'modifications.txt'), 'a') as output:
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
                    with open(os.path.join(path + tagCache + 'ID_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['id'] + "\n")
                    output.close()

                    with open(os.path.join(path + tagCache + 'spectrum_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            output.write(register['TITLE']['spectrum'] + "\n")
                    output.close()

                    with open(os.path.join(path + tagCache + 'taxonomy_unidentify.txt'), 'a') as output:
                        for register in results[result]:
                            if 'TAXONOMY' in register:
                                output.write(register['TAXONOMY'] + "\n")
                            else:
                                continue
                    output.close()


def column_creator(outputPath, tagCache):
    """
     This function creates a table with the frequency of each element
    :param outputPath:
    :return:
    """

    # Sequences
    if os.path.exists(outputPath + tagCache + 'SEQ.txt'):
        with open(os.path.join(outputPath + tagCache + 'SEQ.txt')) as f1, open(os.path.join(outputPath + tagCache + 'tables_sequences_table.txt'),'w') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

    # Modifications
    if os.path.exists(outputPath + tagCache + 'modifications.txt'):

        with open(os.path.join(outputPath + tagCache + 'modifications.txt')) as f1, open(os.path.join(outputPath + tagCache + 'tables_modifications_table.txt'), 'w') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

    # Spectrum identify:
    if os.path.exists(outputPath + tagCache + 'spectrum_identify.txt'):
        with open(os.path.join(outputPath + tagCache + 'spectrum_identify.txt')) as f1, open(outputPath + tagCache + 'tables_spectrum_ide_table.txt','w') as f3:
            lines1 = f1.read().count('\n')
            f3.write("%s\n%s\n" % ("Spectrum Number", lines1))
        f1.close()
        f3.close()

    if os.path.exists(outputPath + tagCache + 'spectrum_unidentify.txt'):
        with open(os.path.join(outputPath + tagCache + 'spectrum_unidentify.txt')) as f2, open(outputPath + tagCache + 'tables_spectrum_unide_table.txt','w') as f3:
            lines2 = f2.read().count('\n')
            f3.write("%s\n%s\n" % ("Spectrum Number", lines2))
        f2.close()
        f3.close()

    if os.path.exists(outputPath + tagCache + 'taxonomy_identify.txt'):
        # Taxonomy ide:
        with open(os.path.join(outputPath + tagCache   + 'taxonomy_identify.txt')) as f1, open(os.path.join(outputPath   + tagCache   + 'tables_taxonomy_ide_table.txt'), 'w') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()

    if os.path.exists(outputPath + tagCache + 'taxonomy_unidentify.txt'):
        # Taxonomy unide:
        with open(os.path.join(outputPath + tagCache + 'taxonomy_unidentify.txt')) as f1, open(os.path.join(outputPath + tagCache + 'tables_taxonomy_unide_table.txt'), 'w') as f2:
            c = Counter(x.strip() for x in f1)
            for x in c:
                f2.write("%s\t%s\n" % (x, str(c[x])))
        f1.close()
        f2.close()


def main(argv):
    # Getting the corresponding parameters.

    pathPreviousRelease = ''
    pathCurrentRelease = ''
    pathOutput = ''

    try:
        opts, args = getopt.getopt(argv, "hi:p:o:", ["ifile=", "ifileprev=", "ofile="])
    except getopt.GetoptError:
        print('file_counter.py -i <inputcurrent> -p <inputprevious> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('file_counter.py -i <inputcurrent> -p <inputprevious> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            pathCurrentRelease = arg
        elif opt in ("-p", "--ifileprev"):
            pathPreviousRelease = arg
        elif opt in ("-o", "--ofile"):
            pathOutput = arg

    print('Current Cluster Release Import Folder', pathCurrentRelease)
    print('Previous Cluster Release Import Folder', pathPreviousRelease)

    (listCurrentFiles, listPreviousFiles) = file_checker(pathCurrentRelease, pathPreviousRelease, pathOutput)

    # Create main files.
    read_files(listCurrentFiles, pathOutput  +  '/cache/', "CurrentRelease_")  # RELEASE1_identify
    read_files(listPreviousFiles, pathOutput +  '/cache/', "PreviousRelease_")  # RELEASE2_identify

    # Create frequency tables
    column_creator(pathOutput  + '/cache/', "CurrentRelease_")
    column_creator(pathOutput  + '/cache/', "PreviousRelease_")


if __name__ == "__main__":
    main(sys.argv[1:])
