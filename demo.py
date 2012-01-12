import time
import junar_api

datastream = junar_api.DataStream('SEGUR-EN-TASA-DE-DENUN')
response = datastream.invoke(output = 'json_array')

my_new_data = []
my_new_data.append(response['result'][3])
my_new_data.append(response['result'][4])

# because your key has a request limit :-)
time.sleep(5)

datastream = junar_api.DataStream('SEGUR-EN-TASA-DE-DETEN')
response = datastream.invoke(output = 'json_array')

my_new_data.append(response['result'][4])

# "printing" our csv
for row in my_new_data:
    print ','.join( ['"%s"' % cell for cell in row] )"""
