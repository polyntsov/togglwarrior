#!/usr/bin/env python3

import sys
import json
from toggl import api
from toggl.cli import helpers

def out_success(task):
    print(json.dumps(task))
    sys.exit(0)

def out_fail():
    sys.exit(1)

def toggl_current_entry():
    return api.TimeEntry.objects.current()

def toggl_find_project_by_name(project_name):
    return helpers.get_entity(api.Project, project_name, field_lookup=('id', 'name',))

def toggl_start(project, desc):
    cur_te = toggl_current_entry()
    if cur_te != None:
        print("There is already running time entry in toggl "
              f"with description '{cur_te.description}'!")
        out_fail()
    api.TimeEntry.start_and_save(project=project, description=desc)

def toggl_stop():
    cur_te = toggl_current_entry()
    if cur_te == None:
        print("There is no time entry running!")
        out_fail()
    cur_te.stop_and_save()

def do_start(project_name, desc):
    project = toggl_find_project_by_name(project_name)
    if project == None:
        print(f"There is no project named '{project_name}' in toggl, not syncing it!")
        return
    toggl_start(project, desc)

def do_stop(project, desc):
    cur_te = toggl_current_entry()
    if cur_te == None or cur_te.description != desc or cur_te.project.name != project:
        return
    toggl_stop()

def do_modify(project_name, desc, mod_project_name, mod_desc):
    cur_te = toggl_current_entry()
    if cur_te == None or cur_te.description != desc or cur_te.project.name != project_name:
        return
    if mod_project_name == None:
        print(f"Not modifying currently running entry by setting empty project!")
        out_fail()
    mod_project = toggl_find_project_by_name(mod_project_name)
    if mod_project == None:
        print(f"There is no project named '{project_name}' in toggl, "
              "can't change current entry project to it!")
        out_fail()
    cur_te.project = mod_project
    cur_te.description = mod_desc
    cur_te.save()

def main():
    old_task = json.loads(sys.stdin.readline())
    mod_task = json.loads(sys.stdin.readline())

    project, mod_project = None, None
    desc, mod_desc = old_task["description"], mod_task["description"]

    if "project" in old_task:
        project = old_task["project"]
    else:
        print("Not syncing an entry without a project with toggl!")
        out_success(mod_task)
    if "project" in mod_task:
        mod_project = mod_task["project"]

    if ('start' in mod_task):
        if 'start' not in old_task:
            do_start(project, desc)
        elif desc != mod_desc or project != mod_project:
            # modifying currently running task
            do_modify(project, desc, mod_project, mod_desc)

    elif ('start' in old_task and 'start' not in mod_task):
        do_stop(project, desc)

    out_success(mod_task)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e).strip())
        out_fail()
