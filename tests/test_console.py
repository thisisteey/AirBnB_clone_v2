#!/usr/bin/python3
"""Unittest module for console.py (command interpreter) is defined"""
import unittest
import json
import MySQLdb
import models
from models import storage
from unittest.mock import patch
from os import getenv
from sqlalchemy.exc import OperationalError
from io import StringIO
from console import HBNBCommand
from tests.__init__ import clearfilecontents


class TestHBNBCommand(unittest.TestCase):
    """Unittest for the HBNBCommand class"""
    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def testcreateFS(self):
        """test 'create' command with the FileStorage"""
        with patch('sys.stdout', new=StringIO()) as result:
            cmdinterp = HBNBCommand()
            cmdinterp.onecmd('create City name="Maryland"')
            expmsg = result.getvalue().strip()
            clearfilecontents(result)
            self.assertIn(f'City.{expmsg}', storage.all().keys())
            cmdinterp.onecmd(f'show City {expmsg}')
            self.assertIn("'name': 'Maryland'", result.getvalue().strip())
            clearfilecontents(result)
            cmdinterp.onecmd('create User name="Joe" age=35 height=5.11')
            expmsg = result.getvalue().strip()
            self.assertIn(f'User.{expmsg}', storage.all().keys())
            clearfilecontents(result)
            cmdinterp.onecmd(f'show User {expmsg}')
            self.assertIn("'name': 'Joe'", result.getvalue().strip())
            self.assertIn("'age': 35", result.getvalue().strip())
            self.assertIn("'height': 5.11", result.getvalue().strip())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def testcreateDB(self):
        """test 'create' command with the Database Storage"""
        with patch('sys.stdout', new=StringIO()) as result:
            cmdinterp = HBNBCommand()
            with self.assertRaises(OperationalError):
                cmdinterp.onecmd('creatte User')
            clearfilecontents(result)
            cmdinterp.onecmd('create User email="joe89@go.com" password="j89"')
            expmsg = result.getvalue().strip()
            dbconn = MySQLdb.connect(
                    user=getenv('HBNB_MYSQL_USER'),
                    passwd=getenv('HBNB_MYSQL_PWD'),
                    host=getenv('HBNB_MYSQL_HOST'),
                    port=3306,
                    dbname=getenv('HBNB_MYSQL_DB')
            )
            dbcur = dbconn.cursor()
            dbqry = f'SELECT * FROM users WHERE id="{expmsg}"'
            dbcur.execute(dbqry)
            qryres = dbcur.fetchone()
            self.assertTrue(qryres is not None)
            self.assertIn('joe89@go.com', qryres)
            self.assertIn('j89', qryres)
            dbcur.close()
            dbconn.close()

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def testshowDB(self):
        """test 'show' command with the Database Storage"""
        with patch('sys.stdout', new=StringIO()) as res:
            cmdinterp = HBNBCommand()
            usrinst = User(email="joe89@gmail.com", password="j189")
            dbconn = MySQLdb.connect(
                    user=getenv('HBNB_MYSQL_USER'),
                    passwd=getenv('HBNB_MYSQL_PWD'),
                    host=getenv('HBNB_MYSQL_HOST'),
                    port=3306,
                    dbname=getenv('HBNB_MYSQL_DB')
            )
            dbcur = dbconn.cursor()
            dbqry = f'SELECT * FROM users WHERE id="{usrinst.id}"'
            dbcur.execute(dbqry)
            qryres = dbcur.fetchone()
            self.assertTrue(qryres is None)
            cmdinterp.onecmd(f'show User {usrinst.id}')
            self.assertEqual(res.getvalue().strip(), '** no instance found **')
            usrinst.save()
            dbconn = MySQLdb.connect(
                    user=getenv('HBNB_MYSQL_USER'),
                    passwd=getenv('HBNB_MYSQL_PWD'),
                    host=getenv('HBNB_MYSQL_HOST'),
                    port=3306,
                    dbname=getenv('HBNB_MYSQL_DB')
            )
            dbcur = dbconn.cursor()
            dbqry = f'SELECT * FROM users WHERE id="{usrinst.id}"'
            dbcur.execute(dbqry)
            clearfilecontents(res)
            cmdinterp.onecmd(f'show User {usrinst.id}')
            qryres = dbcur.fetchone()
            self.assertTrue(qryres is not None)
            self.assertIn('joe89@gmail.com', qryres)
            self.assertIn('j189', qryres)
            self.assertIn('joe89@gmail.com', res.getvalue())
            self.assertIn('j189', res.getvalue())
            dbcur.close()
            dbconn.close()

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def testcountDB(self):
        """test 'count' command with the Database Storage"""
        with patch('sys.stdout', new=StringI0()) as result:
            cmdinterp = HBNBCommand()
            dbconn = MySQLdb.connect(
                    user=getenv('HBNB_MYSQL_USER'),
                    passwd=getenv('HBNB_MYSQL_PWD'),
                    host=getenv('HBNB_MYSQL_HOST'),
                    port=3306,
                    dbname=getenv('HBNB_MYSQL_DB')
            )
            dbcur = dbconn.cursor()
            dbqry = f'SELECT COUNT(*) FROM states;'
            dbcur.execute(dbqry)
            qryres = dbcur.fetchone()
            prevcnt = int(qryres[0])
            cmdinterp.onecmd('create State name="Enugu"')
            clearfilecontents(result)
            cmdinterp('count State')
            newcnt = result.getvalue().strip()
            self.assertEqual(int(newcnt), prevcnt + 1)
            clearfilecontents(result)
            cmdinterp.onecmd('count State')
            dbcur.close()
            dbconn.close()
