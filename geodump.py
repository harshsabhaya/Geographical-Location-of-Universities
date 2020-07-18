import sqlite3
import codecs
import json

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()
cur.execute('SELECT * FROM Location')

fhand = codecs.open('where.js', 'w', 'utf-8')
fhand.write('myData = [\n')
count = 0

for row in cur:
    data  = row[1].decode()

    try:
        js = json.loads(str(data))
    except:
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    if lat == 0 or lng == 0:
        continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", " ")

    try:
        print(where, lat, lng)

        count = count + 1
        if count > 1: fhand.write(',\n')
        output = "["+str(lat)+", "+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        pass

fhand.write('\n]')
cur.close()
fhand.close()