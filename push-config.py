from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import argparse
import yaml

def connect(cfg, port, hostname):
    device = Device(host='127.0.0.1', user='root', password='Juniper', port=port)
    device.auto_probe = 30
    # funTime = datetime.now()
    cu = Config(device, mode='private')
    try:
        device.open()
        print hostname
        try:
            cu.load(cfg, overwrite=True, ignore_warning=True)
        except ValueError as err:
            print err.message
        commit = cu.commit_check()
        if commit == True:
            print '--OK--'
            cu.commit(comment="config loaded via provisioning script")
            print('Configuration commited on {}'.format(hostname))
        else:
            print('Error commiting configuration on {}, rolling back changes'.format(ip))
            cu.rollback()
            pass
        device.close()

    except Exception as err:
        print err.message
    # a = datetime.now() - funTime
    # print("time to execute {}, {}".format(ip, a))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", '--CONFIG_NAME', type=str, help='name of configuration to be uploaded', required=True)
    parser.add_argument("-d", '--CONFIG_DATE', type=str, help='date of configuration to be uploaded', required=True)
    args = parser.parse_args()
    config_name = args.CONFIG_NAME
    config_date = args.CONFIG_DATE
    hosts = yaml.load(open('./jncie-dc-vars.yml'))

    for hostname in hosts['routers']:
        with open("./configs/{}-{}/{}-{}-{}".format(config_name, config_date, hostname, config_name, config_date), 'r') as f:
            cfg = f.read()
        port = hosts['routers'][hostname]['ssh_port']
        try:
            connect(cfg, port, hostname)
        except ValueError as err:
            print(err.args)

    for hostname in hosts['switches']:
        with open("./configs/{}-{}/{}-{}-{}".format(config_name, config_date, hostname, config_name, config_date), 'r') as f:
            cfg = f.read()
        port = hosts['switches'][hostname]['ssh_port']
        try:
            connect(cfg, port, hostname)
        except ValueError as err:
            print(err.args)

    for hostname in hosts['firewalls']:
        with open("./configs/{}-{}/{}-{}-{}".format(config_name, config_date, hostname, config_name, config_date), 'r') as f:
            cfg = f.read()
        port = hosts['firewalls'][hostname]['ssh_port']
        try:
            connect(cfg, port, hostname)
        except ValueError as err:
            print(err.args)
			
if __name__ == '__main__':
    main()