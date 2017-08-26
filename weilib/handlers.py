#!/usr/bin/env python
#weilib/handlers.py - router handlers for weilib
#ver 0.1 by winkidney 2014.05.10

from .lib import text_response

def default_handler(recv_msg):
    return text_response(recv_msg, "咦？你刚才输了什么...")
   


