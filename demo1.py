import junar_api

# mostrando las fechas en que entran y salen los proyectos de ley

guid = 'CONGR-DE-LA-PROYE-PUBLI'
datastream = junar_api.DataStream(guid)
response = datastream.invoke(params = ['01/01/2011', '01/12/2011'], output = 'json_array')
result = response['result']
for row in result:
    print '%s -> %s' % (row[4], row[1])
