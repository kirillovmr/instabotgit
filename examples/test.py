import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '../'))
import my_get_settings

settings = my_get_settings.get_settings(1)
print(settings)
