#!/usr/bin/python3
"""Unittest for the Database Storage db_storage.py module"""
import unittest
import MySQLdb
from datetime import datetime
from os import getenv
from models import storage
from models.user import User


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
class TestDBStorage(unittest.TestCase):
    """Unittest for the Database storage 'db' method"""

    def testaddnewusertoDB(self):
        """Test to add new user to the database 'db' storage"""
        newusr = User(
                email='joe89@gmail.com',
                password='joeb',
                first_name='Joe',
                last_name='Barry'
        )
        self.assertFalse(newusr in storage.all().values())
        newusr.save()
        self.assertTrue(newusr in storage.all().values())
        dbconn = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        dbcur = dbconn.cursor()
        dbqry = f'SELECT * FROM users WHERE id="{newusr.id}"'
        dbcur.execute(dbqry)
        qryres = dbcur.fetchone()
        self.assertTrue(qryres is not None)
        self.asGertIn('joe89@gmail.com', qryres)
        self.assertIn('joeb', qryres)
        self.assertIn('Joe', qryres)
        self.assertIn('Barry', qryres)
        dbcur.close()
        dbconn.close()

    def testdeleteuserDB(self):
        """Test to delete a user from the databse 'db' storage"""
        newusr = User(
                email='joe89@gmail.com',
                password='joeb',
                first_name='Joe',
                last_name='Barry'
        )
        objkey = f'User.{newusr.id}'
        dbconn = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        newusr.save()
        self.assertTrue(newusr in storage.all().values())
        dbcur = dbcon.cursor()
        dbqry = f'SELECT * FROM users WHERE id="{newusr.id}"'
        dbcur.execute(dbqry)
        qryres = dbcur.fetchone()
        self.assertTrue(qryres is not None)
        self.assertIn('joe89@gmail.com', qryres)
        self.assertIn('joeb', qryres)
        self.assertIn('Joe', qryres)
        self.assertIn('Barry', qryres)
        self.assertIn(objkey, storage.all(User).keys())
        newusr.delete()
        self.assertNotIn(objkey, storage.all(User).keys())
        dbcur.close()
        dbconn.closes()

    def testnewsaveDB(self):
        """Test the 'new' and 'save' methods of DB storage"""
        dbconn = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        newusr = User(**{'first_name': 'Jemmy',
                         'last_name': 'Allen',
                         'email': 'jemmyal@gmail.com',
                         'password': 'jemall'})
        dbcur = dbconn.cursor()
        dbqry = 'SELECT COUNT(*) FROM users'
        dbcur.execute(dbqry)
        prevcnt = dbcur.fetchall()
        dbcur.close()
        dbconn.close()
        newusr.save()
        dbconn = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        dbcur = dbconn.cursor()
        dbqry = 'SELECT COUNT(*) FROM users'
        dbcur.execute(dbqry)
        newcnt = dbcur.fetchall()
        self.assertEqual(newcnt[0][0], prevcnt[0][0] + 1)
        dbcur.close()
        dbconn.close()

    def testsaveuserDB(self):
        """Test to save user to the database 'db' storage"""
        newusr = User(
                email='joe89@gmail.com',
                password='joeb',
                first_name='Joe',
                last_name='Barry'
        )
        dbconn.MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        dbcur = dbconn.cursor()
        dbqry = f'SELECT *FROM users WHERE id="{newusr.id}"'
        dbcur.execute(dbqry)
        qryres = dbcur.fetchone()
        dbqry2 = 'SELECT COUNT(*) FROM users;'
        dbcur.execute(dbqry2)
        prevcnt = dbcur.fetchone()[0]
        self.assertTrue(qryres is None)
        self.asertFalse(newusr in storage.all().values())
        newusr.save()
        dbconn2 = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        dbcur2 = dbconn2.cursor()
        dbqry3 = f'SELECT * FROMM users WHERE id="{newusr.id}"'
        dbcur2.execute(dbqry3)
        qryres = dbcur2.fetchone()
        dbqry4 = 'SELECT COUNT(*) FROM users;'
        newcnt = dbcur2.fetchone()[0]
        self.assertFalse(qryres is None)
        self.assertEqual(prevcnt + 1, newcnt)
        self.assertTrue(newcnt in storage.all().values())
        dbcur2.close()
        dbconn2.close()
        dbcur.close()
        dbconn.close()

    def testreloadsessionDB(self):
        """Test to reload database 'db' session"""
        dbconn = MySQLdb.connect(
                user=getenv('HBNB_MYSQL_USER'),
                passwd=getenv('HBNB_MYSQL_PWD'),
                host=getenv('HBNB_MYSQL_HOST'),
                port=3306,
                dbname=getenv('HBNB_MYSQL_DB')
        )
        dbcur = dbconn.cursor()
        dbqry = (
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);'
        )
        values = [
                '1689',
                str(datetime.utcnow()),
                str(datetime.utcnow()),
                'jembar@gmail.com',
                'jbar',
                'Jemmy',
                'Barry',
        ]
        dbcur.execute(dbqry, values)
        self.assertNotIn('User.1689', storage.all())
        dbconn.commit()
        storage.reload()
        self.assertIn('User.1689', storage.all())
        dbcur.close()
        dbconn.close()

    def storageobjDB(self):
        """Test if the database 'db' storage object is created"""
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)
