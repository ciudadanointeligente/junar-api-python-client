import urllib
import json
import decimal

class Junar:
    def __init__(self, auth_key, base_uri = 'http://apisandbox.junar.com'):
        self.auth_key = auth_key
        self.base_uri = base_uri

    def datastream(self, guid):
        return DataStream(guid, self.auth_key, self.base_uri)


class DataStream:

    def __init__(self, guid, auth_key, base_uri):
        self.auth_key = auth_key
        self.base_uri = base_uri
        self.guid = guid
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

        if not self.auth_key:
            raise Exception('Please configure your auth_key, get one at http://www.junar.com/developers/')

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
        network_object = urllib.urlopen(self.base_uri + url)
        response       = network_object.read()

        if network_object.getcode() != 200:
            raise Exception('Error HTTP status code = %s' % network_object.getcode())

        # parsing the content
        if self.output in ['', 'prettyjson', 'json_array']:
            self.response = json.loads(response, parse_float=decimal.Decimal)
        else:
            self.response = response

        return self.response
