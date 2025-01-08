import re # module imported to use regex for the date format and use alongside glob to see files in directory
import calendar # mainly used here to check if the year input is a leap year or not
import glob # keep track and view files in directory
import matplotlib.pyplot as plt # to see visualisations of the expenses

DATE_FORMAT = r"^\d{2}-\d{2}$" # regex to match date with user input date

class Expense: # an Expense object is created whereby each expense user inputs will be an instance containing these properties
	def __init__(self, desc, amount, category, date_of_expense):
		self.desc = desc
		self.amount = amount
		self.category = category
		self.date_of_expense = date_of_expense
	
	def __repr__(self): # used to represent a specific instance of this object class in this way, otherwise the memory address is returned
		return f"{self.desc}, {self.amount:.1f}, {self.category}, {self.date_of_expense}"

def date_format_checker(date_str, year): # function to check if date entered is correct
		
	if re.match(DATE_FORMAT, date_str):
		split_date = date_str.split('-')

		month = int(split_date[0])
		day = int(split_date[1])

		if month < 1 or month > 12:
			raise ValueError(f"Invalid Month Entered.\n")
		
		if ((day < 1) or ((month == 4 or month == 6 or month == 9 or month == 11) and (day > 30)) or (day > 31)):
			raise ValueError(f"Invalid Day Entered.\n")
		
		if month == 2:
			if (calendar.isleap(year) == True) and (day > 29):
				raise ValueError(f"Invalid Day. You have input a Leap Year.\n")

			elif (calendar.isleap(year) == False) and (day > 28):
				raise ValueError(f"Invalid Day.\n")
			
	else:
		return 1
	
	return 0

def user_input(year): # user input data is stored in various variables and an instance of the Expense object class is made

	expense_date = input(f"Enter the Date of your Expense (MM-DD):\n")

	if date_format_checker(expense_date, year) == 1:
		raise TypeError(f"Invalid Date Format. Please Enter your Date in the format specified\n")

	expense_desc = input(f"Enter a Description:\n")

	expense_amount = float(input(f"Enter the amount (in MVR):\n"))

	print(f"Please Select a Category for your Expense:\n")

	expense_categories = {1 : "Entertainment", 2 : "Food & Drinks", 3 : "General Purchases", 4 : "Living Expense", 5 : "Other"}
	
	for num, category in expense_categories.items():
		print(f"{num}. {category}\n")

	selected_num = int(input(f"Enter the number of the category of your choice:\n"))

	if selected_num in expense_categories:
		selected_category = expense_categories[selected_num]
		expense = Expense(expense_desc, expense_amount, selected_category, expense_date)
		return expense
	else:
		raise ValueError("Invalid Number. Please pick \n")


def store_data(expense: Expense, file_path): # As a string it is written into a specified file

	print(f"Storing Expense in {file_path}...")

	with open(file_path, "a") as file:
		file.write(f"{expense.desc},{expense.amount},{expense.category},{expense.date_of_expense}\n")
	
def show_expenses(file_path): # Each expense user has input into a file is shown with this
	
	expenses = []

	with open(file_path, "r") as file:
		lines = file.readlines()
		for line in lines:
			expense_desc, expense_amount, expense_category, expense_date = line.strip().split(",")

			line_expense = Expense(expense_desc, float(expense_amount), expense_category, expense_date)

			expenses.append(line_expense)

	for line_expense in expenses:
		print(f"{line_expense}\n")
	
def predict(file_path): # very simple predictions are made after reading a specific file stored in various dictionaries to then be displayed to the user in meaningful ways

	expense_dict = {}

	total_amounts = {}

	predictions = {}

	month_counter = 0

	latest_month = 0

	with open(file_path, "r") as file:
		lines = file.readlines()

		for line in lines:
			expense_desc, expense_amount, expense_category, expense_date = line.strip().split(",")
			
			month = expense_date.split("-")[0]
			
			if month in expense_dict:
				if expense_category in expense_dict[month]:
					expense_dict[month][expense_category] += float(expense_amount)
				else:
					expense_dict[month][expense_category] = float(expense_amount)
			else:
				expense_dict[month] = {expense_category: float(expense_amount)}
				month_counter += 1

	print(f"We have data for {month_counter} Months\n")
	
	print(f"This is the Expense Data for the Past 3 Months in Data:\n")
	for month_key, values in expense_dict.items():
		if int(month_key) > latest_month:
			latest_month = int(month_key)

		values = dict(sorted(values.items()))

		if int(month_key) <= latest_month and int(month_key) > latest_month - 2:
			print(f"{month_key} - {values}\n")
			for value_category, value_amount in values.items():
				if value_category in total_amounts:
					total_amounts[value_category] += value_amount
				else:
					total_amounts[value_category] = value_amount

	for category, total_amount in total_amounts.items():
		predictions[category] = total_amount / 3
		predictions[category] = round(predictions[category], 1)

	print(f"Predictions for Next Month (Using Simple Moving Average):\n")
	for category, prediction_amount in predictions.items():
		print(f"{category} - {prediction_amount}\n")

	print(f"Would you like to see Visualisations of your data?")
	print(f"1. Yes")
	print(f"2. No\n")
	see_choice = int(input())

	if see_choice == 1:
		print(f"Here is the Visualisation based on your data for the Past 3 Months")
		tot_categories = list(total_amounts.keys())
		tot_amounts = list(total_amounts.values())

		plt.bar(range(len(total_amounts)), tot_amounts, tick_label=tot_categories)
		plt.show()

		print(f"Here is the Visualisation of the Predictions for Next Month")
		pred_categories = list(predictions.keys())
		predictions_amounts = list(predictions.values())

		plt.bar(range(len(predictions)), predictions_amounts, tick_label=pred_categories)
		plt.show()

	elif see_choice == 2:
		exit
	
	else:
	 	raise TypeError("Invalid Choice. Choose either 0 for Yes or 1 for No")
	
def savings_plan(savings_goal, file_path): # give users recommendations based on data, not fully fleshed out and gives very general "advice" but still takes in a savings goal

	expense_dict = {}

	total_amounts = {}

	predictions = {}

	month_counter = 0

	latest_month = 0

	with open(file_path, "r") as file:
		lines = file.readlines()

		for line in lines:
			expense_desc, expense_amount, expense_category, expense_date = line.strip().split(",")
			
			month = expense_date.split("-")[0]
			
			if month in expense_dict:
				if expense_category in expense_dict[month]:
					expense_dict[month][expense_category] += float(expense_amount)
				else:
					expense_dict[month][expense_category] = float(expense_amount)
			else:
				expense_dict[month] = {expense_category: float(expense_amount)}
				month_counter += 1

	print(f"We have data for {month_counter} Months\n")
	
	print(f"This is the Total Amount spent over the Past 3 Months:\n")
	for month_key, values in expense_dict.items():
		if int(month_key) > latest_month:
			latest_month = int(month_key)

		values = dict(sorted(values.items()))

		if int(month_key) <= latest_month and int(month_key) > latest_month - 2:
			for value_category, value_amount in values.items():
				if value_category in total_amounts:
					total_amounts[value_category] += value_amount
				else:
					total_amounts[value_category] = value_amount

	for category, tot_amount in total_amounts.items():
		print(f"{category} - {tot_amount}\n")

	for category, total_amount in total_amounts.items():
		predictions[category] = total_amount / 3
		predictions[category] = round(predictions[category], 1)

	print(f"Predictions for Next Month (Using Simple Moving Average):\n")
	for category, prediction_amount in predictions.items():
		print(f"{category} - {prediction_amount}\n")

	user_budget = int(input(f"What is your current budget?\n"))

	print(f"Here are some general recommendations based on your data:\n")
	for category, tot_amount in total_amounts.items():
		if category == "Entertainment" and tot_amount > 1000:
			print(f"- Consider cutting back on your purchases in Entertainment. Life is short.\n")

		if category == "Food & Drinks" and tot_amount > 5000:
			print(f"- Plan out your meals more accordingly. Maybe you should go see a doctor\n")

		if category == "General Purchases" and tot_amount > 2000:
			print(f"- Please think about your spending habits and budget. ")

		if category == "Living Expenses" and tot_amount > 100000:
			print(f"- Maybe you should start thinking about moving")

		if category == "Other" and tot_amount > 10000:
			print(f"- Go sit in a corner and think about how much you've spent right now")
		
		else:
			print(f"We don't have any recommendations for you at the moment")



def main(): # main function which contains what is visibly seen on the command line interface, while true loop keeps program running unless an error is raised

	while True:

		print(f"Welcome to the Python Expense Tracker")
		print(f"1. Enter an Expense")
		print(f"2. Show Expenses")
		print(f"3. Predict Expenses for Next Month")
		print(f"4. Savings Plan\n")

		user_choice = int(input("Please choose a number to proceed:\n"))

		if user_choice == 1:
  		# User Input Section
			print(f"You have chosen \"Enter an Expense\"\n")
			print(f"Where would you like to enter the expense?...")
			print(f"1. Create New File")
			print(f"2. Enter into Existing File")

			enter_choice = int(input())
			print('\n')

			if enter_choice == 1:

				user_name = input("Tell me your Name:\n")

				expense_year = int(input("Enter the Year of your Expenses (YYYY):\n"))
				if expense_year < 2000 or expense_year > 2099:
					raise ValueError (f"Invalid Year Entered.\n")

				file_path = f"{user_name}_{expense_year}_expenses.csv"
		
				new_expense = user_input(expense_year)
				print(f"Expense Successfully Entered \n")

				store_data(new_expense, file_path)
				print(f"New Expense File Created\n")

			elif enter_choice == 2:
				csv_files = glob.glob("*.csv")

				csv_file_list = []

				for i, csv_file in enumerate(csv_files, start=1):
					csv_file_list.append(csv_file)
					print(f"{i}. {csv_file}\n")
			
				if len(csv_file_list) == 0:
					print(f"No Expense Files in Directory")
					exit

				else:
					file_choice = int(input(f"Which file would you like to enter to?\n"))

					if file_choice in range(len(csv_file_list) + 1):
						file_path = csv_file_list[file_choice - 1]

						user_name, expenses_year, notimportant = file_path.split("_")
						
						new_expense = user_input(expenses_year)
						print(f"Expense Successfully Entered\n")

						store_data(new_expense, file_path)
						print(f"Expense Stored\n")

					else:
						raise ValueError(f"Invalid Choice. Please choose a file number shown")

		elif user_choice == 2:
			# Show Expenses Section
			print(f"You have chosen \"Show Expenses\"\n")

			csv_files = glob.glob("*.csv")

			csv_file_list = []

			for i, csv_file in enumerate(csv_files, start=1):
				csv_file_list.append(csv_file)
				print(f"{i}. {csv_file}\n")
			
			if len(csv_file_list) == 0:
				print(f"No Expense Files in Directory")
				exit

			else:
				file_choice = int(input(f"Which file would you like to view?\n"))

				if file_choice in range(len(csv_file_list) + 1):
					file_path = csv_file_list[file_choice - 1]
					show_expenses(file_path)

				else:
					raise ValueError(f"Invalid Choice. Please choose a file number shown")
				
		elif user_choice == 3:
			#Prediction Section
			print(f"You have chosen \"Predict Expenses for Next Month\"\n")

			csv_files = glob.glob("*.csv")

			csv_file_list = []

			for index, csv_file in enumerate(csv_files, start=1):
				csv_file_list.append(csv_file)
				print(f"{index}. {csv_file}\n")
			
			if len(csv_file_list) == 0:
				print(f"No Expense Files in Directory")
				exit

			else:
				file_choice = int(input(f"Which file would you like to run the prediction on?\n"))

				if file_choice in range(len(csv_file_list) + 1):
					file_path = csv_file_list[file_choice - 1]
					predict(file_path)

		elif user_choice == 4:
			#Saving Plan Section
			print(f"You have chosen \"Savings Plan\"\n")

			savings_goal = int(input(f"What is your savings goal for next month?\n"))

			csv_files = glob.glob("*.csv")

			csv_file_list = []

			for index, csv_file in enumerate(csv_files, start=1):
				csv_file_list.append(csv_file)
				print(f"{index}. {csv_file}\n")
			
			if len(csv_file_list) == 0:
				print(f"No Expense Files in Directory")
				exit

			else:
				file_choice = int(input(f"Which file would you like recommendations for?\n"))

				if file_choice in range(len(csv_file_list) + 1):
					file_path = csv_file_list[file_choice - 1]
					savings_plan(savings_goal, file_path)

		else:
			raise ValueError("Invalid choice. Please pick a number from 1 - 4.\n")
		


main() # calling of that main function to run program