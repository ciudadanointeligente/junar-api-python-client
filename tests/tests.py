from unittest import TestCase
from ludibrio import Stub
from junar_api import junar_api
import urllib

class PublishingTest(TestCase):
    dictionary = {
            'source'    : u'http://www.example.com/example.csv',
            'title'     : u'example title',
            'subtitle'  : u'example title - subtitle',
            'description': u'a description',
            'tags'      : u'', #empty for now because resources do not have any tags
            'notes'     : u'',#empty for now because resources do not have any author notes
            'table_id'  : u'table0',
            'category'  : u'thecategory',
            'auth_key'  : u'THE-AUTH-KEY'
            }

    params = urllib.urlencode(dictionary)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    the_guid = u'THE-PRECIOUS-GUID'
    

    def setUp(self):
        from httplib import HTTPResponse
        with Stub() as HTTPResponse:
            HTTPResponse.status >> 200
            HTTPResponse.read() >> '{"id": "THE-PRECIOUS-GUID", "title": "example title", "subtitle": "example title - subtitle", "description": "a description", "user": "lfalvarez", "tags": [], "created_at": 1329767353.0, "source": "http://www.example.com/example.csv", "link": "http://www.junar.com/datastreams/some-url"}'

        with Stub() as conn:
            from httplib import HTTPConnection
            conn = HTTPConnection("api.junar.com")
            conn.request("POST", "/datastreams/publish", self.params, self.headers)
            conn.getresponse()  >> HTTPResponse

    

    def tearDown(self):
        pass
 
    def test_stub(self):
        from httplib import HTTPConnection
        conn = HTTPConnection("api.junar.com")
        conn.request("POST","/datastreams/publish", self.params, self.headers)
        response = conn.getresponse()
        assert response.status == 200
        assert isinstance(response.read(), (str,unicode))

    def test_si_publica_correctamente_devuelve_un_objeto_datastream(self):
        junar_api_client = junar_api.Junar(u'THE-AUTH-KEY', base_uri = 'http://api.junar.com')
        datastream = junar_api_client.publish(self.dictionary)
        assert isinstance(datastream, junar_api.DataStream)
        assert datastream.guid == self.the_guid
