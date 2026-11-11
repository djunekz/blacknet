[app]
title = BLACKNET
package.name = blacknet
package.domain = org.djunekz
source.dir = .
source.include_exts = py,json,txt,ttf,png
source.exclude_dirs = tests,docs,tools,bin,.github,.buildozer,__pycache__
source.exclude_patterns = data/player.json,data/profile.json,data/world_cache.json,data/world.json,data/jobs_taken.json,data/jobs_done.json,data/logs_*,data/persist_*,data/creds_*,data/reports/*
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/core/version.py
requirements = python3,kivy==2.3.0,certifi
orientation = portrait
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
android.presplash_color = #070B14
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
p4a.branch = v2024.01.21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
