import subprocess, re

class TextDecorator(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def sucess(txt):
        return TextDecorator.OKGREEN + txt + TextDecorator.ENDC

    @staticmethod
    def fail(txt):
        return TextDecorator.FAIL + txt + TextDecorator.ENDC

    @staticmethod
    def warning(txt):
        return TextDecorator.WARNING + txt + TextDecorator.ENDC

def check_machine_statues():
    machines = [
        {'id': 0,  'ip': '52.89.130.208'},
        {'id': 1,  'ip': '52.88.213.154'},
        {'id': 2,  'ip': '52.89.136.97' },
        {'id': 3,  'ip': '52.11.249.176'},
        {'id': 4,  'ip': '52.89.169.220'},
        {'id': 6,  'ip': '52.89.147.43' },
        {'id': 7,  'ip': '52.25.4.192'  },
        {'id': 9,  'ip': '52.88.93.86'  },
        {'id': 10, 'ip': '52.88.255.164'},
        {'id': 11, 'ip': '52.88.163.127'},
        {'id': 12, 'ip': '50.112.137.231'},
    ]

    for machine in machines:
        remote_cmds = [
            'ps aux | grep [r]uby',
            'wc -l data-mining/renters/full_crosses_renters_0921212303_%s.csv' % machine['id'],
            'tail data-mining/renters/data/out_full_%s_0921212303.log | grep HITTING' % machine['id'],
        ]
        cmd = "ssh -i /Users/haoran/.ssh/bonjoy-team.pem ubuntu@%s '%s'" % (machine['ip'], ';'.join(remote_cmds))
        try:
            output = subprocess.check_output(cmd, shell=True)
            header = ">>>> [%s] %s" % (machine['id'], machine['ip'])

            if re.search('ruby browser_robot.rb', output):
                header = TextDecorator.sucess(header)
            else:
                header = TextDecorator.fail(header)
            print(header)
            print output
        except subprocess.CalledProcessError as e:
            print e

if __name__ == '__main__':
    check_machine_statues()
