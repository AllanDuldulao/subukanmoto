# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using dictionaries, files, and exception handling and adds the use of functions
#       classes, and using the separation of concern pattern
# Change Log: (Who, When, What)
# ADuldulao, 5/21/2025, Created Script
# ADuldulao, 5/23/2025, Created class and static method
# ADuldulao, 5/24/2025, Worked on editing and cleaning the script. Added DocStrings

# ------------------------------------------------------------------------------------------ #
import json


#---Data-------------------------------------------------------------------------------------#
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"
MENU: str = '''
---- Course Registration Program -------------
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------------
'''
# Define Data Variables
students: list = []  # a table of student data
menu_choice: str = ''  # Hold the choice made by the user.

# TODO Create a Person Class
class Person:
    """
      A class representing person data.

    """

# TODO Add first_name and last_name properties to the constructor
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

# TODO Create a getter and setter for the first_name property
    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.replace(" ", "").isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

# TODO Create a getter and setter for the last_name property
    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.replace(" ", "").isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The first last should not contain numbers.")
    # TODO Override the __str__() method to return Person data
    def __str__(self):
        return f'{self.first_name},{self.last_name}'

# TODO Create a Student class the inherits from the Person class
class Student(Person):
    """
      A class representing student data.

      Properties:
          first_name (str): The student's first name.
          last_name (str): The student's last name.
          gpa (float): The gpa of the student.

      ChangeLog: (Who, When, What)

      """

    # TODO call to the Person constructor and pass it the first_name and last_name data
    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.__course_name = course_name

    @property
    def course_name(self):
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value
    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'







#---Processing------------------------------------------------------------------------------#
class FileProcessor:
    """
    A collection of layer functions that work with Json file
    When the program starts, read the file data into a list of lists (table)
    Extract the data from the file
    ChangeLog: (Who, When, What)
    ADuldulao, 5/24/2025, Created class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function attempts to open and read a JSON file, parse its contents into a list,
        and return the list. It handles errors such as missing files or invalid JSON file format
        and print appropriate error message.
        :param file_name: string data with name of file to read from
        :return: list
         ChangeLog: (Who, When, What)
    ADuldulao, 5/24/2025, Created function
        """
        file = None
        try:
            file = open(file_name, 'r')

            #student_data = json.load(file)
            list_of_dictionary_data = json.load(file)

            for student_dict in list_of_dictionary_data:
                student_object: Student = Student(first_name=student_dict["FirstName"],
                                                  last_name=student_dict["LastName"],
                                                  course_name=student_dict["CourseName"])
                student_data.append(student_object)
            file.close()

        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
            print("To prevent confusion. PRESS 4 TO EXIT IMMEDIATELY!!!")
        except Exception as e:
            IO.output_error_messages("Please check that the data is a valid JSON format!", e)
            print(e)
            print("To prevent confusion. PRESS 4 TO EXIT IMMEDIATELY!!!")
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This functions writes a list to specified file in JSON format.
        It handles errors such as invalid JSON data or other issues.
        It will show the current student is being saved in the list.
        :param file_name: string data with name of file to read from
        :return: list
         ChangeLog: (Who, When, What)
    ADuldulao, 5/24/2025, Created Function
        """
        file = None
        try:

            list_of_dictionary_data: list = []

            for student in student_data:
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name,
                       "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)
            file = open(file_name, "w")

            json.dump(list_of_dictionary_data, file, indent=1)  # Added the indent so that my datas are easily readable.
            file.close()
            if student_data:
               current_student = student_data[-1]
               print("The following student was added to list!")
               print(f'Student {current_student.first_name} '
                        f'{current_student.last_name} is enrolled in {current_student.course_name}')
        except TypeError as e:
            IO.output_error_messages("Please make sure that the data is a valid JSON format!\n", e)
        except Exception as e:
            IO.output_error_messages("\nThere was a non-specific error!\n", e)
        finally:
            if file is not None and not file.closed:
                file.close()
#---Presentation----------------------------------------------------------------------------------------------#
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog:(Who, When, What)
    ADuldulao, 5/24/2025, Created Clas
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This Function displays that a custom error messages to the user
        ChangLog: (Who,When,What)
        ADuldulao, 5/23/2025
        :param message: spring with message data to display
        :param error: Exception object with technical message to display
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-----Technical Error Message------")
            print(error, error.__doc__, type(error), sep='\n')
    @staticmethod
    def output_menu(menu: str):
        """
        This function displays that a menu of choice to the user
        :return: None
        """
        print(menu)
    @staticmethod
    def input_menu_choice():
        """
        This function gets a menu choice from the user
        :return: string with the user choice
         ChangeLog: (Who, When, What)
         ADuldulao, 5/24/2025, Created Function
        """
        choice = "0"
        try:
            choice = input("What would you like to do: \n")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice
    @staticmethod
    def input_student_data(student_data: list):
        """
        This function gets to User first name, last name, and course name.
        This function will produce an error if user enter a number.
        :param student_data: list of dictionary rows to be filled with input data
        :return: list
         ChangeLog: (Who, When, What)
         ADuldulao, 5/24/2025, Created Function
        """
        try:
            #student_first_name = input("Enter the student's first name: \n")
            #if not student_first_name.replace(" ", "").isalpha():
            #    raise ValueError("The first name should not contain numbers.")
            #student_last_name = input("Enter the student's last name: \n")
            #if not student_last_name.replace(" ", "").isalpha():
            #    raise ValueError("The last name should not contain numbers.")
            #course_name = input("Please enter the name of the course: \n")
            #student = Student(first_name=student_first_name, last_name=student_last_name,
            #                  course_name=course_name)
            student = Student()
            student.first_name = input("What is the student's first name? \n")
            student.last_name = input("What is the student's last name? \n")
            student.course_name = input("Please enter the name of the course: \n")
            student_data.append(student)
            #print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return students
    @staticmethod
    def output_student_courses(student_data: list):
        """
        This function displays the list of registered students and courses. It will display a string
        of comma-separated values for each row collected in the students variable
        :return: None
         ChangeLog: (Who, When, What)
         ADuldulao, 5/24/2025, Created Function
        """
        print("The current registration data: ")
        print("-" * 47)
        for student in student_data:
            message = "{},{},{}"
            print(message.format(student.first_name, student.last_name, student.course_name))
        print("-" * 47)
        print()
#---Beginning of the main body of the script-----------------------------------------------------------#
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)
#---Present and Process the Data-----------------------------------------------------------------------#
while (True):
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()
    # Present the menu of choices    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue
        # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        # Process the data to create and display a custom message
        continue
    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue
    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please select only 1,2, and 3. Select 4 to exit")
        continue
print("Program Ended")
