import time
import junar_api

if __name__ == '__main__':
    # mixing data about chilean nacional security

    # get an auth_key at www.junar.com/developers/
    auth_key = 'yourauthkey'
    junar_api_client = junar_api.Junar(auth_key)

    # the guid (identificator)
    datastream = junar_api_client.datastream('SEGUR-EN-TASA-DE-DENUN')
    response = datastream.invoke(output = 'json_array')

    # creating new data =)
    my_new_data = []
    my_new_data.append(response['result'][3])
    my_new_data.append(response['result'][4])

    # because your key could has a request limit :-)
    time.sleep(5)

    datastream = junar_api_client.datastream('SEGUR-EN-TASA-DE-DETEN')
    response = datastream.invoke(output = 'json_array')

    my_new_data.append(response['result'][4])

    # "printing" our csv
    for row in my_new_data:
        print ','.join( ['"%s"' % cell for cell in row] )
