# TogglWarrior

TogglWarrior is a hook for [TaskWarrior](https://taskwarrior.org/) to enable time tracking functionality. It automatically syncs the current task in TaskWarrior with a time entry in [Toggl Track](https://toggl.com), a popular time tracking tool.

## Features

- Starts a new time entry in Toggl Track with the description and project of the started task in TaskWarrior
- Stops the current time entry when the corresponding task is stopped in TaskWarrior
- Modifies the project or description of the time entry in Toggl Track when it's modified in TaskWarrior

Note that TogglWarrior only syncs tasks with a non-empty project that exists within the Toggl Track workspace. Additionally, TogglWarrior only permits a single running synced task at any given time.

## Requirements

- Python 3
- [Toggl-CLI](https://github.com/AuHau/toggl-cli)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/polyntsov/togglwarrior.git
```

3. Set up Toggl-CLI following the instructions in their repository: https://github.com/AuHau/toggl-cli#install

4. Copy the `on-modify-toggl-sync.py` file to the TaskWarrior hooks directory:

```bash
cp on-modify-toggl-sync.py ~/.task/hooks/
```

## Configuration

TogglWarrior relies on Toggl-CLI to interact with Toggl Track. Currently, Toggl-CLI's default `~/.togglrc` is the only supported configuration file. If you have already set up Toggl-CLI, you don't need to do anything else.

You can create a configuration file by running any `toggl` command for the first time (it will prompt an interactive configuration). For example:
```bash
toggl projects ls
```

## Usage

Start a task in TaskWarrior as you would normally:

```bash
task start task_id
```
TogglWarrior will automatically start a time entry in Toggl Track with the description and the project of task\_id task.

When you stop this task in TaskWarrior:
```bash
task stop task_id
```
TogglWarrior will stop current time entry in Toggl Track.

If you modify the project or description of this task in TaskWarrior when it's running:
```bash
task modify task_id project:new_project description:new_description
```
TogglWarrior will modify current time entry in Toggl Track with the new project and/or description.

## License

TogglWarrior is licensed under the MIT License. See LICENSE for more information.
