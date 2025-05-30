# Pomo Tracker

## Overview

Pomo Tracker is a simple CLI-based Pomodoro tracker and task manager designed to
help you stay productive. It allows you to manage tasks, track time spent on
them, and set alarms to keep you on schedule.

## Features

- Task management (add, delete, update, complete tasks)
- Time tracking for tasks
- Standalone alarms
- Recurring or one-time alarms
- Alarm notifications using `wsl-notify-send`
- Automatic alarm checking process

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/guides/install-python/)
- (Optional) `wsl-notify-send` for Windows notifications inside WSL2

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/pomo-tracker.git
   cd pomo-tracker
   ```
2. Install dependencies:
   ```bash
   uv install
   ```
3. Initialize the database:
   ```bash
   uv run init-db
   ```
4. Start using the CLI:
   ```bash
   uv run taskcli --help
   ```

## Usage

### Task Management

#### Add a task

```bash
uv run taskcli task add "Write documentation" Work
```
#### Show tasks

```bash
uv run taskcli task show
```
#### Complete a task

```bash
uv run taskcli task complete 1
```
#### Delete a task

```bash
uv run taskcli task delete 1
```

### Time Tracking

#### Start tracking a task

```bash
uv run taskcli tracker start 1
```
#### Start tracking with an alarm

```bash
uv run taskcli tracker start 1 --timer 25 --recurring
```
#### Stop tracking

```bash
uv run taskcli tracker stop 1
```
#### Show active timers

```bash
uv run taskcli tracker active
```

### Alarms

#### Set an alarm

```bash
uv run taskcli alarm start 5
```
#### List active alarms

```bash
uv run taskcli alarm list
```
#### Stop an alarm

```bash
uv run taskcli alarm stop 1
```
#### Stop all alarms

```bash
uv run taskcli alarm stop_all
```

## Architecture

### File Structure
```
├── src
│   ├── app.py              # Main CLI entrypoint
│   ├── database.py         # Database connection
│   ├── init_db.py          # Database schema setup
│   ├── tasks               # Task management module
│   ├── tracker             # Time tracking module
│   ├── alarm               # Alarm system module
│   ├── utils               # Utility functions
```

### Database Schema

- `tasks` (Task information)
- `categories` (Task categories)
- `time_tracking` (Task time tracking records)
- `alarms` (Alarms with status and recurrence options)

## Notifications

Pomo Tracker uses `wsl-notify-send` for alarm notifications on WSL2.

If `wsl-notify-send` is not available, the CLI will print alerts instead.

## Future Improvements

- Export task reports
- Todoist integration
- JIRA integration

## License

This project is licensed under the MIT License.

---

Happy tracking! 🚀

