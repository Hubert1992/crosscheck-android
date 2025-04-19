[app]
# --- podstawowe dane aplikacji ---
title = Cross check
package.name = crosscheck
package.domain = org.example

# --- źródła i wersja ---
source.dir = .
source.include_exts = py,kv,json
version = 1.0

# --- zależności i uprawnienia ---
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET

[buildozer]
# (opcjonalnie można wskazać ścieżki do SDK/NDK, ale nie jest to konieczne)
# android.sdk_path =
# android.ndk_path =
