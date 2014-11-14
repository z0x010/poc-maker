#!/usr/bin/env python
# -*- coding: utf-8 -*-

def modify_poc_template(words):
    if words['info_post_data']:
        data_dict = dict([x.split('=' , 1) for x in words['info_post_data'].split('&')])
        words['info_post_data'] = u'payload = {data}\n        response = req.post(self.url + target_url, data=payload, timeout=10)'.format(data=data_dict)
    else:
        words['info_post_data'] = u'\n        response = req.get(self.url + target_url, timeout=10)'
    if words['info_match']:
        words['info_match'] = u'\n        match = re.search(\'{match}\', content)'.format(match=words['info_match'])
    if words['info_other_match']:
        words['info_other_match'] = u'match_other = re.search(\'{match}\', content)\n\n        if match and match_other:'.format(match=words['info_other_match'])
    else:
        words['info_other_match'] = u'\n        if match:'
