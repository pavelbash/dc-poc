from jinja2 import Environment, FileSystemLoader
import yaml
from collections import OrderedDict
import datetime


def read_file():
    now = datetime.datetime.now()
    config_data = ordered_load(open('./jncie-dc-lab.yml'))
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('vagrantfile-template.j2')
    f = open('Vagrantfile' + '-' + now.strftime("%Y-%m-%d"), 'w')
    f.write(template.render(config_data=config_data))

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def main():
    try:
        read_file()
    except ValueError as err:
            print(err.args)
            print "Something went wrong _MAIN_"

if __name__ == '__main__':
          main()