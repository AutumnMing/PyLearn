from requests import get as res_get
from requests.cookies import RequestsCookieJar
from textwrap import dedent

base_url = 'https://club-api.c.hihonor.com/honor/apk/clientreq.php'
params = {
    'ver': '1',
    'seq': '1',
    'MagicUIVer': '',
    'MachineID': 'SM-G955N',
    'versionCode': '10019010',
    'club_id': 'CLUB_1670503696484',
    'interface': 'gethome',
    'uid': '35589253'
}
cookies_dict = {
    'a3ps_2132_auth': '''WafJucVRHm%2BPYXRr6bII2kdPT3PY4jFKrYoPt%2BlU8A89l36CAS%2FeIr47r4EFQTxLylDR2gLuM%\
2BtKUC2G8aR77SdCTcpC9Mwg3Dd2Ki17Qz1ahRSvgMi2mFBaWWjVH4gBTwhLitwrSkGJxv87lbk7kI148aDbfAdjccFzW3wzh4%2BkzZA6\
Aj9koXDtaQ7bvVGPQJmcLLl8OnxhdXRoY29kZXw6fG9wZW5zc2xfMnw6fKCK2SB765JBuRwhrXw6fLXYX8l8oWAqfzpV%2FxWltVE%3D''',
    'a3ps_2132_saltkey': '''3JuXGubcA28n53ft%2F8%2FsSh87Cgn%2BNuK9tlgKxJaFnjXsaoH7N0bgQjQ9kHM2l6DKWTMJYYWvZ%2B2q6\
%2FTb%2FsAWznw6fGF1dGhrZXl8OnxvcGVuc3NsXzJ8OnxtEtAnM4XSiKes9cx8OnwqbOn3VR2O%2BoRF%2FSifk5Jw'''
}
jar = RequestsCookieJar()
for key, value in cookies_dict.items():
    # print('=' * 150)
    # print(key)
    # print(value)
    jar.set(key, value)

headers = {
    'User-Agent': dedent('''Mozilla/5.0 (Linux; U; Android 7.1.2; zh; SM-G955N Build/NRD90M.G955NKSU1AQDC) \
AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'''),
    'AUTHORIZATION': dedent('''HUAFANS-HMAC-SHA256 appid=7910,timestamp=1670852417,\
signature="PMcnJ0WUxWPL+/jl4guzEYvYjoRmYBovtIaaNcHru2o="''')
}
r = res_get(base_url, params=params, cookies=jar, headers=headers)
print(r.status_code)
print(r.url)
print(r.encoding)
print(r.json())


