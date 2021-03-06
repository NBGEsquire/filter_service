"""
This is a UI that was made only to show the user how the filter service works. This is to be used with the data.json
file that is included, which contains a mock database that has been exported to JSON.
"""

def create_terms():
    filter_terms = open('filter_terms.txt', 'w+')
    attr = ""
    print("Which category would you like to filter? Class, Assignment, or Due Date?")
    while attr != 'done':
        attr = input('Enter "Class", "Assignment", or "Due" and press return? (Note: enter \"done\" to continue): ')
        if attr == 'done':
            print('continue.....')
            return
        print('What term(s) would you like to filter for within the category? (Dates should be formatted YYYY/MM/DD)')
        term = input('Enter the term and press return: ')
        if term == '':
            print('Invalid Term...Start again!!')
            create_terms()
        filter_terms.write(attr + '\n')
        filter_terms.write(term + '\n')
    filter_terms.close()


create_terms()
