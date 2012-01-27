import junar_api
auth_key = 'h3pq8z2eu84djqenbzik';
junar_api_client = junar_api.Junar(auth_key)
datastream = junar_api_client.datastream('FARM-CROP-PRICE-BY-PARRI')
response = datastream.invoke(params = ['CLARENDON'], output = 'json_array', page = 0, limit = 10)
result = response['result']
for row in result:
    print row
