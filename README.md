# api-Python-crud-operations
operation POST: http://localhost/insert
payload= {
    "Name":"jai prakash",
    "DateOfBirth":"12/30/1992",
    "Id": 2,
    "city":"VSKP",
    "state":"TL",
    "Email":"dummy@xyz.com"
}

operation PUT :http://localhost/insert
payload = {
    "Id": "2", # condition
    "firstname":"j" #value need to changed 
}

Operation GET : http://localhost/query
payload = {
    "Id": 1 # condition
}

Operation DELETE : http://localhost/delete
payload = {
    "Id": "2"
      }
