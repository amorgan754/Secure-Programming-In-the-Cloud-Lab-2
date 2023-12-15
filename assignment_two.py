"""This program is to demonstrate the capabilities to modify in dynamodb"""

#imports
import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key

#database resource
dynamodb = boto3.resource("dynamodb")

#region
REGION = "us-east-1"

#create table
def create_table():
    """This function is to create the table"""
    table_creation = dynamodb.create_table(
        TableName="Courses",
        KeySchema=[
            {
                "AttributeName": "CatalogNbr",
                "KeyType": "HASH"
            },

            {
                "AttributeName": "Subject",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "CatalogNbr",
                "AttributeType": "N"
            },
            {
                "AttributeName": "Subject",
                "AttributeType": "S"
            }
            ],
        ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10
            }
        )
    
#create_table()

table = dynamodb.Table("Courses")

#functions

#validate the subject
def subject_check():
    """This function is to validate subject input"""
    subject_input = input("Please select a subject: \n")
    while len(subject_input) != 4:
        print("Incorrect format.")
        print()
        subject_input = input("Please select a subject: \n")
    return subject_input

#validate the catalog number
def number_check():
    """This function is to validate course input"""
    course_input = input("Please enter a catalog number: \n")
    while len(course_input) != 3:
        print("Incorrect format.")
        print()
        course_input = input("Please enter a catalog number: \n")
    return int(course_input)


#table inputs
def table_inputs():
    """This function is to input the data"""
    with open("courses_data.json") as json_file:
        courses = json.load(json_file, parse_float = decimal.Decimal)
        for class_data in courses:
            class_subject = class_data['Subject']
            class_catalog_nbr = int(class_data['CatalogNbr'])
            class_title = class_data['Title']
            number_credits = class_data['NumCredits']

            table.put_item(
                Item={
                    'Subject': class_subject,
                    'CatalogNbr' : class_catalog_nbr,
                    'Title': class_title,
                    'NumCredits': number_credits
                }
            )


#search for title with subject and catalog number
def search_table(class_subject, catalog_number):
    """This function searches for the table information"""
    response = table.query(
        KeyConditionExpression=Key('Subject').eq(class_subject)
            & Key('CatalogNbr').eq(catalog_number)
    )

    for i in response['Items']:
        print("Subject: ", i['Subject'])
        print("Catalog Number: ", i['CatalogNbr'])
        print("Title: ", i['Title'])
        print("Number of Credits: ", i['NumCredits'])


table_inputs()

CHOICE = None

while CHOICE != "n":
    subject = subject_check()
    subject = subject.upper()
    catalog_nbr = number_check()
    CATALOG_NBR = int(catalog_nbr)
    print()
    search_table(subject, catalog_nbr)
    print()
    CHOICE = input("Would you like to continue? Y or N: \n")
    CHOICE = CHOICE.lower()
    print()

    if CHOICE == "n":
        print("Thank you for using the program")
