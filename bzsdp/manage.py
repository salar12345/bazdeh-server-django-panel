#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from ncl.utils.config.base_config import ConfigConstants

from prometheus_client import start_http_server

from bzsdp.project.config import BZSDPConfig

def main():
    """Run administrative tasks."""

    settings = 'bzsdp.project.settings_prod'
    if BZSDPConfig.is_development_env():
        settings = 'bzsdp.project.settings_dev'
    elif BZSDPConfig.RUN_ENV_TYPE == ConfigConstants.RUN_ENV_TYPE_STAGE:
        settings = "bzsdp.project.settings_stage"

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from ncl.utils.config.configuration import Configuration

    Configuration.configure(BZSDPConfig, alternative_env_search_dir=__file__)
    main()
