[app]
title = Para Valentina
package.name = paravalentina
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

orientation = portrait
osx.kivy_version = Newest
fullscreen = 1

android.api = 33
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 33.0.1
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
