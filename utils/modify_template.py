#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import quote

def modify_poc_template(words):
    if words['info_post_data']:
        try:
            data_dict = dict([x.split('=', 1) for x in words['info_post_data'].split('&')])
            words['info_post_data'] = u'payload = {data}\n        response = req.post(self.url + target_url, data=payload, timeout=10)'.format(data=data_dict)
        except ValueError:
            words['info_post_data'] = u'payload = {data}\n        response = req.post(self.url + target_url, data=payload, timeout=10)'.format(data='')
    else:
        words['info_post_data'] = u'\n        response = req.get(self.url + target_url, timeout=10)'
    if words['info_match']:
        words['info_match'] = u'\n        match = re.search(\'{match}\', content)'.format(match=words['info_match'])
    if words['info_other_match']:
        words['info_other_match'] = u'match_other = re.search(\'{match}\', content)\n\n        if match and match_other:'.format(match=words['info_other_match'])
    else:
        words['info_other_match'] = u'\n        if match:'
    if words['info_target_url']:
        target_url = words['info_target_url']
        if ' ' in target_url:
            target_url = quote(target_url)
        if words['info_test_url']:
            if target_url.startswith(words['info_test_url']):
                target_url = target_url[len(words['info_test_url']):]
        elif target_url.startswith('http'):
            target_url = '/'.join(target_url.split('/')[3:])
        if target_url[0] != '/':
            target_url = '/' + target_url
        words['info_target_url'] = target_url
    if words['vuldesc']:
        blank = ' ' * 11
        vuldesc = words['vuldesc'].encode('gbk')
        n = 71 if len(vuldesc) % 2 else 70 # 喝喝
        result = [blank + vuldesc[i:i+n] for i in range(0, len(vuldesc), n)]
        words['vuldesc'] = '\n'.join(result).decode('gbk')
