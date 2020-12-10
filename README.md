******************\*******************CAR RENTAL SYSTEM**********\*\***********



Required Packages To Install:

1. Python 3.7.x - you can download it from https://www.python.org/downloads/release/python-374/
   Add following to path in system variables
   {your installation directory}\Python\Python37\
   {your installation directory}\Python\Python37\scripts

2. Django.
   -> goto open terminal in project folder and type: pip install django
   Note : django to be installed only after installing python

3. Selenium WebDriver.
   -> goto open terminal in project folder and type: pip install selenium
   Note : selenium to be installed only after installing python and django ; set python to the path.

4. webdriver_manager.
   -> goto open terminal in project folder and type: pip install webdriver_manager
   Note: webdriver_manager to be installed only after installing python,django and selenium.

5. PyCharm Ultimate Version. (Ultimate Version supports Django, Community Does not).

6. pip install pysimplegui

Note: JetBrains give one year ultimate version license to students for free, register with your student ENCS email id

Steps to run project :

1. Open Pycharm Ultimate Version.
2. Checkout the latest version of the project from the GIT repository.
3. Build the project , after installing all dependencies.
4. Admin Credentials
   Username : admin
   Password : admin
5. Clerk Credentials
   Username : clerk
   Password : clerk

Command to run the project from terminal - python manage.py runserver 4. You will see localhost server address on the console (window named : run)inside pyCharm : Open browser and use the localhost address to run the application. 5. For convenience and development,
clerk username : b
Password : b
you can test with these credentials for the clerk.

---

As an addition part,
For this first iteration we have introduced a Selenium Automated Web Test Framework module, which runs the UI tests (for Admin Module only ) and then generates a reports of UI passed/ failed tests.
Steps for running:

---

1. Start the application by running the server following "Steps A".
2. open the command prompt terminal in the project folder and type
   -python manage.py test
3. Results are stored as csv reports as of now in File -> UITest_file.csv

---
