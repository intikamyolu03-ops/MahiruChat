# Mahiru Chat – Android APK

A KivyMD chat app with login/register, friend search, and profile management.

---

## Project files

| File | Purpose |
|---|---|
| `main.py` | App entry point (KivyMD) |
| `chat.kv` | UI layout |
| `server.py` | Python TCP server – run on your own PC/VPS |
| `buildozer.spec` | Android build configuration |
| `icon.png` | App icon |
| `arka_pan.jpg` | Splash / background image |
| `varsayilan_avatar.png` | Default user avatar |

---

## How to build the APK (two options)

### Option A – GitHub Actions (recommended, no local setup needed)

1. Create a new **public or private** GitHub repository.
2. Drag all files in this folder into that repo (or use `git push`).
3. Go to **Actions → Build Mahiru Chat APK → Run workflow**.
4. Wait ~20–30 minutes for the first build (cached builds take ~5 min).
5. When it finishes, click the run → **Artifacts** → download `mahiru-chat-debug.apk`.
6. Transfer the APK to your phone and install it  
   *(Settings → Security → Install unknown apps → enable for your browser or Files app)*.

> The `.github/workflows/build-apk.yml` file is already included and configured.

---

### Option B – Build locally with Docker (no Android Studio needed)

Requires Docker installed on your PC.

```bash
# 1. Pull the official Kivy/Buildozer image
docker pull kivy/buildozer

# 2. Run buildozer inside the container
docker run --volume "$(pwd)":/home/user/hostcwd \
           --workdir /home/user/hostcwd \
           kivy/buildozer \
           android debug

# 3. Your APK will appear in ./bin/
```

---

## Running the server

The Android app tries to connect to `127.0.0.1:55555`.  
For real network play, update the IP in `main.py` and run `server.py` on any machine with Python 3:

```bash
pip install -r requirements-server.txt   # just stdlib – no extra packages
python server.py
```

Then change this line in `main.py`:
```python
self.client.connect(('YOUR_SERVER_IP', 55555))
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Build fails with `SDK license not accepted` | Already handled by `android.accept_sdk_license = True` in the spec |
| `kivymd` import error | Make sure the version in `requirements` matches: `kivy==2.3.0,kivymd==1.2.0` |
| App crashes on Android < 5.0 | `android.minapi = 21` already covers Android 5.0+ |
| Phone says "App not installed" | Enable *Install unknown apps* in phone Settings |
