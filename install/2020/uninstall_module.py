import getpass
import os

user_name = getpass.getuser()
module_name = 'karnak'

module_path = 'C:\\Users\\{0}\\Documents\\maya\\2020\\modules\\{1}.mod'.format(user_name, module_name)

try:
    os.remove(module_path)

except:
    print('Nothing needs to be removed.')
