import getpass
import os

user_name = getpass.getuser()
module_name = 'karnak'

module_folder = 'C:\\Users\\{0}\\Documents\\maya\\2020\\modules'.format(user_name)
module_file = '{0}\\{1}.mod'.format(module_folder, module_name)

command = """+ karnak 1.0 C:/Users/{0}/PycharmProjects/{1}
scripts: C:/Users/{0}/PycharmProjects/{1}""".format(user_name, module_name)

if not os.path.exists(module_folder):
    os.makedirs(module_folder)

fp = open(module_file, 'w')
fp.write(command)
fp.close()

