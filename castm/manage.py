#!/usr/bin/env python

if __name__ == "__main__":
    
    from socket import gethostname 
    host_name = gethostname()
    
    import os
    if host_name is "castm":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "castm.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "castm.development")
    
    import sys    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
