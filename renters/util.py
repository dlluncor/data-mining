import json
from collections import Counter

def extract_emails_from_logs():
    emails = Counter()

    for filename in ['data/success_no_0921212303.log', 'data/success_special_0921212303.log']:
        with open(filename) as fin:
            for line in fin:
                log = json.loads(line)
                email = log['data'][16]
                emails[email] += 1
    """
    for filename in ['data/error_no_0921212303.log', 'data/error_special_0921212303.log']:
        with open(filename) as fin:
            for line in fin:
                log = json.loads(line)
                email = log['data'][16]
                if emails[email] > 0:
                    print('Oooops same email scucess and fail; %s' % email)
                    del emails[email]
    """
    print "[%s]" % ','.join( '"%s"' % email for email, cnt in emails.most_common(20))

if __name__ == '__main__':
    extract_emails_from_logs()
