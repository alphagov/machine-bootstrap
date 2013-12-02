#!/usr/bin/env python
from fabric.api import (abort, env, get, hide, local, puts, run, runs_once,
                            settings, sudo, task, warn)

import bootstrap
