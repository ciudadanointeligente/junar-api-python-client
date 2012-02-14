import junar_api
junar_api_client = junar_api.Junar('yourauthkey')
datastream = junar_api_client.datastream('CURRE-AGAIN-USD-FULL-LIST')
response = datastream.invoke(output = 'prettyjson')
for row in response['result']:
    print row

response = datastream.invoke(output = 'xml')
print response
