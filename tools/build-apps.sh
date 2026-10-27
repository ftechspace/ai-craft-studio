#!/bin/sh
# Release-build each Craft app (desktop app + CLI). Usage: sh tools/build-apps.sh [app ...]
# Logs to output/build-logs/<app>.log. Run after `git pull` in apps/.
# Running exes (e.g. MCP servers) lock their files on Windows, but a running exe can be renamed:
# move them aside first so the link step can write the new ones; stale copies are deleted when free.
cd "$(dirname "$0")/.." || exit 1
mkdir -p output/build-logs
apps=${*:-"soundcraft effectcraft vectorcraft photocraft lightcraft designcraft figcraft filmcraft"}
for a in $apps; do
  start=$(date +%s)
  rel="apps/$a/target/release"
  rm -f "$rel"/*.exe.old-* 2>/dev/null
  for e in "$a" "$a-cli"; do [ -f "$rel/$e.exe" ] && mv "$rel/$e.exe" "$rel/$e.exe.old-$start" 2>/dev/null; done
  extra=""; [ "$a" = filmcraft ] && extra="--example contact"
  if (cd "apps/$a" && ~/.cargo/bin/cargo build --release -p "$a" -p "$a-cli" $extra) > "output/build-logs/$a.log" 2>&1
  then
    # cargo skips linking when nothing changed, so an exe moved aside is not re-created: put it back
    for e in "$a" "$a-cli"; do [ ! -f "$rel/$e.exe" ] && [ -f "$rel/$e.exe.old-$start" ] && cp "$rel/$e.exe.old-$start" "$rel/$e.exe"; done
    echo "OK   $a ($(( $(date +%s) - start ))s)"
  else
    echo "FAIL $a (see output/build-logs/$a.log)"
    for e in "$a" "$a-cli"; do [ ! -f "$rel/$e.exe" ] && [ -f "$rel/$e.exe.old-$start" ] && mv "$rel/$e.exe.old-$start" "$rel/$e.exe"; done
  fi
done
