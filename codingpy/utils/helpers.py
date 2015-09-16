#!usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
from flask import current_app, request, url_for


def baidu_ping(url):
    """
    :ref: http://zhanzhang.baidu.com/tools/ping

    发送给百度Ping服务的XML-RPC客户请求需要包含如下元素：
    RPC端点： http://ping.baidu.com/ping/RPC2
    调用方法名： weblogUpdates.extendedPing
    参数： (应按照如下所列的相同顺序传送)
    博客名称
    博客首页地址
    新发文章地址
    博客rss地址
    """

    result = 1
    rpc_server = xmlrpclib.ServerProxy('http://ping.baidu.com/ping/RPC2')

    try:
        # 返回0表示提交成功
        current_app.logger.info('begin to ping baidu: <%s>' % url)
        result = rpc_server.weblogUpdates.extendedPing(
            current_app.config.get('SITE_NAME'),
            url_for('main.index', _external=True),
            url,
            url_for('main.feed', _external=True)
        )
    except:
        pass

    if result != 0:
        current_app.logger.warning('<%s> ping to baidu failed' % url)

    return result == 0