from jnpr.junos import Device
import argparse
import yaml
import datetime
from lxml import etree
import os

def connect(port, hostname, config_name, config_date):
    device = Device(host='127.0.0.1', user='root', password='Juniper', port=port)
    device.auto_probe = 30
    # funTime = datetime.now()
    try:
        device.open()
        print 'connected to ' + hostname
        config = etree.tostring(device.rpc.get_config(), encoding='unicode', pretty_print=True)
    except Exception as err:
        print err.message
    f = open('./configs/{}-{}'.format(config_name, config_date) + '/' + hostname + '-' + config_name + '-' + config_date, 'w')
    f.write(config)

    # a = datetime.now() - funTime
    # print("time to execute {}, {}".format(ip, a))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", '--CONFIG_NAME', type=str, help='name of configuration to be uploaded', required=True)
    args = parser.parse_args()
    config_name = args.CONFIG_NAME
    config_date = str(datetime.date.today())
    hosts = yaml.load(open('./jncie-dc-vars.yml'))
    os.mkdir('./configs/{}-{}'.format(config_name, config_date))

    for hostname in hosts['routers']:
        port = hosts['routers'][hostname]['ssh_port']
        try:
            connect(port, hostname, config_name, config_date)
        except ValueError as err:
            print(err.args)

    for hostname in hosts['switches']:
        port = hosts['switches'][hostname]['ssh_port']
        try:
            connect(port, hostname, config_name, config_date)
        except ValueError as err:
            print(err.args)
			
    for hostname in hosts['firewalls']:
        port = hosts['firewalls'][hostname]['ssh_port']
        try:
            connect(port, hostname, config_name, config_date)
        except ValueError as err:
            print(err.args)

if __name__ == '__main__':
    main()