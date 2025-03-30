import os
import sys
from datetime import datetime

from invoke import Collection, task

CONTAINER_NAME = "django"
DB_CONTAINER = "postgres"
DB_NAME = "elodrinks_db"
DB_USER = "postgres"
BACKUP_DIR = "backups"


@task
def run(c: Collection, daemon: bool = False, debug: bool = False, debug_vscode: bool = False):
    """Run the local Docker stack

    :param c: The Invoke context, which is used to run the command.
    :param daemon: If True, runs the stack in detached mode.
    :param debug: If True, enables PyCharm remote debugging.
    :param debug_vscode: If True, enables VSCode remote debugging.
    """
    env_vars = []
    if debug:
        env_vars.append("DEBUG_PYCHARM=1" if sys.platform != "win32" else "set DEBUG_PYCHARM=1 &&")
    elif debug_vscode:
        env_vars.append("DEBUG_VSCODE=1" if sys.platform != "win32" else "set DEBUG_VSCODE=1 &&")

    cmd = f"{' '.join(env_vars)} docker compose -f docker-compose.yaml up {'-d' if daemon else ''}"
    c.run(cmd)


@task
def build(c: Collection, daemon: bool = False, up: bool = False):
    """Build the local Docker stack

    :param c: The Invoke context, which is used to run the command.
    :param daemon: If True, runs the stack in detached mode.
    :param up: If True, runs `docker compose up --build` to build and start the stack.
    """
    cmd = f"docker compose -f docker-compose.yaml build {' -q' if daemon else ''}"
    c.run(cmd)

    if up:
        run(c, daemon=daemon)

    c.run(cmd)


@task
def down(c: Collection):
    """Stop and remove the local Docker stack

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = "docker compose -f docker-compose.yaml down"
    c.run(cmd)


@task
def kill(c: Collection):
    """Kill the local Docker stack

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = "docker compose -f docker-compose.yaml kill"
    c.run(cmd)


@task()
def fresh_restart(c: Collection, ignore_system_prune: True = True, backup_file: True = None):
    """Kill, remove, rebuild, and restart the local Docker stack, and restore the database from a backup.

    :param c: The Invoke context, which is used to run the command.
    :param ignore_system_prune: If False, runs `docker system prune` to clean up unused Docker data
    (affect all Docker data, use with caution).
    :param backup_file: The name of the backup file to restore from (must be inside the `backups` directory).
    """
    print("🛑 Killing existing containers...")
    kill(c)

    if not ignore_system_prune:
        print("🧹 Cleaning up unused Docker data...")
        c.run("docker system prune -f")
    else:
        print("🔴 Removing Docker containers, images, volumes and networks...")
        c.run("docker compose -p brsc-core-connect down --rmi all -v")

    print("🔨 Rebuilding the Docker stack...")
    build(c, daemon=True, up=True)

    print("⚙️ Running Django migrations...")
    migrate(c)

    if backup_file:
        restore(c, backup_file)
    else:
        print("⚠️ No backup file provided. Skipping database restore.")

    print("🔄 Restarting the stack...")
    kill(c)

    print("✅ Fresh restart completed.")


@task
def makemigrations(c: Collection):
    """Run Django migrations inside the container

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = f"docker exec {CONTAINER_NAME} python /code/manage.py makemigrations"
    c.run(cmd)


@task
def migrate(c: Collection):
    """Apply Django migrations inside the container

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = f"docker exec {CONTAINER_NAME} python /code/manage.py migrate"
    c.run(cmd)


@task
def backup(c: Collection, clear: bool = True):
    """Create a backup of the database

    :param c: The Invoke context, which is used to run the command.
    :param clear: If True, deletes the backup file from the container after copying it.
    """
    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{BACKUP_DIR}/backup_{timestamp}.bkp"
    container_backup_path = "/var/lib/postgresql/backup.bkp"

    print(f"📦 Creating backup: {backup_file}")

    cmd = (
        f"docker exec -u {DB_USER} {DB_CONTAINER} pg_dump -F c -d {DB_NAME} -f {container_backup_path} && "
        f"docker cp {DB_CONTAINER}:{container_backup_path} {backup_file}"
    )

    if clear:
        cmd += f" && docker exec -u {DB_USER} {DB_CONTAINER} rm {container_backup_path}"

    c.run(cmd)
    print("✅ Backup completed.")


@task
def restore(c, file_name, clear=True):
    """Restore the database from a backup file

    :param c: The Invoke context, which is used to run the command.
    :param file_name: The name of the backup file to restore (must be inside the `backups` directory).
    :param clear: If True, deletes the restore file from the container after restoring it.
    """
    backup_path = os.path.join(BACKUP_DIR, file_name)
    container_restore_path = "/var/lib/postgresql/restore.bkp"

    if not os.path.exists(backup_path):
        print(f"❌ Backup file not found: {backup_path}")
        return

    print(f"🔄 Restoring database from: {backup_path}")

    c.run(f"docker cp {backup_path} {DB_CONTAINER}:{container_restore_path}")

    cmd = (
        f"docker exec -u {DB_USER} {DB_CONTAINER} pg_restore -d {DB_NAME} "
        f"--clean --if-exists {container_restore_path}"
    )

    if clear:
        cmd += f" && docker exec -u {DB_USER} {DB_CONTAINER} rm {container_restore_path}"

    c.run(cmd)
    print("✅ Restore completed.")


@task
def flake8(c: Collection):
    """Execute flake8 against code

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = "flake8 ."
    c.run(cmd)


@task
def black(c: Collection):
    """Execute black against code

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = "black ."
    c.run(cmd)


@task
def isort(c: Collection):
    """Execute isort against code

    :param c: The Invoke context, which is used to run the command.
    """
    cmd = "isort ."
    c.run(cmd)


@task(default=True)
def pytest(c, file_path=None, keyword=None, marker=None, debug=False, serial=False):
    """Execute pytest to run tests

    :param c: The Invoke context, which is used to run the command.
    :param file_path: The specific test file to run (relative to the code directory).
    :param keyword: A keyword expression to filter tests.
    :param marker: A marker expression to filter tests.
    :param debug: If True, runs tests with `pudb` for debugging.
    :param serial: If True, runs the tests in a single thread.
    """
    cmd = ["pytest"]
    if file_path:
        cmd.append(file_path.replace("./code/", ""))
    if keyword:
        cmd.append("-k")
        cmd.append(keyword)
    if marker:
        cmd.append("-m")
        cmd.append(marker)
    if debug:
        cmd.append("-n 0")
        cmd.append("--pudb")
    if serial:
        cmd.append("-n 0")
    c.run(" ".join(cmd))


docker = Collection("docker", run, down, kill, build, fresh_restart)
django = Collection("django", makemigrations, migrate)
db = Collection("db", backup, restore)
lint = Collection("lint", flake8, black, isort)
test = Collection("test", pytest)

namespace = Collection(docker, django, db, lint, test)
