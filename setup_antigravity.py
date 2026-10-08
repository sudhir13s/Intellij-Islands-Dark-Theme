#!/usr/bin/env python3
"""Set up Antigravity (or another VS Code fork) for this theme in one command.

Installs the theme package, removes extensions whose grammars fight the theme (Pylance),
installs BasedPyright for Python code intelligence, and merges the editor settings the
theme relies on. Everything it applies lives in editor/antigravity-setup.json; the CLI and
settings paths can be overridden with ANTIGRAVITY_CLI and ANTIGRAVITY_SETTINGS.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, "editor", "antigravity-setup.json")
CLI_ENV = "ANTIGRAVITY_CLI"
SETTINGS_ENV = "ANTIGRAVITY_SETTINGS"


class SetupError(Exception):
    """A setup step could not complete; the message says which and why."""


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        config = json.load(config_file)
    config["cli"] = os.environ.get(CLI_ENV, config["cli"])
    config["settingsFile"] = os.path.expanduser(os.environ.get(SETTINGS_ENV, config["settingsFile"]))
    return config


def run_cli(cli, *arguments):
    result = subprocess.run([cli, *arguments], capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise SetupError(f"{os.path.basename(cli)} {' '.join(arguments)} failed: {result.stderr.strip()}")
    return result.stdout


def theme_package_path():
    with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    package_path = os.path.join(ROOT, f"{manifest['name']}-{manifest['version']}.vsix")
    if not os.path.exists(package_path):
        raise SetupError(f"{os.path.basename(package_path)} not found; run build_vsix.py first")
    return package_path


def sync_extensions(config):
    cli = config["cli"]
    if not os.path.exists(cli):
        raise SetupError(f"editor CLI not found at {cli}; set {CLI_ENV}")
    installed = {line.strip().lower() for line in run_cli(cli, "--list-extensions").splitlines()}
    for extension_id in config["uninstallExtensions"]:
        if extension_id.lower() in installed:
            run_cli(cli, "--uninstall-extension", extension_id)
            print(f"removed   {extension_id}")
    for extension_id in config["installExtensions"]:
        if extension_id.lower() not in installed:
            run_cli(cli, "--install-extension", extension_id)
            print(f"installed {extension_id}")
    package_path = theme_package_path()
    run_cli(cli, "--install-extension", package_path, "--force")
    print(f"installed {os.path.basename(package_path)}")


def merge_settings(config):
    settings_path = config["settingsFile"]
    settings = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, encoding="utf-8") as settings_file:
                settings = json.load(settings_file)
        except json.JSONDecodeError as error:
            raise SetupError(f"{settings_path} is not plain JSON (comments?): {error}") from error
        backup_path = os.path.join(tempfile.gettempdir(), f"antigravity-settings-{int(time.time())}.json")
        shutil.copyfile(settings_path, backup_path)
        print(f"backup    {backup_path}")
    for key in config["removeSettings"]:
        if settings.pop(key, None) is not None:
            print(f"dropped   {key}")
    settings.update(config["settings"])
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, "w", encoding="utf-8") as settings_file:
        json.dump(settings, settings_file, indent=4)
        settings_file.write("\n")
    print(f"settings  {len(config['settings'])} applied to {settings_path}")


def main():
    config = load_config()
    try:
        sync_extensions(config)
        merge_settings(config)
    except SetupError as error:
        print(f"setup failed: {error}", file=sys.stderr)
        return 1
    print("done — run 'Developer: Reload Window' in the editor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
