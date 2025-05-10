# flywayApp/apps.py

import os
import subprocess
import shutil
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class FlywayappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "flywayApp"

    def ready(self):
        # Hook into Django’s post_migrate signal
        post_migrate.connect(self.run_flyway, sender=self)

    def run_flyway(self, **kwargs):
        # Absolute path to flyway.conf
        project_root = settings.BASE_DIR                  # e.g. D:\flyway
        conf_file    = os.path.join(project_root, "flyway", "conf", "flyway.conf")
        conf_dir     = os.path.dirname(conf_file)         # D:\flyway\flyway\conf

        # Locate the Flyway CLI executable on Windows or *nix
        flyway_exec = (
            shutil.which("flyway")    
            or shutil.which("flyway.cmd")  # Windows
            or shutil.which("flyway.bat")
        )
        if not flyway_exec:
            print(
                "❌ Flyway CLI not found. "
                "Please install it and add its bin folder to your PATH.",
                file=os.sys.stderr,
            )
            return

        cmd = [
            flyway_exec,
            f"-configFiles={conf_file}",
            "migrate",
        ]

        try:
            # Run from the conf directory so that '../sql' → 'flyway/sql'
            subprocess.run(cmd, cwd=conf_dir, check=True)
            print("✅ Flyway migrations applied")     
        except subprocess.CalledProcessError as e:
            print(f"❌ Flyway migrate failed:\n{e}", file=os.sys.stderr)
            raise
