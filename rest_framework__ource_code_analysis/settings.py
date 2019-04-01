"""
Django settings for rest_framework__ource_code_analysis project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j64h^v78*cw5-pis*$askt+oz=_7v935%jbz4gysd3!amk&#q-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rest_framework__ource_code_analysis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rest_framework__ource_code_analysis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rest_framework',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # 全局使用的认证类
    "DEFAULT_AUTHENTICATION_CLASSES": ['app01.utils.auth.Authentication', ],
    # 匿名用户设置
    # "UNAUTHENTICATED_USER": lambda :"匿名用户"
    "UNAUTHENTICATED_USER": None,           #推荐使用，匿名，因为request.user = None
    "UNAUTHENTICATED_TOKEN": None,          # 匿名，因为request.auth = None

    # 全局权限类
    "DEFAULT_PERMISSION_CLASSES": ['app01.utils.permission.SvipPermission', ],

    # 版本配置类
    "DEFAULT_VERSIONING_CLASS": 'rest_framework.versioning.URLPathVersioning',
    "DEFAULT_VERSION": 'v1',         # 默认版本
    "ALLOWED_VERSIONS": ['v1', 'v2'],  # 允许版本
    "VERSION_PARAM": 'version',      # 版本参数

    # 解析器配置
    "DEFAULT_PARSER_CLASSES": ['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser'],

    # 分页
    "DEFAULT_PAGINATION_CLASS": ['rest_framework.pagination.LimitOffsetPagination', ],
    "PAGE_SIZE": 2,

    # 渲染器
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer',
                                 'rest_framework.renderers.BrowsableAPIRenderer'],
    # 访问频率控制
    'DEFAULT_THROTTLE_CLASSES': ['app01.utils.throttle.UserThorttle', ],
    'DEFAULT_THROTTLE_RATES': {
        'Lufei': '3/m',  # 匿名用户配置 一分钟三次
        'LufeiUser': '3/m',  # 用户配置 一分钟三次
    }
}