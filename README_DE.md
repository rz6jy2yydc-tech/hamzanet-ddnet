# HamzaNet DDNet Custom Client v0.1 Builder

Das ist ein **sauberes, cheat-freies Testpaket** für einen eigenen DDNet-Client.
Es verändert nur Branding und HUD-Optik. Keine Bots, kein Aim, kein Hookbot, kein Movement-Hack, kein Bypass.

## Was v0.1 macht

- Clientname in `GAME_NAME`: `HamzaNet Client`
- größerer Game-Timer oben mittig
- kleines `HamzaNet v0.1` Wasserzeichen oben links im HUD
- Windows-Build-Workflow für GitHub Actions
- lokales Windows-Build-Skript als Alternative

## Wichtig ehrlich

Dieses Paket ist ein Builder/Patch. Es enthält nicht den kompletten DDNet-Sourcecode und keine fertige EXE.
Der Workflow lädt den offiziellen DDNet-Code, patcht ihn und versucht daraus automatisch eine Windows-ZIP zu bauen.

## Schnellster Test über GitHub

1. Neues leeres GitHub-Repository erstellen, z. B. `hamzanet-ddnet`.
2. Den Inhalt dieses ZIPs in das Repository hochladen.
3. In GitHub auf **Actions** gehen.
4. Workflow **Build HamzaNet Windows** starten.
5. Wenn fertig: bei **Artifacts** `HamzaNet-Windows` herunterladen.

## Lokaler Windows-Test

Wenn Visual Studio 2022 mit C++/CMake, Python und Rust installiert ist:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_hamzanet_windows.ps1
```

Die fertigen Dateien werden dann unter `out/` gesammelt, falls der Build klappt.

## Nächste Version

Wenn v0.1 baut und startet, kann v0.2 bekommen:
- echtes Custom-Menü
- besserer Chat-Look
- eigenes Logo/Bild
- HUD-Boxen transparent/dunkel
- mehr Einstellungen im Menü
