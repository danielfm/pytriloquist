import os

import e32db

class DBManager(object):
    """Class to abstract the use of the e32db module.
    """
    def __init__(self, db_file):
        """Initializes a new instance.
        """
        self.db = e32db.Dbms()
        self.db_file = db_file

    def open_or_create(self):
        """Opens or creates the database file.
        """
        if os.path.exists(self.db_file):
            self.db.open(self.db_file)
        else:
            self.db.create(self.db_file)
            self.db.open(self.db_file)
            return True

    def close(self):
        """Closes the database.
        """
        self.db.close()

    def execute(self, sql):
        """Executes an update SQL.
        """
        return self.db.execute(sql)

    def execute_atomic(self, sqls):
        """Executes several update SQLs inside a transaction.
        """
        ret = []
        try:
            self.db.begin()
            for sql in sqls:
                ret.append(self.execute(sql))
            self.db.commit()
        except:
            self.db.rollback()
            return None
        return ret

    def query(self, sql):
        """Executes a query.
        """
        view = e32db.Db_view()
        view.prepare(self.db, sql)
        return view
