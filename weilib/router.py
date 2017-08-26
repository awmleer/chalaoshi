#!/usr/bin/env python
# weilib/router.py - router handlers for weilib
# include router function and router pattern response
# ver 0.1 by winkidney 2014.05.10

import re
import os
import logging
from weilib.handlers import default_handler
from weilib.models import (DBTextMsg, PatternT2T, DBImgTextMsg, PatternT2PT,
                           PatternE2PT, PatternE2T)
from weilib.lib import text_response, pic_text_response, PicTextMsg, PTItem


def base_router(recv_msg, router_patterns):
    for type, key, handler in router_patterns:
        if recv_msg.msg_type == 'text' and type == recv_msg.msg_type:
            match = re.search(key, recv_msg.content)
            if match:
                return handler(recv_msg)
        elif recv_msg.msg_type == 'event' and type.find(recv_msg.msg_type) >= 0 and type.find(recv_msg.event) >= 0:
            match = re.search(key, recv_msg.event_key)
            if match:
                return handler(recv_msg)
        elif recv_msg.msg_type == type:
            return handler(recv_msg)

def new_msg_from_db(pattern):
    """Convert PicTextMsg from db to PicTextMsg object for rendering"""
    items = []
    for item in pattern.handler.all():
        items.append(
            PTItem(item.title, item.description, item.pic_url, item.url))
    return items


def db_router(recv_msg, *args):
    if recv_msg.msg_type == 'text':
        for pattern in PatternT2T.objects.all():
            match = re.search(
                pattern.content.encode('utf-8'), recv_msg.content)
            if match:
                return text_response(recv_msg, pattern.handler.content)

        for pattern in PatternT2PT.objects.all():
            match = re.search(
                pattern.content.encode('utf-8'), recv_msg.content)
            if match:
                return pic_text_response(recv_msg, new_msg_from_db(pattern))

    if recv_msg.msg_type == 'event':
        for pattern in PatternE2T.objects.all():

            if pattern.event == recv_msg.event:
                if recv_msg.event_key:
                    match = re.search(
                        pattern.event_key.encode('utf-8'), recv_msg.event_key)
                    if match:
                        return text_response(recv_msg, pattern.handler.content)
                else:
                    return text_response(recv_msg, pattern.handler.content)

        for pattern in PatternE2PT.objects.all():
            if pattern.event == recv_msg.event:
                if recv_msg.event_key:
                    match = re.search(
                        pattern.event_key.encode('utf-8'), recv_msg.event_key)
                    if match:
                        return pic_text_response(recv_msg, new_msg_from_db(pattern))
                else:
                    return pic_text_response(recv_msg, new_msg_from_db(pattern))
