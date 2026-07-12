name: Build Mahiru Chat APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:   # lets you trigger the build manually from GitHub

jobs:
  build:
    runs-on: ubuntu-22.04
    timeout-minutes: 90

    steps:
      # ── 1. Checkout ────────────────────────────────────────────────────────
      - name: Checkout code
        uses: actions/checkout@v4

      # ── 2. Python 3.13.3 Kurulumu ──────────────────────────────────────────
      - name: Set up Python 3.13.3
        uses: actions/setup-python@v5
        with:
          python-version: '3.13.3'

      # ── 3. System dependencies ────────────────────────────────────────────
      - name: Install system dependencies
        run: |
          sudo dpkg --add-architecture i386
          sudo apt-get update -qq
          sudo apt-get install -y --no-install-recommends \
            git zip unzip openjdk-17-jdk \
            python3-setuptools python3-virtualenv \
            libffi-dev libssl-dev \
            build-essential ccache \
            autoconf automake libtool \
            libltdl-dev libgl1-mesa-dev libgles2-mesa-dev \
            libncurses5 libncurses5:i386 libstdc++6 libstdc++6:i386 \
            libz1 libz1:i386

      # ── 4. Python / Buildozer ─────────────────────────────────────────────
      - name: Install Buildozer and Cython
        run: |
          python -m pip install --upgrade pip
          python -m pip install --user buildozer cython
          # Buildozer komutunun sistem tarafından tanınması için PATH'e ekliyoruz
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      # ── 5. Buildozer cache (speeds up repeated builds significantly) ───────
      - name: Cache Buildozer global directory
        uses: actions/cache@v4
        with:
          path: ~/.buildozer
          key: buildozer-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}
          restore-keys: |
            buildozer-${{ runner.os }}-

      # ── 6. Build the APK ──────────────────────────────────────────────────
      - name: Build APK
        run: buildozer android debug
        env:
          JAVA_HOME: /usr/lib/jvm/java-17-openjdk-amd64

      # ── 7. Upload the APK as a downloadable artifact ──────────────────────
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: mahiru-chat-debug
          path: bin/*.apk
          retention-days: 30