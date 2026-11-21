import subprocess
import time


PUSH_INTERVAL_SECONDS = 30 * 60
PUSH_SLOTS = 6
REMOTE = "origin"


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], encoding="utf-8").strip()


def push_session() -> int:
    branch = git_output("branch", "--show-current")
    if not branch.startswith("feature/"):
        print("Switch to a feature/* branch before starting the push session.", flush=True)
        return 1
    if REMOTE not in git_output("remote").splitlines():
        print("Add the shared GitHub repository as origin before starting.", flush=True)
        return 1

    branch_ref = f"refs/heads/{branch}"
    remote_ref = f"refs/remotes/{REMOTE}/{branch}"
    last_pushed = git_output("for-each-ref", "--format=%(objectname)", remote_ref)
    started_at = time.monotonic()
    print(f"Syncing {branch} to {REMOTE} at 30-minute intervals for three hours.", flush=True)

    for slot in range(1, PUSH_SLOTS + 1):
        deadline = started_at + slot * PUSH_INTERVAL_SECONDS
        time.sleep(max(0, deadline - time.monotonic()))
        if git_output("branch", "--show-current") != branch:
            print("The active branch changed. The push session has stopped.", flush=True)
            return 1

        commit = git_output("rev-parse", branch_ref)
        elapsed_minutes = slot * PUSH_INTERVAL_SECONDS // 60
        if commit == last_pushed:
            print(f"[{elapsed_minutes} min] No new commits.", flush=True)
            continue

        print(f"[{elapsed_minutes} min] Pushing {commit[:8]} on {branch}.", flush=True)
        try:
            result = subprocess.run(
                [
                    "git", "push", "--set-upstream", "--no-follow-tags",
                    "--recurse-submodules=no", REMOTE, f"{branch_ref}:{branch_ref}",
                ],
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            print("Push timed out. Check the connection and Git authentication.", flush=True)
            continue
        if result.returncode == 0:
            last_pushed = commit
        else:
            print("Push failed. Check the Git message above.", flush=True)

    if git_output("rev-parse", branch_ref) != last_pushed:
        print("The session ended with local commits awaiting a push.", flush=True)
        return 1
    print("The three-hour push session is complete.", flush=True)
    return 0


def main() -> int:
    try:
        return push_session()
    except FileNotFoundError:
        print("Install Git or add it to PATH, then run this script again.", flush=True)
        return 1
    except subprocess.CalledProcessError:
        return 1
    except KeyboardInterrupt:
        print("\nPush session stopped.", flush=True)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
