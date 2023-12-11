import certifi as certifi
import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """

    valid_department = False
    collection = db["departments"]
    while not valid_department:
        # Create a "pointer" to the students collection within the db database.
        # unique_name: bool = False
        # unique_abbreviation: bool = False
        # unique_chair_name: bool = False
        # unique_building_office: bool = False
        # unique_description: bool = False

        name: str = ''
        abbreviation: str = ''
        chair_name: str = ''
        building: str = ''
        office: int = 0
        description: str = ''

        # while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        # name_count: int = collection.count_documents({"name": name})
        # unique_name = name_count == 0
        # if not unique_name:
        #    print("We already have a department by that name.  Try again.")

        # if unique_name:
        #    abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
        #    unique_abbreviation = abbreviation_count == 0
        #    if not unique_abbreviation:
        #        print("We already have a department with that abbreviation.  Try again.")
        # while not unique_chair_name:
        chair_name = input("Department chair name--> ")
        # chair_name_count = collection.count_documents({"chair_name": chair_name})
        # unique_chair_name = chair_name_count == 0
        # if not unique_chair_name:
        #    print("We already have a department with that chair name. Try again.")

        # while not unique_building_office:
        building = input("Department building--> ")
        office = int(input("Department Office--> "))
        # building_office_count: int = collection.count_documents({"building": building, "office": office})
        # unique_building_office = building_office_count == 0
        # if not unique_building_office:
        #    print("We already have a department by that office in that building. Try again.")

        # while not unique_description:
        description = input("Department description--> ")
        # description_count: int = collection.count_documents({"description": description})
        # unique_description = description_count == 0
        # if not unique_description:
        #    print("We already have a department by that description. Try again.")

        # Build a new departments document preparatory to storing it
        department = {
            "name": name,
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description
        }
        try:
            collection.insert_one(department)
            valid_department = True
        except Exception as exception:
            print("We got the following exception from a bad input:")
            print(exception)
            print("Please re-enter your values")


def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    name: str = ''
    abbreviation: str = ''
    while not found:
        name = input("Department's name--> ")
        abbreviation = input("Department's abbreviation--> ")
        name_count: int = collection.count_documents({"name": name, "abbreviation": abbreviation})
        found = name_count == 1
        if not found:
            print("No department found by that name and abbreviation.  Try again.")
    found_department = collection.find_one({"name": name, "abbreviation": abbreviation})
    return found_department


def delete_department(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING),
                                                   ("abbreviation", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->') or "Cathrina1976"
    username: str = input('Database username [shaunlim] -->') or \
                    "shaunlim"
    project: str = input('Mongo project name [cecs-323-fall] -->') or \
                   "cecs-323-fall"
    hash_name: str = input('7-character database hash [44qveqy] -->') or "44qveqy"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster, tlsCAFile=certifi.where())

    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.

    # ************************** Set up the students collection
    department_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': 'the basic administrative unit within the University organized to carry on and develop'
                               ' the instructional and research activities of its faculty.',
                'required': ["name", "abbreviation", "chair_name", "building", "office", "description"],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'name': {
                        'bsonType': "string",
                        "minLength": 10,
                        "maxLength": 50,
                        'description': "The label that identifies a singular department."
                    },
                    'abbreviation': {
                        'bsonType': "string",
                        "minLength": 1,
                        "maxLength": 6,
                        'description': "A shortened string that identifies a singular department"
                    },
                    'chair_name': {
                        'bsonType': "string",
                        "minLength": 1,
                        "maxLength": 80,
                        'description': "The person who is in charge of the department"
                    },
                    'building': {
                        'enum': ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"],
                        'description': "The string name of the structure the head office of the department will be"
                    },
                    'office': {
                        'bsonType': "int",
                        'minimum': 1,
                        'description': "An integer identifying the room the head office of"
                                       " the department will be"
                    },
                    'description': {
                        'bsonType': "string",
                        "minLength": 10,
                        "maxLength": 80,
                        'description': "A sentence describing the department"
                    },
                }
            }

        }
    }

    db.create_collection("departments", **department_validator)
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Students in the collection so far: {department_count}")
    departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviations")
    departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_names')
    departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                             unique=True, name="departments_buildings_and_offices")
    departments.create_index([('name', pymongo.ASCENDING)], unique=True, name="departments_names")

    """
    departments_indexes = departments.index_information()
    if 'departments_abbreviations' in departments_indexes.keys():
        print("abbreviation index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviations")

    if 'departments_chair_names' in departments_indexes.keys():
        print("chair name index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_names')

    if 'departments_buildings_and_offices' in departments_indexes.keys():
        print("building and office index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True, name="departments_buildings_and_offices")

    if 'departments_descriptions' in departments_indexes.keys():
        print("description index present.")
    else:
        departments.create_index([('description', pymongo.ASCENDING)], unique=True, name="departments_descriptions")
    """
    # pprint(departments.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
