#!/usr/bin/env python
from fabric import state
from fabric.api import (abort, env, get, hide, local, puts, run, runs_once,
                            settings, sudo, task, warn)
from fabric.task_utils import crawl

import textwrap

import bootstrap

@task
def help(name):
    """Show extended help for a task (e.g. 'fab help:bootstrap.changepassword')"""
    task = crawl(name, state.commands)

    if task is None:
        abort("%r is not a valid task name" % task)

    puts(textwrap.dedent(task.__doc__).strip())
