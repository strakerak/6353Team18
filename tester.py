import requests
import json


#Testing if login page works:
print("Testing if login page is accessible")
response = requests.get('https://6353team18project.strakerak.repl.co/')
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing initial login response
print("Testing if sample login works with sample data")
data = {
    'username': 'admin',
    'password': 'password',
}
response = requests.post('https://6353team18project.strakerak.repl.co/', data=data)
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing failed login
print("Testing if sample login won't work")
data = {
    'username': 'notadmin',
    'password': 'password',
}
response = requests.post('https://6353team18project.strakerak.repl.co/', data=data)
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing random page
print("Testing if random page will fail the test (Look for fail)")
response = requests.get('https://6353team18project.strakerak.repl.co/doesntexist')
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed! (Passed here)\n')

#Testing registration page get
print("Testing if registration page works")
response = requests.get('https://6353team18project.strakerak.repl.co/register')
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing registration itself
print("Testing if I can register")
data = {
    'username': 'newuser',
    'password': 'password',
}
response = requests.post('https://6353team18project.strakerak.repl.co/register', data=data)
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing profile editing
print("Testing if I can edit my profile")
data = {
    'fullname':'Jon Doe',
    'address1':'4545 Cullen',
    'address2':'',
    'city':'Houston',
    'state':'TX',
    'zipcode':'77004',
}
response = requests.post('https://6353team18project.strakerak.repl.co/profile', data=data)
if '200' in str(response): #In this case a 302 should show up in my console, if it doesn't, fail.
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing if I can access quote page
print("Testing if I can go to quote page")
response = requests.get('https://6353team18project.strakerak.repl.co/quote')
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')


#Testing if I can ask for a quote

  data = {
    'quantity':'10'
  }
print("Testing if I can ask for a quote") #This one might fail due to quote only being a class
response = requests.post('https://6353team18project.strakerak.repl.co/quote', data=data)
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')

#Testing if I can access history page
print("Testing if I can go to history page")
response = requests.get('https://6353team18project.strakerak.repl.co/history')
if '200' in str(response):
  print('Test Passed!\n')
else:
  print('Test Failed!\n')
