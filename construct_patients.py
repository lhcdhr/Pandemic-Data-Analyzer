
import doctest
import matplotlib.pyplot as plt
import datetime


class Patient:

    def __init__(self, number, day_diagnosed, age, sex_gender, \
                    postal, state, temps, days_symptomatic):
        '''
        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> p.num
        0
        '''

        self.num = int(number)
        
        self.day_diagnosed = int(day_diagnosed)
        
        self.age = int(age)
        
        # Convert different expression of sex/gender in to
        # F, M or X.
        if sex_gender in ['F', 'FEMALE', 'FEMME', 'GIRL', 'WOMAN']:
            gender = 'F'
        elif sex_gender in ['M', 'MALE', 'H', 'HOMME', 'BOY', 'MAN']:
            gender = 'M'
        else:
            gender = 'X'
        self.sex_gender = gender

        # Convert postal code.
        if postal[0] !='H':
            postal_code = '000'
        else:
            postal_code = postal[0:3]
        self.postal = postal_code

        
        self.state = state

        # convert temperature
        temperature = []
        temps = str(temps)

        # for 'NONAPPLICALBE' cases
        if temps[0] == 'N':
            temperature.append(0.0)
        else:
            temps = temps.replace('C', '').replace('F','').replace('°', '')
            temps = temps.replace(',','.').replace('-', '.')
            temps = float(temps)
            # convert all temperature greater than 45 to celsius
            if temps > 45:
                temps = (temps-32)*5/9
                temps = round(temps, 2)
                temperature.append(temps)
            else:
                temps = round(temps, 2)
                temperature.append(temps)


        self.temps = temperature

        
        
        self.days_symptomatic = int(days_symptomatic)

    
    def __str__(self):
        '''(Patient) -> Patient
        Return a string with following attributes, seperated by tabs.
        self.num, self.age, self.sex gender, self.postal,
        self.day_diagnosed, self.state, self.days symptomatic, and
        all temperature observed separated by semi-colons.
        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> str(p)
        '0\\t42\\tX\\tH3Z\\t0\\tI\\t12\\t39.0'
        
        '''
        # place those content in order
        # seperate by tab
        info = ''
        info += str(self.num)+'\t'
        info += str(self.age) + '\t'
        info += self.sex_gender +'\t'
        info += self.postal + '\t'
        info += str(self.day_diagnosed)+'\t'
        info += self.state + '\t'
        info += str(self.days_symptomatic)+ '\t'

        temp = ''

        count = 0
        
        # add ';' for updated cases
        for i in range(len(self.temps)):
            count += 1
            if count == len(self.temps):
                temp += str(self.temps[i])
            else:
                temp += str(self.temps[i]) + ';'
        info += temp
        
        return info


    def update(self, new):
        '''(Patient, Patient) -> None
        If the other Patient object's number, sex/gender
        and postal code are the same, then update the
        patient's days_symptomatic to the newer one and
        update the state to the newer one as well. Append
        the new temperature to temp.

        >>> p = Patient('0', '0', '42', 'WOMAN', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0 C', '13')
        >>> p.update(p1)
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t13\\t39.0;40.0'

        >>> p = Patient('0', '0', '42', 'WOMAN', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('0', '1', '42', 'MAN', 'H3Z', 'I', '40,0 C', '13')
        >>> p.update(p1)
        Traceback (most recent call last):
        AssertionError: num/sex gender/postal are not the same
        '''
        # update the object if they are for the same patient
        if new.num == self.num and new.sex_gender == self.sex_gender \
and new.postal == self.postal:
            self.days_symptomatic = new.days_symptomatic
            self.state = new.state
            self.temps.append(new.temps[0])
        # raise AssertionError if not
        else:
            raise AssertionError('num/sex gender/postal are not the same')


def stage_four(input_filename, output_filename):
    '''(str, str) -> dict
    Create a new Patient object for each line. Keep
    and return a dictionary, using the patient's number
    as the key, the Patient object as the values. Update
    if the patient is already in the list. Convert every 
    patient to a string, then sort them by patient number.
    Return the dictionary of patients


    >>> d = stage_four('stage3.tsv', 'stage4.tsv')
    >>> str(d[0])
    '0\\t3\\tF\\tH4C\\t0\\tI\\t6\\t38.4;38.73;38.0'
    
    '''
    # prepare to read and write
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')

    notebook = {}
    
    # add patients to the dictionary, and update them if necessary
    for row in input_file.readlines():
        split_row = row.split('\t')
        p = Patient(split_row[1], split_row[2],\
                    split_row[3], split_row[4], split_row[5], split_row[6],\
                    split_row[7], split_row[8])

        if p.num in notebook:
            notebook[p.num].update(p)
        
        else:
            notebook[int(split_row[1])] = p
    # sort the patient numbers
    keys = list(notebook.keys())
    keys = sorted(keys)

    # write patients sorted by patient number to the new file 
    for key in keys:
        new_row = str(notebook[key])
        output_file.write(new_row)
        output_file.write('\n')

    input_file.close()
    output_file.close()
    
    return notebook
    
        

def fatality_by_age(notebook):
    '''(dict) -> list
    From the input dictionary, round the patients' ages to the
    nearest 5, and calculate probability of fatality for each
    age group. Plot and save it. Return a list of probability
    of deth by age group.
    >>> a = stage_four('datastage3.tsv', 'datastage4.tsv')
    >>> fatality_by_age(a)
    [1.0, 1.0, 1.0, 0.9333333333333333, 1.0, 0.8947368421052632, \
1.0, 0.9629629629629629, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, \
1.0, 1.0, 1.0, 1.0, 1]
    

    '''
    
    age_d = {}
    age_r = {}
    age_prob = {}

    # go through each item in the dictionary
    for key in notebook:

        # round the age to the nearest 5
        fives = notebook[key].age // 5
        remainder = notebook[key].age % 5
        if remainder in [0, 1, 2]:
            rounded_age = fives * 5
        else:
            rounded_age = (fives + 1) * 5
            
        # create a new item if the age is not in the list yet
        # also, for state R and D, they need to be recorded
        
        if (notebook[key].age not in age_d) and (rounded_age not in age_r):
            age_d[rounded_age] = 0
            age_r[rounded_age] = 0
            if notebook[key].state == 'R':
                age_r[rounded_age] += 1
            elif notebook[key].state == 'D':
                age_d[rounded_age] += 1
        else:
            if notebook[key].state == 'R':
                age_r[rounded_age] += 1
            elif notebook[key].state == 'D':
                age_d[rounded_age] += 1

    # calculate probability
    for key in age_d:
        numerator = age_d[key]
        denominator  = age_d[key] + age_r[key]
        if denominator == 0:
 
            age_prob[key] = 1
            
        else:
            prob = numerator / denominator
            age_prob[key] = prob
    

    ages = []
    probs = []

    # sort it according to patient number
    for key in sorted(age_prob):
        ages.append(key)
        probs.append(age_prob[key])

    # draw the graph and save it  
    plt.xlabel('Age')
    plt.ylabel('Deaths / (Deaths+Recoveries)')
    plt.title('Probabilty of death vs age, by Haochen Liu')
    plt.ylim((0, 1.2))
    plt.plot(ages, probs)


    plt.savefig('fatality_by_age.png')
    plt.close()

    # get keys from the dictionary into a list
    probability = list(age_prob.values())

    return probability

    
if __name__ =='__main__':
    doctest.testmod()
       
        
    
