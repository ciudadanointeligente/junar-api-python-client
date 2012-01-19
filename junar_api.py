import urllib
import json
import decimal

class DataStream:

    def __init__(self, guid):
        # get one at http://www.junar.com/developers/
        self.auth_key = 'YOUR_AUTH_KEY'
        self.guid = guid
        self.base_uri = 'http://apisandbox.junar.com'
        self.response = None

        """
        for default junar json leave output blank, its structure is explained here http://wiki.junar.com/index.php/API#JSON_Structure
        other options are: 
        - prettyjson
        - json_array, basic javascript array of arrays
        - csv
        - tsv
        - excel
        """
        self.output = '';


    def get_guid(self):
        return self.guid

    def invoke(self, params = [], output = ''):

        # create the URL
        query = {'auth_key': self.auth_key}
        i = 0
        for param in params:
            query['pArgument%d' % i] = param;
            i = i + 1

        if output != '':
            self.output = output
            query['output'] = output

        url = '/datastreams/invoke/%s?%s' % (self.guid, urllib.urlencode(query))
        return self.call_uri(url);

    def info(self):
        # create the URL
        query = {'auth_key': self.auth_key}
        url = '/datastreams/invoke/%s?%s' % (self.guid, urllib.urlencode(query))
        return self.call_uri(url);

    def call_uri(self, url):
        # get the url
        # you could also use cURL here, it has better performance but i dont
        # know if you have cURL installed
        network_object = urllib.urlopen(self.base_uri + url)
        response       = network_object.read()

        # parsing the content
        if self.output in ['', 'prettyjson', 'json_array']:
            self.response = json.loads(response, parse_float=decimal.Decimal)

        return self.response


if __name__ == '__main__':
    datastream = DataStream('TEPCO-STOCK-QUOTE')
    print datastream.invoke(output = 'json_array')
