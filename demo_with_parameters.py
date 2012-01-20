import junar_api

if __name__ == '__main__':
    # display dates related to proposed law at Chilean senado
    guid = 'CONGR-DE-LA-PROYE-PUBLI'

    # get an auth_key at www.junar.com/developers/
    auth_key = 'yourauthkeyhere'
    junar_api_client = junar_api.Junar(auth_key)

    # the guid (identificator)
    datastream = junar_api_client.datastream(guid)

    response = datastream.invoke(params = ['01/01/2011', '01/12/2011'], output = 'json_array')
    result = response['result']

    # iterating the response and printing it
    for row in result:
        print '%s -> %s' % (row[4], row[1])
