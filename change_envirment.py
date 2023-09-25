# --*--*--*--*--*--*- Create by bh at 2020/8/27 15:08 -*--*--*--*--*--*--
import os

setting_dir = os.path.join(os.path.abspath('./'))

production_name = 'apis/conf/project_conf.py'
production_offline_name = 'apis/conf/project_offline.py'

production_setting = os.path.join(setting_dir, production_name)
production_offline_setting = os.path.join(setting_dir, production_offline_name)


# docker_name = 'docker-compose.yml'
# docker_offline_name = 'docker-compose_offline.yml'

# docker_setting = os.path.join(setting_dir, docker_name)
# docker_offline_setting = os.path.join(setting_dir, docker_offline_name)


def exchange_file_name(file_name1, file_name2, tmp_name):
    """
    切换文件名

    :param file_name1:
    :param file_name2:
    :param tmp_name:
    :return:
    """
    os.rename(file_name1, tmp_name)
    os.rename(file_name2, file_name1)
    os.rename(tmp_name, file_name2)


def change_settings_name(settings_dir, offline_dir):
    """
        修改配置文件名称与docker环境名称，方便开发。
        以后的开发中，配置文件将永远引用project_conf，特写此程序互换配置文件的文件名。
        以后只需要运行一下该程序，便可以在各种开发环境与线上环境中切换。
    """
    if os.path.exists(settings_dir) and os.path.exists(offline_dir):
        tmp_name = os.path.join(setting_dir, 'tmp_name')
        exchange_file_name(settings_dir, offline_dir, tmp_name)
        return 0
    else:
        return -1


if __name__ == "__main__":
    print(production_setting)
    result = change_settings_name(production_setting, production_offline_setting)
    if result == 0:
        print('修改完毕!')
    elif result == -1:
        print('缺少配置文件!')
