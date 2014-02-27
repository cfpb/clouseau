#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Encapsulate the clouseau structure to simplify use in different parsers
#
#
import pprint
import re

class ClouseauModel(object):

    model = {'meta': {'github_url': ''}}

    def __init__(self, github_url, terms):
        self.model['meta']['github_url'] = github_url
        for term in terms:
            self.model[term] = {}

    def start_match(self, term, refspec, filename, git_log):
        title = refspec + ":" + re.sub('[^0-9a-zA-Z]+', '_', filename) # title will look like sha1:directory_file_ext, eg d1859009afc7e48506ec025a07f4f90ce4c5a210:somedir_hooktest_txt'
        if not title in self.model[term]:
            self.model[term][title] = {'src': filename, 'refspec': refspec, 'git_log': git_log, 'matched_lines': []}
        return title

    def add_match_line(self, term, title, line_number, match_text):
        self.model[term][title]['matched_lines'].append([line_number, match_text])

    def __str__(self):
        return pprint.pformat(self.model)

    def __repr__(self):
        return self.__str__()


  # {
  #   search_term: {'%hash:filename%': {'git_log': [array_of_git_log_output_lines],
  #                                     'refspec':hash,
  #                                     'src':'filename.ext',
  #                                     'matched_lines':[[line_number, match_string],[line_number, match_string]]},
  #                 '%hash:filename2%': {...}}
  # }
  #
  # example:

 #  {
 #  'meta': {'github_url': 'https://github.com/marcesher/cato'},
 # '[A-Z0-9._%-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}': {u'e0e0aa800a4f2b0a9339614107828c67bd73a769:admin_py': {'git_log': ['commit e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                               'Author: Marc Esher <marc.esher@gmail.com>',
 #                                                                                                               'Date:   Mon Feb 24 16:35:51 2014 -0500',
 #                                                                                                               'Adding a password to the file',
 #                                                                                                               '',
 #                                                                                                               'Hey Jude',
 #                                                                                                               '',
 #                                                                                                               'My username = "thekid"'],
 #                                                                                                   'matched_lines': [[u'14',
 #                                                                                                                      u"self.email = 'admin@gov.gov'"]],
 #                                                                                                   'refspec': 'e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                   'src': 'admin.py'},
 #                                            u'e0e0aa800a4f2b0a9339614107828c67bd73a769:data_data_1_json': {'git_log': ['commit e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                                       'Author: Marc Esher <marc.esher@gmail.com>',
 #                                                                                                                       'Date:   Mon Feb 24 16:35:51 2014 -0500',
 #                                                                                                                       'Adding a password to the file',
 #                                                                                                                       '',
 #                                                                                                                       'Hey Jude',
 #                                                                                                                       '',
 #                                                                                                                       'My username = "thekid"'],
 #                                                                                                           'matched_lines': [[u'14',
 #                                                                                                                              u'"email": "dreyfusf@pp.pd.gov.fr"']],
 #                                                                                                           'refspec': 'e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                           'src': 'data/data_1.json'},
 #                                            u'e0e0aa800a4f2b0a9339614107828c67bd73a769:email_py': {'git_log': ['commit e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                               'Author: Marc Esher <marc.esher@gmail.com>',
 #                                                                                                               'Date:   Mon Feb 24 16:35:51 2014 -0500',
 #                                                                                                               'Adding a password to the file',
 #                                                                                                               '',
 #                                                                                                               'Hey Jude',
 #                                                                                                               '',
 #                                                                                                               'My username = "thekid"'],
 #                                                                                                   'matched_lines': [[u'10',
 #                                                                                                                      u'me = "my@email.com"'],
 #                                                                                                                     [u'11',
 #                                                                                                                      u'you = "your@email.com"']],
 #                                                                                                   'refspec': 'e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                   'src': 'email.py'},
 #                                            u'e0e0aa800a4f2b0a9339614107828c67bd73a769:pos_one_py': {'git_log': ['commit e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                                 'Author: Marc Esher <marc.esher@gmail.com>',
 #                                                                                                                 'Date:   Mon Feb 24 16:35:51 2014 -0500',
 #                                                                                                                 'Adding a password to the file',
 #                                                                                                                 '',
 #                                                                                                                 'Hey Jude',
 #                                                                                                                 '',
 #                                                                                                                 'My username = "thekid"'],
 #                                                                                                     'matched_lines': [[u'26',
 #                                                                                                                        u"self.email = 'admin@gov.gov'"]],
 #                                                                                                     'refspec': 'e0e0aa800a4f2b0a9339614107828c67bd73a769',
 #                                                                                                     'src': 'pos_one.py'}},
 #
 #                                         }