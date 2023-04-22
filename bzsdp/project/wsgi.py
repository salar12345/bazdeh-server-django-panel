"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from ncl.utils.config.configuration import Configuration
from ncl.utils.config.base_config import ConfigConstants

from bzsdp.project.config import BZSDPConfig
Configuration.configure(BZSDPConfig, alternative_env_search_dir=__file__)
settings = 'bzsdp.project.settings_prod'
if BZSDPConfig.is_development_env():
    settings = 'bzsdp.project.settings_dev'
elif BZSDPConfig.RUN_ENV_TYPE == ConfigConstants.RUN_ENV_TYPE_STAGE:
    settings = "bzsdp.project.settings_stage"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()
