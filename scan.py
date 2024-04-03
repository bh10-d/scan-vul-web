import sys
import sqli_scanner as sqliscanner
import sql_injection_detector as sqlinjection_detectform
# def menus():
#     print('''
#     [+] 1. 
#     [+] 2. Access Control
#     [+] 3. SQL Injection
#     [+] 4. 
#     [+] 5. URL Brute force detection
#     ''')

# menus()
print('''\033[92m
    ______            _     _        _____  _   _  
    |  _  \          | |   | |      / __  \| | | | 
    | | | |___  _   _| |__ | | ___  `' / /'| |_| | 
    | | | / _ \| | | | '_ \| |/ _ \   / /  |  _  | 
    | |/ / (_) | |_| | |_) | |  __/ ./ /___| | | | 
    |___/ \___/ \__,_|_.__/|_|\___| \_____/\_| |_/
	                    recoded by BUIDUCHIEU
''')

attackNameString = [
    {"-r":""}
]

helpCommand = """
    Welcome to my tool and now how we run this tool. To run it please using command
    and provide tag information.
    -h: --help
    -u: url string
    -a: attack name, example: -a sqlinjection, -a accesscontrol, ... 
"""

getUrl = sys.argv[sys.argv.index('-u')+1]
getAttackName = sys.argv[sys.argv.index('-a')+1]

# print(sys.argv)
# print(getUrl)
# print(getAttackName)


# for string in sys.argv:
#     if((string == '-h' or string == '--help')and string in helpCommand):
#         print(helpCommand)
#         exit()


match getAttackName:
    case 'sqlinjection':
        # sqliscanner.sqlinjection(getUrl)
        # print(sqlinjection_detectform.sqlinjection_detectform(getUrl))
        detect_form = sqlinjection_detectform.sqlinjection_detectform(getUrl)
        if detect_form == 0:
            print(detect_form)
            sqliscanner.sqlinjection(getUrl)
