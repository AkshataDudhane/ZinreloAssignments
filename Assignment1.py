import pandas as pd 
import re
from datetime import datetime, date, timedelta
import calendar
import csv
 


class AcmewinesOrder:
    def __init__(self):
        self.df = pd.read_csv(r"orders.csv")
        self.valid_orders = []
        self.invalid_orders = []
    def processfile(self):
        for _, row in self.df.iterrows():
            order = Order(row['ID'], row['Name'],row['Birthday'], row['Email'], row['State'], row['ZipCode'])
            if order.validate_order():
                self.valid_orders.append(order)
            else:
                self.invalid_orders.append(order)

    def write(self):
        with open('valid_orders.csv', 'w', newline='') as valid:
            writer = csv.writer(valid)
            writer.writerows([[order.order_id]] for order in self.valid_orders)

        with open('invalid_orders.csv', 'w', newline='') as invalid:
            writer = csv.writer(invalid)
            writer.writerows([[order.order_id]] for order in self.invalid_orders)

print("Analyzed successfully")

class Order:
    def __init__(self, order_id, name,birthday, email, state, zipcode):
        self.order_id = order_id
        self.user=User(name,birthday,email,state,zipcode)
    def validate_order(self):
        return self.user.check_state() & self.user.check_zip() & self.user.val_weekday() & self.user.check_email() & self.user.calculateAge()


                
class User:
    def __init__(self,name, birthday, email, state, zipcode):

        self.name = name
        self.birthday = birthday
        self.email = email
        self.state = state
        self.zipcode = zipcode

#writing a function for : No wine can ship to New Jersey, Connecticut, Pennsylvania, Massachusetts, Illinois, Idaho or Oregon
    def check_state(self):

        if self.state not in ['NJ','CT','PA','MA','IL','ID','OR']:
            return True
        else:
            return False
        

    #2)writing the function for: Wine can not ship to any zipcode that has two consecutive numbers next to each other


    #it takes zipcode as an input and converts it into a string.
    def check_zip(self):
        zip_str=str(self.zipcode)
        for i in range(len(zip_str)-1): #iterating through the characters
            if (int(zip_str[i])+1==int(zip_str[i+1]) or int(zip_str[i+1])+1==int(zip_str[i])): #checking if the current character and next character if find return true else false
                return False
        return True


    #3) writing a function to return wine not sold to anyone born on the first Monday of the month.

    def val_weekday(self):
        weekday=datetime.strptime(self.birthday, '%m/%d/%Y') #converting weekday to a datetime object and matching the date format
        return weekday.weekday()!=0 or weekday.day>7
    #returns true if the particular day is not the first monday(0) or day should be greater than 7.


    #4) writing a function for email validation
    def check_email(self):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #regex pattern
        if re.fullmatch(pattern, self.email): #match the entire input string against the regular expression 
            return True
        else:
            return False

    #21 years 
    def calculateAge(self):
        birth=datetime.strptime(self.birthday, '%m/%d/%Y')
        today = date.today()
        age = today.year - birth.year
        if(today.month<birth.month or (today.month==birth.month and today.day<birth.day)):
            '''to check if person's is birth month or date falls after the current month or date
            if birth year=2002 age will be considered as 21.
            if birthday is on 26th july 2023, present month=birth month and present date(25)<birth date(26)
            '''
            age-=1
            #we need to subtract age by 1 so actual age will be 20
        return age>=21
if __name__ == '__main__':
    acmewines_order = AcmewinesOrder()
    acmewines_order.processfile()
    acmewines_order.write() 