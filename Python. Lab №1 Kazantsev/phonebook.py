import csv
from datetime import date


def csv_reader(file_csv):
    with open(file_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = list()
        data = [i for i in reader]
    return data


def csv_writer(file_csv, data):
    fieldnames = ['Name', 'Surname', 'Phone number', 'Date of birth']
    with open(file_csv, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def one_person(obj):
    person = ''
    for k, v in obj.items():
        person += v
        person += '; '
    person = person[0:-2]
    return person


def show_all(data):
    n = 0
    for x in data:
        n += 1
        print(n, ' - ', one_person(x))


def search(data):
    copy_data1 = data
    new_data = list()
    criteria = ['Name', 'Surname', 'Phone number', 'Date of birth']
    answer = ''
    while criteria and (answer != 'No'):
        print('Select the search criteria:')
        for i in criteria:
            print(i)
        flag = True
        while flag:
            crt = input('Criteria: ')
            crt = crt.capitalize()
            for i in criteria:
                if crt == i:
                    flag = False
            if flag:
                print('Incorrect criteria, try again!')
        value = (input('Write the value: '))
        for x in copy_data1:
            if value == x[crt]:
                new_data.append(x)
        if not new_data:
            print('No matches')
            return None
        criteria.remove(crt)
        if criteria:
            print('Do you want to add another criteria?')
            answer = input()
            answer = answer.capitalize()
            while (answer != 'Yes') and (answer != 'No'):
                answer = input('Incorrect criteria, try again!')
                answer = answer.capitalize()
        copy_data1 = new_data
        new_data = []
    if copy_data1:
        show_all(copy_data1)


def search_by_dob(data):
    new_data = list()
    dob = input('Date of birth:')
    for i in data:
        if i['Date of birth'][:5] == dob:
            new_data.append(i)
    if new_data:
        show_all(new_data)
    else:
        print('No matches')


def check_date(date_str):
    if len(date_str) == 0:
        return True
    if len(date_str) != 10:
        return False
    d = int(date_str[0:2])
    m = int(date_str[3:5])
    y = int(date_str[6:])
    if y > 2020:
        return False
    try:
        date(y, m, d)
        return True
    except ValueError:
        return False


def check_n_s(ns_str):
    for i in ns_str:
        if not ((i == ' ') or (i.isalnum())):
            return True
    return False


def add_new(record):
    value = ''
    for i in record:
        if i != ';':
            value += i
        else:
            yield value
            value = ''
    yield value


def check(data, func, pers):
    if len(pers['Name']) == 0:
        print('Incorrect Name, please try again!')
        func(data)
        return None
    if check_n_s(pers['Name']):
        print('Incorrect Name, please try again!')
        func(data)
        return None
    pers['Name'] = pers['Name'].capitalize()
    if len(pers['Surname']) == 0:
        print('Incorrect Surname, please try again!')
        func(data)
        return None
    if check_n_s(pers['Surname']):
        print('Incorrect Surname, please try again!')
        func(data)
        return None
    pers['Surname'] = pers['Surname'].capitalize()
    if pers['Phone number'][:2] == '+7':
        pers['Phone number'] = '8' + pers['Phone number'][2:]
    if (pers['Phone number'][0] != '8') or (len(pers['Phone number']) != 11):
        print('Incorrect Phone number, please try again!')
        func(data)
        return None
    if not check_date(pers['Date of birth']):
        print('Incorrect Date of birth, please try again!')
        func(data)
        return None


def adding(data):
    new_record = input('Write the string please: ')
    count = 0
    for i in new_record:
        if i == ';':
            count += 1
    if count != 3:
        print('Incorrect string, please try again!')
        adding(data)
        return None
    criteria = ['Name', 'Surname', 'Phone number', 'Date of birth']
    new_dict = dict()
    j = 0
    for i in add_new(new_record):
        new_dict[criteria[j]] = i
        j += 1
    check(data, adding, new_dict)
    for i in data:
        if (i['Name'] == new_dict['Name']) and (i['Surname'] == new_dict['Surname']) or (i['Phone number'] == new_dict['Phone number']):
            print('This person is already in the phone book')
            ans = ''
            while (ans != 'Yes') and (ans != 'No'):
                ans = input('Do you want to change your data? Please write Yes or No: ')
                ans = ans.capitalize()
            if ans == 'Yes':
                adding(data)
                return None
            else:
                return None
    data.append(new_dict)
    data = sorted(data, key=lambda x: x['Name'])
    #data = sorted(new_data, key=lambda x: x['Surname'])
    print('The person added to the directory')


def delete(data):
    flag = True
    while flag:
        name = input('Name: ')
        surname = input('Surname: ')
        for i in data:
            if (i['Name'] == name) and (i['Surname'] == surname):
                data.remove(i)
                print('The person is deleted from the phonebook')
                flag = False
                return None
        else:
            print('Such a person does not exist in the list, try again!')


def delete_by_number(data):
    flag = True
    while flag:
        number = input('Phone number: ')
        if number[:2] == '+7':
            number = '8' + number[2:]
        if (number[0] != '8') or (len(number) != 11):
            print('Incorrect Phone number, please try again!')
            delete_by_number(data)
            return None
        for i in data:
            if i['Phone number'] == number:
                data.remove(i)
                print('The person is deleted from the phonebook')
                flag = False
                return None
        print('Such a person does not exist in the list, try again!')


def change(data):
    name = input('Please enter Name: ')
    surname = input('Please enter Surname: ')
    person = ''
    for i in data:
        if (i['Name'] == name) and (i['Surname'] == surname):
            person = i
    if person == '':
        print('Such a person does not exist in the list')
        ans =''
        while (ans != 'Yes') and (ans != 'No'):
            ans = input('Do you want to try again? Please write Yes or No: ')
            ans = ans.capitalize()
        if ans == 'Yes':
            change(data)
            return None
        else:
            return None
    print('This is ', one_person(person))
    criteria = ['Name', 'Surname', 'Phone number', 'Date of birth']
    answer = ''
    while criteria and (answer != 'No'):
        print('Select the criteria:')
        for i in criteria:
            print(i)
        flag = True
        while flag:
            crt = input()
            crt = crt.capitalize()
            for i in criteria:
                if crt == i:
                    flag = False
            if flag:
                print('Incorrect criteria, try again!')
        value = (input('Write the changed value: '))
        if crt == 'Name':
            if check_n_s(value):
                print('Incorrect Name, please try again!')
                change(data)
                return None
        elif crt == 'Surname':
            if check_n_s(value):
                print('Incorrect Surname, please try again!')
                change(data)
                return None
        elif crt == 'Phone number':
            if value[:2] == '+7':
                value = '8' + value[2:]
            if (value[0] != '8') or (len(value) != 11):
                print('Incorrect Phone number, please try again!')
                change(data)
                return None
        else:
            if not check_date(value):
                print('Incorrect Date of birth, please try again!')
                change(data)
                return None
        person[crt] = value
        criteria.remove(crt)
        if criteria:
            print('Do you want to add another criteria?')
            answer = input()
            answer = answer.capitalize()
            while (answer != 'Yes') and (answer != 'No'):
                answer = input('Incorrect criteria, try again!')
                answer = answer.capitalize()
    print('The data is changed')


def calculate_age(data):
    name = input('Please enter Name: ')
    surname = input('Please enter Surname: ')
    person = ''
    for i in data:
        if (i['Name'] == name) and (i['Surname'] == surname):
            person = i
    if person == '':
        print('Such a person does not exist in the list')
        ans = ''
        while (ans != 'Yes') and (ans != 'No'):
            ans = input('Do you want to try again? Please write Yes or No: ')
            ans = ans.capitalize()
        if ans == 'Yes':
            calculate_age(data)
            return None
        else:
            return None
    print('This is ', one_person(person))
    criteria = ['Name', 'Surname', 'Phone number', 'Date of birth']
    born_date = person['Date of birth']
    if len(born_date) == 0:
        print('The person do not have the date of birth')
    d = int(born_date[0:2])
    m = int(born_date[3:5])
    y = int(born_date[6:])
    today = date.today()
    print('Age:', today.year - y - ((today.month, today.day) < (m, d)), 'years')


def operations():
    print('0 - View all operations')
    print('1 - View all directory entries')
    print('2 - Search for a person in the directory')
    print('3 - Search for a person in the directory by Date of birth')
    print('4 - Add a new record')
    print('5 - Delete a record from the directory')
    print('6 - Delete a record from the directory by phone number')
    print('7 - Change any field in a directory record')
    print('8 - Display the age of the person')
    print('9 - Quit the program')


directory = csv_reader('phonebook.csv')
directory = sorted(directory, key=lambda x: x['Name'])
print('Hello, I am a phonebook. This is a list of my  available operations:')
operations()
oper = ''
while oper != '9':
    oper = input('Please write a number of the operation: ')
    if oper == '0':
        operations()
        print('-' * 50)
    elif oper == '1':
        print('You chose to view all records')
        show_all(directory)
        print('-'*50)
    elif oper == '2':
        print('You chose to search for a person')
        search(directory)
        print('-' * 50)
    elif oper == '3':
        print('You chose to search for a person in the directory by Date of birth. To do this please enter DD.MM')
        search_by_dob(directory)
        print('-' * 50)
    elif oper == '4':
        print('You chose to add a new person. To do this please enter Name;Surname;XXXXXXXXXXX;DD.MM.YYYY')
        adding(directory)
        directory = sorted(directory, key=lambda x: x['Name'])
        print('-' * 50)
    elif oper == '5':
        print('You chose to delete a record. To do this please enter Name and Surname')
        delete(directory)
        print('-' * 50)
    elif oper == '6':
        print('You chose to delete a record by phone number. To do this please enter Phone number')
        delete_by_number(directory)
        print('-' * 50)
    elif oper == '7':
        print('You chose to change information about a person. To do this please find the person')
        change(directory)
        print('-' * 50)
    elif oper == '8':
        print('You chose to display the age of a person. To do this please find the person')
        calculate_age(directory)
        print('-' * 50)
    elif oper == '9':
        print('You chose to quit the program')
    else:
        print('You entered the number of the operation incorrectly. Try again')
csv_writer('phonebook.csv', directory)


