from DatabaseManager import DatabaseManager
import time

"""This class provides methods for easy database operations
"""


class CrudOperations(object):
    dbmgr = None

    def __init__(self):  # constructor initiates database connection instance
        self.dbmgr = DatabaseManager("cmapp.db")

        """Performs insert in db to save a notetext
        """

    def save(self, **content):  # content contains the name and mobile number of contacts
        contactname = ""
        contactnumber = ""
        if len(content) == 2:
            # Both name and mobile number exist
            contactname = content['contactname']
            contactnumber = content['contactnumber']
        elif len(content) == 1:  # only title exists
            return "Cannot save to db only one argument provided , two are expected"
        # save to db
        self.dbmgr.query(
            "insert into contactsDB(Contactname,Content,sent,datecreated) VALUES('" + contactname + "','" + contactnumber + "','NO','" + self.gettime() + "')")

