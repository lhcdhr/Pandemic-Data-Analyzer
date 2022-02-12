
import doctest
import matplotlib.pyplot as plt
import datetime

def date_diff(date1, date2):
    '''(str, str)->int
    Return an integer that shows the difference
    between the two input dates as a integer in
    days. If the first date is earlier than the
    second date, the number should be positive;
    otherwise thenumber should be negative.
    
    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2018-10-31', '2000-11-2')
    -6572
    '''
    # split two dates into two lists
    date1 = date1.split('-')
    date2 = date2.split('-')

    # put the numbers into the format of date
    d1 = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
    d2 = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))

    # calculate the difference between the two input
    diff = d2-d1
    diff = diff.days
    return diff
    
def get_age(date1, date2):
    '''(str, str)-> int
    Return an integer showing how many complete years
    are the two input dates are part.
    
    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    '''
    age_days = date_diff(date1, date2)
    age_years = int(age_days/365.2425)
    return age_years


def stage_three(input_filename, output_filename):
    '''(str, str)-> dict

    Replace the date of each row with the date_diff of that
    date and the index date, replace the date of birth with
    age at the time of index date, and replace the status
    with I, R and D. Return a dictionary with each day of
    pandemic being keys and the number of people of each
    state on that day be the value(the value is a dictionary).
    
    >>> stage_three('stage2.tsv', 'stage3.tsv')
    {0: {'I': 1, 'D': 0, 'R': 0}, \
1: {'I': 3, 'D': 0, 'R': 0}, \
2: {'I': 6, 'D': 0, 'R': 0}}
    '''

    day_state = {}
    new_row = ''

    # prepare to read and write
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')

    # read the first row and get index date
    first_row = input_file.readline()
    first_row_list = first_row.split('\t')
    index_date = first_row_list[2]
    
    # read the file from the very beginning
    input_file.seek(0)
    for row in input_file.readlines():
        
        split_row = row.split('\t')

        # convertions of dates
        birth_date = split_row[3]
        entry_date = split_row[2]

        age = get_age(birth_date, entry_date)
        index_diff = date_diff(index_date, entry_date)
        
        split_row[2] = index_diff
        split_row[3] = age

        # convertion of states
        if split_row[6][0] == 'i' or split_row[6][0] =='I':
            split_row[6] = 'I'
        elif split_row[6][0] == 'r' or split_row[6][0] == 'R':
            split_row[6] = 'R'
        elif split_row[6][0] == 'd' or split_row[6][0] == 'D':
            split_row[6] = 'D'
        elif split_row[6][0] == 'm' or split_row[6][0] == 'M':
            split_row[6] = 'D'

        # fill them to the dictionary
        if day_state.__contains__(split_row[2]):
            day_state[split_row[2]][split_row[6][0]] += 1
        else:
            day_state[split_row[2]] = {'I': 0, 'D': 0, 'R': 0}
            day_state[split_row[2]][split_row[6][0]] += 1
        # form the new row    
        for i in split_row:
            new_row += str(i)
            new_row += '\t'
        new_row =  new_row[:-1]

        # write the new row to the new file
        output_file.write(new_row)
        new_row = ''

    input_file.close()
    output_file.close()
        
    return day_state

def plot_time_series(d):
    '''(dict) -> list
    Return a list of lists, where each sublist represents each day of
    the pandemic, and the sublist shows [number of infected, number of
    recovered, number of dead]. Plot the lists and save it.
    >>> a = stage_three('datastage2.tsv', 'datastage3.tsv')
    >>> plot_time_series(a)
    [[1, 0, 0], [3, 0, 0], [9, 0, 0], [21, 4, 0], \
[61, 3, 0], [162, 16, 0], [455, 24, 1], \
[1234, 83, 2], [705, 215, 1]]
    '''

    time_series = []
    infected = []
    recovered = []
    dead = []
    
    # From the dictionary, arrage the date by its
    # states. Each state has a list of data
    for day in d:

        day_list = []
        day_list.append(d[day]['I'])
        day_list.append(d[day]['D'])
        day_list.append(d[day]['R'])
        
        time_series.append(day_list)

        infected.append(d[day]['I'])
        recovered.append(d[day]['R'])
        dead.append(d[day]['D'])
        

    # draw the graph
    plt.xlabel('Days into Pandemic')
    plt.ylabel('Number of People')
    plt.title('Time series of early pandemic, by Haochen Liu')
    x = range(0, len(d))
    plt.plot(x, infected)
    plt.plot(x, recovered)
    plt.plot(x, dead)
    plt.legend(['Infected', 'Recovered', 'Dead'])
    plt.savefig('time_series.png')
    plt.close()
    

    return time_series


if __name__=='__main__':
    doctest.testmod()

