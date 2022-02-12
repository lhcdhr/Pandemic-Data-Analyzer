
import doctest


def which_delimiter(row):
    '''(str)->str
    Return the most commonly used delimiter in the input string.
    It will be a comma, a tab, or a space.
    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('1 1 2021.12.9 1998.7.9 Femme H4C 2H6 Infectée 38,8 5')
    ' '
    >>> which_delimiter('0\\t2\\t2021 2 2\\t 2002.2.2\\tH\\tH4C1N5\\tInfecte')
    '\\t'

    >>> which_delimiter('1234')
    Traceback (most recent call last):
    AssertionError: there is no space/comma/tab
    '''

    
    space = ' '
    tab = '\t'
    comma = ','
    deli = {space: 0, tab: 0, comma: 0}

    # count how many times each delimiter appear in the input string
    deli[tab] = row.count(tab)
    deli[space] = row.count(space)
    deli[comma] = row.count(comma)
    
    # raise AssertionError if there is no required delimiter.
    if deli[space] == 0 and deli[tab] == 0 and deli[comma] == 0:
        raise AssertionError('there is no space/comma/tab')

    # pick and return the most common delimiter
    most_common = max(deli, key=deli.get)
    return most_common


def stage_one(input_filename, output_filename):
    '''(str,str)->int
    For each row in input_filename, convert the most commom delimiter
    to tab, and all letters becomes upper-cased. Change all '/' and '.'
    to '-'. Write the converted row to output_filename, and return an integer
    represents how many rows were written to the new file.
    
    >>> stage_one('example.txt', 'example.tsv')
    4
    >>> stage_one('data-short.txt', 'stage1.tsv')
    10
    >>> stage_one('100row.txt', '100rowstage1.tsv')
    100
    >>> stage_one('data.txt', 'datastage1.tsv')
    3000
    '''
    # prepare to read and write
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')

    count = 0
    # go through every row in the file
    for row in input_file.readlines():

        # find the most commom delimiter
        most_common = which_delimiter(row)
        # replace it with tab
        row = row.replace(most_common, '\t')

        # replace other characters
        row = row.replace('/','-')
        row = row.replace('.','-')

        # all capitalized
        row = row.upper()

        # write the converted row into the new file
        output_file.write(row)
        count += 1

    input_file.close()
    output_file.close()
        
    return count

        
def stage_two(input_filename, output_filename):
    '''(str,str)->int
    Continue to clean up the data. For each row in input_filename,
    it should have 9 colunms. Convert every row to 9 colunms and write
    the converted row to the new file. Return an integer represents how
    many rows are written.
    
    >>> stage_two('example.tsv', 'example2.tsv')
    4
    >>> stage_two('stage1.tsv', 'stage2.tsv')
    10
    >>> stage_two('100rowstage1.tsv', '100rowstage2.tsv')
    100
    >>> stage_two('datastage1.tsv', 'datastage2.tsv')
    3000
    '''
    
    # prepare to read and write
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')
    
    count = 0

    # go through every row in the file
    for row in input_file.readlines():
        # tab is the delimiter
        # use it to seperate each colunms
        split_row = row.split('\t')

        # convert postals codes
        # If column 6 starts with a digit,
        # then the postal codes has been seperated.
        if split_row[6][0].isdigit():
            split_row[5]=split_row[5] + split_row[6]
            split_row.pop(6)

        # If column 6 starts with 'A',
        # then it is a seperated NON APPLICABLE.
        # Combine those 2 colunms.
        elif split_row[6][0] == 'A':
            split_row[5] = split_row[5] + split_row[6]
            split_row.pop(6)

        # Or the postal codes stays in one colunm,
        # but there is a space between.
        # Remove the space.
        else:
            split_row[5] = split_row[5].replace(' ', '')


        # After get postal code converted, if there are still
        # more than 9 colunms, then temperature is seperated.
        if len(split_row)>9:
            
            if split_row[8][0].isdigit():
                split_row[8]=split_row[8].replace(' ','')
                split_row[7]=split_row[7]+'.'+split_row[8]
                split_row.pop(8)
                
            else:
                split_row[8]=split_row[8].replace(' ','')    
                split_row[7]=split_row[7]+split_row[8]
                split_row.pop(8)
            
        new_row = ''

        # Merge the splitted row back together and
        # write it to the new file.
        for i in split_row:
            new_row += i
            new_row += '\t'
            
        new_row = new_row[:-1]
        
        output_file.write(new_row)
        count += 1
        
    input_file.close()
    output_file.close()
    
    return count
    



if __name__=='__main__':


    doctest.testmod()




    
