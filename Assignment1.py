import pandas as pd 
import re
from datetime import datetime, date, timedelta
import calendar
import csv
 

 #read orders
#df.info() #print information
#print(df.head()) #print first 5 columns of the order list
#print(df.tail()) #print last 5 columns of the order list

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

        ###################### write to file #################
        # valid_df = pd.DataFrame([order.to_dict() for order in valid_orders])
        # invalid_df = pd.DataFrame([order.to_dict() for order in invalid_orders])
        
        # valid_df.to_csv('valid_orders.csv', index=False)
        # invalid_df.to_csv('invalid_orders.csv', index=False)
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
    def __init__(self, name, birthday, email, state, zipcode):

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
        return weekday.weekday()!=0 or weekday.day>7 #weekday() method returns a datetime object with the day of the week as an integer so according to our condition 0 is represented as monday (1 as tuesday... 6 as sunday) and weekday>7 to check if value is greater than 7 i.e this checks if day of week is not a=monday.
#so it returns true if either of the condition is holds true or else returns false.
#for example: if someone is born on 3rd of july 2023(which is the first Monday of the month) the weekday method will return False as the method will return it as 0 which is not valid and hence we will get the output as False
#similarly, if someone is born on 4th of july 2023(which is tuesday) it will be returned as True.


    #4) writing a function for email validation
    def check_email(self):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #regular expression
        if re.fullmatch(pattern, self.email): #match the entire input string against the regular expression 
            return True
        else:
            return False

    #21 years 
    def calculateAge(self):
        birth=datetime.strptime(self.birthday, '%m/%d/%Y')
        today = date.today()
        age = today.year - birth.year
        if(today.month<birth.month or (today.month==birth.month and today.day<birth.day)): #here we just check if the person has not yet celebrated their birthday in the current year. again in this case we needs to consider 2 conditions if the person is born in august of 2023 and currently it is july of 2023 the person's birthday has not occured yet or we need to check if person is born on 29th of july and currently it is 24th of july then also the person has not yet born so for such particular individual we need to recalculate his/her age by performing age-1 and if any of the conditions holds false we just return and check if person is >=21 and return it.
            age-=1
        return age>=21
if __name__ == '__main__':
    acmewines_order = AcmewinesOrder()
    acmewines_order.processfile()
    acmewines_order.write() 