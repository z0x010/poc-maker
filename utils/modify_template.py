#!/usr/bin/env python
# -*- coding: utf-8 -*-


def modify_poc_template(dict):
    if dict['info_post_data']:
        dict['info_post_data'] = u'payload = \'{data}\'\n        response = req.post(self.url + target_url, data=payload, timeout=10)'.format(data=dict['info_post_data'])
    else:
        dict['info_post_data'] = u'\n        response = req.get(self.url + target_url, timeout=10)'
    if dict['info_match']:
        dict['info_match'] = u'\n        match = re.search(\'{match}\', content)'.format(match=dict['info_match'])
    if dict['info_other_match']:
        dict['info_other_match'] = u'match_other = re.search(\'{match}\', content)\n\n        if match and match_other:'.format(match=dict['info_other_match'])
    else:
        dict['info_other_match'] = u'\n        if match:'
