import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from subprocess import Popen, PIPE, DEVNULL
import time
import signal
import os


class AppPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.app = Popen("export FLASK_APP=app.py; env/bin/python -m flask run", stdin=PIPE, stdout=DEVNULL, shell=True, preexec_fn=os.setsid)
        time.sleep(.5)

    def tearDown(self):
        self.driver.close()
        os.killpg(os.getpgid(self.app.pid), signal.SIGINT)

    def test_page(self):
        self.driver.get("localhost:5000")
        self.assertIn("Hello World", self.driver.find_element(By.TAG_NAME, "body").text)

class AppApiTest(unittest.TestCase):
    def setUp(self):
        self.app = Popen("export FLASK_APP=app.py; env/bin/python -m flask run", stdin=PIPE, stdout=DEVNULL, shell=True, preexec_fn=os.setsid)
        time.sleep(.5)

    def tearDown(self):
        os.killpg(os.getpgid(self.app.pid), signal.SIGINT)

    def test_get_api_returns_200(self):
        resp = requests.get('http://localhost:5000/api.json')
        self.assertEqual(resp.status_code, 200)

    def test_get_api_returns_returns_the_right_value(self):
        resp = requests.get('http://localhost:5000/api.json')
        self.assertEqual(resp.json(), {"value": "Hello World"})
