[app]

# --- Basic info ---
title = Mahiru Chat
package.name = mahiruchat
package.domain = org.mahiru
version = 0.1

# --- Source ---
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf

# --- Assets ---
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/arka_pan.jpg

# --- Requirements ---
# Pin specific versions for a reproducible build.
# kivymd must match the kivy version you use.
requirements = kivy==2.3.0,kivymd==1.2.0,pillow,certifi

# --- Orientation & display ---
orientation = portrait
fullscreen = 1

# --- Android SDK/NDK ---
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

# --- Permissions ---
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# --- Build optimisations ---
android.release_artifact = apk

[buildozer]
log_level = 1
warn_on_root = 1
