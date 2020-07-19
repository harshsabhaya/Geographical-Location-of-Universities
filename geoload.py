import json
import sqlite3
import urllib.parse
import urllib.request
import ssl

api_key = False
if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else:
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()
# cur.execute('DROP table if exists Location')
cur.execute('CREATE TABLE if not EXISTS Location (address TEXT, geodata TEXT)')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fhand = open('where.data')
count = 0
total = 0
for line in fhand:
    if count >= 50 :   # run file one time, received 50 new data only if you want more than 50 then re-run file
        break

    address = line.strip()

    cur.execute('SELECT geodata FROM Location WHERE address = ?', (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print('Found in database', address)
        total = total + 1
        continue
    except:
        pass

    parm = dict()
    parm['address'] = address
    if api_key is not False: parm['key'] = api_key

    url = serviceurl + urllib.parse.urlencode(parm)
    print('Retrieved url : ', url)

    uh = urllib.request.urlopen(url, context=ctx)
    geodata = uh.read().decode()

    count = count + 1
    total = total + 1
    try:
        js = json.loads(geodata)
    except:
        print(geodata)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] == 'ZERO_RESULTS'):
        print('-----FAIl to find data ------')
        print(geodata)
        continue

    cur.execute('INSERT INTO Location (address, geodata) VALUES (?,?)',
                (memoryview(address.encode()), memoryview(geodata.encode())))

    conn.commit()
print('\nReceived', count, 'new Data')
print('Total', total, 'Data in Database')
print('\nRe_run file If you want to more data')