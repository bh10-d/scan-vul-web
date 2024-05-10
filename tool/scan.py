import sys, config
# import config
import sqli_scanner as sqliscanner
import access_control as accesscontrol
# import bruteforce_oscommand as oscommand
import sql_injection_detector as sqlinjection_detectform
import OSCommand as oscommand

print("""
    ______            _     _        _____  _   _  
    |  _  \          | |   | |      / __  \| | | | 
    | | | |___  _   _| |__ | | ___  `' / /'| |_| | 
    | | | / _ \| | | | '_ \| |/ _ \   / /  |  _  | 
    | |/ / (_) | |_| | |_) | |  __/ ./ /___| | | | 
    |___/ \___/ \__,_|_.__/|_|\___| \_____/\_| |_/
	            coded by BUIDUCHIEU + MINH HOA
""")

attackNameString = [
    {"-r":""}
]

helpCommand = """
    Welcome to my tool and now how we run this tool. To run it please using command
    and provide tag information.
    -h: --help
    -u: url string
    -a: attack name, example: -a sqlinjection, -a accesscontrol, ... 
    --username: username, example: --username hieu
    --password: password, example: --password hieu
"""

for string in sys.argv:
    if((string == '-h' or string == '--help')):
        print(helpCommand)
        exit()

getUrl = sys.argv[sys.argv.index('-u')+1]
getAttackName = sys.argv[sys.argv.index('-a')+1]
getUsername = ''
getPassword = ''
if '--username' in sys.argv and '--password' in sys.argv:
    getUsername = sys.argv[sys.argv.index('--username')+1]
    getPassword = sys.argv[sys.argv.index('--password')+1]
# handle url
r = config.r.get(getUrl)

if r.status_code == 200:
    getUrl
else:
    if getUrl[-1] != '/':
        getUrl = getUrl + '/'


match getAttackName:
    case 'sqlinjection':
        # sqliscanner.sqlinjection(getUrl)
        # print(sqlinjection_detectform.sqlinjection_detectform(getUrl))
        detect_form = sqlinjection_detectform.sqlinjection_detectform(getUrl)
        # print(detect_form)
        if detect_form == 0:
            sqliscanner.sqlinjection(getUrl)
    case 'accesscontrol':
        if getUrl[-1] != '/':
            getUrl = getUrl + '/'
        accesscontrol.access_control(getUrl, getUsername, getPassword)
        # print(getUrl)
        # accesscontrol.access_control(getUrl)
    # case 'xss':
    case 'oscommand':
        oscommand.interact_with_form(getUrl, verify_ssl=False)
        # print("OS-COMMAND")
    # case 'pathtraversal':
            
