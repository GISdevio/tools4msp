from django.core.management.base import BaseCommand, CommandError
from tools4msp.models import CodedLabel

BODY = """Tools4MSP Coded Labels
======================

{body}
"""

GROUP = """{group_label}
{group_label_underline}

{group_body}
"""

CODE = """{code}
  {code_label}
  
  {code_desc}

  MSFD: {code_msfd}
  
  {code_uri}
"""


class Command(BaseCommand):
    help = 'Export documentation for the Coded Labels'
    
        
    def handle(self, *args, **options):
        groups = [
            ('casestudy', 'Case Study'),
            ('use', 'Human Uses'),
            ('env', 'Environmental Receptors'),
            ('pre', 'Pressures'),
            ('cea', 'CEA Module'),
            ('pmar', 'Pressure Assessment for Marine Activities module'),
            ('muc', 'MUC Module'),
            ('partrac', 'PARTRAC Module'),
            ]

        body = ""
        for g in groups:
            body += "\n\n\n" + get_group_body(g[0], g[1])
        self.stdout.write(BODY.format(body=body))

        # for c in cls:
        #    pass
        #    # 

def get_group_body(group, group_label):
    qs = CodedLabel.objects.filter(group=group)
    body = ""
    for c in qs:
        msfd_code = '-'
        if c.group == 'env':
            msfd_code = c.get_msfd() or '-'
        d = {'code': c.code,
             'code_label': c.label,
             'code_desc': c.description.replace("\n", "\n  ").replace("-", " -"),
             'code_msfd': msfd_code,
             'code_uri': "https://api.tools4msp.eu/api/codedlabels/{}".format(c.code)
             }
        body += "\n\n" + CODE.format(**d)
    group_body = GROUP.format(group_label=group_label,
                              group_label_underline="-"*len(group_label),
                              group_body=body
                              )
    return group_body
