from django.apps import AppConfig
import socket, sys, os
import logging
# import threading
import _thread
# import time
# from serverlist.models import *
# from serverlist.scan_module import *
# from serverlist.scan_module import scan_repeater


class MyAppConfig(AppConfig):
    logging.basicConfig(level=logging.ERROR)
    name = 'serverlist'
    verbose_name = "My Application"

    def ready(self):
        pass

    # def ready(self):
    #     try:
    #         _thread.start_new_thread(scan_repeater.continuous_scan, ())
    #         pass
    #     except Exception as e:
    #         logging.exception(str(e))
    #         sys.exit(0)
