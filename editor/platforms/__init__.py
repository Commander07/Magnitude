## Platform specifc code
import os
if os.name == "nt":
  from .windows import *
else:
  from .linux import *
