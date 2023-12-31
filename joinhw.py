import pymongo
from pymongo import MongoClient
import certifi as certifi

#create the connection string
connect = 'mongodb+srv://shaunlim:Cathrina1976@cecs-323-fall.44qveqy.mongodb.net/?retryWrites=true&w=majority' # your connection string from Atlas with your password goes here.
# create the connection to the MongoDB cluster in Atlas.
db=MongoClient(connect, tlsCAFile=certifi.where())
# create a reference to the Demonstration database within your cluster
demo = db["Demonstration"]
# make a reference to the departments collection in the Demonstration database.
depts = demo["departments"]
# make a reference to the courses collection in the Demonstration database.
crses = demo["courses"]
# set up a dict with two department's definitions.
departments=[
    {
        "name": "Computer Engineering Computer Science",
        "abbreviation": "CECS",
        "chair_name": "Mehrdad Aliasgari",
        "building": "ECS",
        "office": 526,
        "description": "All things computer"
    },
    {
        "name": "Chemical Engineering",
        "abbreviation": "CHE",
        "chair_name": "Roger C. Lo",
        "building": "EN2",
        "office": 101,
        "description": "Finding new ways to make the world better chemically"}
]
# Insert our new departments.
depts.insert_many(departments)
# define a little utility to pretty print iterables.
from pprint import pprint
def pp(thing):
    for thingee in thing:
        pprint(thingee)
# define a little utility that maps from the department abbreviation to the _id value for that department
# interestingly enough, the ObjectID wrapper is unnecessary.
def dept_id(abbreviation: str):
    # honestly, the project is gratuitous since I just ask for
    # the _id from the resulting dict.
    return depts.find_one({"abbreviation": abbreviation}, {"_id": 1})["_id"]
# define two courses in the CECS department
courses = [
    {
        "department": dept_id("CECS"),
        "course_number": 323,
        "course_name": "Database Design Fundamentals",
        "description": "Relational & NoSQL design",
        "units": 3
    },
    {
        "department": dept_id("CECS"),
        "course_number": 274,
        "course_name": "Data Structures",
        "description": "Using basic data structures to solve problems in Object Oriented Python programming",
        "units": 3
     }
]
crses.insert_many(courses)
# Do a "join from Department to Course using the
# "migrating foreign key" of _id in
# Department that "migrates" down into Course.
pp(depts.aggregate(
    [
        {"$lookup":
            {
                "from": "courses",
                "localField": "_id",
                "foreignField": "department",
                "as": "courses"
            }
        }
    ]
))
# This time, I'm going to fake an inner join. The above query returns
# all the departments, regardless whether they have any course or not.
# This is a bit ghetto, but it works:
"""
pp(depts.aggregate(
    [
        {"$lookup":
            {
                "from": "courses",
                "localField": "_id",
                "foreignField": "department",
                "as": "courses"
            }
        },
        {"$match": {"courses": {"$exists": True, "$type": 'array', "$not":{"$size": 0}}}}
    ]
))
# The above represents some defensive programming. courses
# is manufactured by the $lookup pipeline stage, so it should
# always be present, and should always be an array, but just
# because MongoDB is so casual about typing (what a match
# for Python!), I figured it would not hurt to have it here.
# The $size returns the length of the array.
# There is a certain economy to this last aggregation just
# because we only display the department data once.
# But I've not found a successful way to sort the array so that
# we can control the order of the course elements within
# the department collection items that get returned.
# The way to do that is to turn the join on its head:
pp(crses.aggregate(
    [
        {"$sort":
            {"course_number": 1}
        },
        {"$lookup":
            {
                "from": "departments",
                "localField": "department",
                "foreignField": "_id",
                "as": "department"
            }
        },
        {"$match":
            {"department":
                {"$exists": True, "$type": 'array', "$not":
                    {"$size": 0}
                }
            }
        },
    ]
))
# In the above, we start the join with the courses
# collection, sort that collection, then join it
# to departments to get the department information
# for each course. Just remember that the dict
# that MongoDB returns is not an ADT at all. To get that,
# we would need to use an ODM.
"""
