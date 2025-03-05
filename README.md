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
- [Poetry](https://python-poetry.org/docs/)
- (Optional) `wsl-notify-send` for Windows notifications inside WSL2

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/pomo-tracker.git
   cd pomo-tracker
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Initialize the database:
   ```bash
   poetry run init-db
   ```
4. Start using the CLI:
   ```bash
   poetry run taskcli --help
   ```

## Usage

### Task Management

#### Add a task

```bash
poetry run taskcli task add "Write documentation" Work
```
#### Show tasks

```bash
poetry run taskcli task show
```
#### Complete a task

```bash
poetry run taskcli task complete 1
```
#### Delete a task

```bash
poetry run taskcli task delete 1
```

### Time Tracking

#### Start tracking a task

```bash
poetry run taskcli tracker start 1
```
#### Start tracking with an alarm

```bash
poetry run taskcli tracker start 1 --timer 25 --recurring
```
#### Stop tracking

```bash
poetry run taskcli tracker stop 1
```
#### Show active timers

```bash
poetry run taskcli tracker active
```

### Alarms

#### Set an alarm

```bash
poetry run taskcli alarm start 5
```
#### List active alarms

```bash
poetry run taskcli alarm list
```
#### Stop an alarm

```bash
poetry run taskcli alarm stop 1
```
#### Stop all alarms

```bash
poetry run taskcli alarm stop_all
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

Pomo Tracker uses `wsl-notify-send` for alarm notifications on WSL2. Install it with:

```bash
winget install wsl-notify-send
```

If `wsl-notify-send` is not available, the CLI will print alerts instead.

## Future Improvements

- Export task reports
- GUI integration
- Sync with online calendars

## License

This project is licensed under the MIT License.

---

Happy tracking! 🚀

