import sys
import csv
import settings
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError

class ADInfo:
    def __init__(self, server_name, domain_name, user_name, password, search_dc):
        self.__server_name = server_name
        self.__domain_name = domain_name
        self.__user_name = user_name
        self.__password = password
        self.__search_dc = search_dc

    def connect(self):
        self.__server = Server(self.__server_name, port = 389, get_info = ALL)
        self.__conn = Connection(self.__server,
                                 user = f'{self.__domain_name}\\{self.__user_name}',
                                 password = self.__password,
                                 authentication = NTLM,
                                 auto_bind = True)

    def who_am_i(self):
        return self.__conn.extend.standard.who_am_i()

    def search_users(self):
        self.__conn.search(self.__search_dc,
                           '(&(|(objectclass=user)(objectclass=person)(objectclass=inetOrgPerson)(objectclass=organizationalPerson))(!(objectclass=computer)))',
                           attributes = [ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        return self.__conn.entries

    def output_users(self, entries, csv_filepath):
        with open(csv_filepath, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f)
            for entry in sorted(entries):
                try:
                    desc = entry.description
                except LDAPCursorError:
                    desc = ""
                try:
                    memberOf = entry.memberOf
                except LDAPCursorError:
                    memberOf = [""]
                for group in memberOf:
                    group_cnname = group.split(",")[0].lstrip("CN=")
                    writer.writerow([entry.sAMAccountName, entry.name, desc, group_cnname])
                    print([entry.sAMAccountName, entry.name, desc, group_cnname])

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

def main():
    print("===================================================================")
    print("Active Directory のユーザー情報を取得してCSVファイルを出力します。")
    print("ユーザーごとに所属しているグループも取得します。")
    print("===================================================================")

    # 引数のチェック
    argvs = sys.argv
    if len(argvs) != 2 or not argvs[1]:
        print("CSVファイルのパスを指定してください。")
        return RETURN_FAILURE

    # CSVファイルパスの取得
    csv_filepath = argvs[1].strip()

    try:
        # AD情報
        adinfo = ADInfo(settings.SERVER_NAME,
                        settings.DOMAIN_NAME,
                        settings.USER_NAME,
                        settings.PASSWORD,
                        settings.SEARCH_DC)
        adinfo.connect()
        print(adinfo.who_am_i())

        # CSV出力
        entries = adinfo.search_users()
        adinfo.output_users(entries, csv_filepath)
    except Exception as e:
        print(e)
        return RETURN_FAILURE

    return RETURN_SUCCESS

if __name__ == "__main__":
    main()
