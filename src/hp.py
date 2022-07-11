import matplotlib.pyplot as plt
#import numpy as np
import sys, os, json

class HandyPlotter:

    def __init__(self, *args):
        if len(args) == 0:
            return None
        elif len(args) == 1:
            try:
                with open(args[0]) as config_file:
                    self.config = json.load(config_file) 
            except Exception as err:
                sys.stderr.write("\n")
                raise Exception(f"Failed to load HandyPlotter config file\n({type(err)}): {err}")
        else:
            raise Exception(f"Failed to initialize a HandyPlotter object. Expected 0-1 arguments, got {len(args)}")