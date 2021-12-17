import argparse
import yaml
import paramiko
from scp import SCPClient


def connect(license, port, hostname):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', username='root', password='Juniper', look_for_keys=False, port=port)
    scp = SCPClient(client.get_transport())
    print hostname

    try:
        scp.put(license, 'vmx-license')
    except Exception as err:
        print err.message
    try:
        stdin, stdout, stderr = client.exec_command(
            '/usr/sbin/cli -c "request system license add vmx-license"', timeout=60)
        print stdout.channel.recv_exit_status()
    except Exception as err:
        print err.message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--FILE_NAME', type=str, help='license file name', required=True)
    args = parser.parse_args()
    license = args.FILE_NAME
    hosts = yaml.load(open('./dc-poc.yml'))

    for hostname in hosts['routers']:
        port = hosts['routers'][hostname]['ssh_port']
        try:
            connect(license, port, hostname)
        except ValueError as err:
            print(err.args)


if __name__ == '__main__':
    main()