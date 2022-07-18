from typing import OrderedDict
from requests import request
import uncurl
import pytest
from freeintruder import attacks

request = "curl -i -s -k -X $'GET' \
    -H $'Host: www.shodan.io' -H $'Sec-Ch-Ua: \"-Not.A/Brand\";v=\"8\", \"Chromium\";v=\"102\"' -H $'Sec-Ch-Ua-Mobile: ?0' -H $'Sec-Ch-Ua-Platform: \"Linux\"' -H $'Upgrade-Insecure-Requests: 1' -H $'User-Agent: %Mozilla%/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H $'Sec-Fetch-Site: same-origin' -H $'Sec-Fetch-Mode: navigate' -H $'Sec-Fetch-User: ?1' -H $'Sec-Fetch-Dest: document' -H $'Referer: https://www.shodan.io/' -H $'Accept-Encoding: %gzip%, deflate' -H $'Accept-Language: en-US,en;q=0.9' \
    $'https://www.shodan.io/search?query=%solid-snake%'"

char = "$"
request = (request).replace(char,"")
marker = "%"
r = (uncurl.parse_context(request))._asdict()

pattern = f"(?:{marker})(.*?)(?:{marker})"
payloads = ["/home/lucio/InfoSec/LISTS/digits.txt"]

def test_positions():
    positions = attacks.positions_search(r,pattern)
    result = OrderedDict([("url",(None,(35,48))),('User-Agent', ('headers', (0, 9))), ('Accept-Encoding', ('headers', (0, 6)))])
    
    
    assert positions == result
    
def test_marker_cleaner():
    
    clean_request = attacks.marker_cleaner(r,marker)
    
    clean_raw_request = (request).replace(marker,"")
    clean_r = uncurl.parse_context(clean_raw_request)

    
    assert clean_request == clean_r._asdict()
    
def test_request_modifier():
    
    payload = "I_am_Here"
    
    changed_request = attacks.request_modifier(r,payload,"url",pattern)
       
    #assert changed_request["url"] == "https://www.shodan.io/search?query=I_am_Here"
    
    
def test_request_modifier_2():
    
    payload = "I_am_Here"
    
    changed_request = attacks.request_modifier(r,payload,"User-Agent",pattern,"headers")
       
    assert changed_request["headers"]["User-Agent"] ==  "I_am_Here/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
   
        
    
def test_sniper():
    
    positions = attacks.positions_search(r,pattern)
    with open(payloads[0],"r") as file:
        sniper_res = attacks.sniper(r,positions,file,marker,pattern)
    #assert len(sniper_res) == 3*10