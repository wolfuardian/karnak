import getpass

user_name = getpass.getuser()
module_name = 'karnak'

module_path = 'C:\\Users\\{0}\\Documents\\maya\\2020\\modules\\{1}.mod'.format(user_name, module_name)

command = """+ karnak 1.0 C:/Users/{0}/PycharmProjects/{1}
scripts: C:/Users/{0}/PycharmProjects/{1}""".format(user_name, module_name)

fp = open(module_path, 'w')
fp.write(command)
fp.close()

