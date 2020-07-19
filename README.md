# Geographical Location of Universities
---
### where.data
- You can create your own file and add University name in text format

---
###  geoload.py :
- Read Universities name from where.data file
- Store Universities name in TEXT format and it's address in JSON format in Database (location received using urllib.request.urlopen() method)

---
### geodump.py :  
- Retrieved it's location from Database and Data store in where.js file 

---
### where.js : automatically created file (using File Handling)
- Latitude, Longitude and Address of Universities data in list format  

--- 
### where.html: 
 - Read latitude, longitude and address from where.js file
 - Show Universities location in map
 - If you want to read address then hover over on marker in map
---
