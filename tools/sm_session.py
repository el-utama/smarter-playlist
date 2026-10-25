#!/usr/bin/env python3
"""SmarterPlaylights authenticated session manager.

Login once with Spotify (OAuth via /api/auth/login), persist the SmarterPlaylights
session cookie to ``auth/session.json``, and reuse it for all subsequent API calls
so the user never has to log in again until the session expires.

API endpoints used (reverse-engineered from the SmarterPlaylights v3.12.4 frontend
bundle):
    GET    /api/auth/login        - start Spotify OAuth (307 redirect)
    GET    /api/auth/me           - check whether session is valid
    POST   /api/auth/logout       - log out
    GET    /api/programs/enriched - list existing programs (pid + name)
    POST   /api/programs/         - create program {name, program_json}
    PUT    /api/programs/{pid}    - update program {name, program_json}
    POST   /api/programs/{pid}/run- run program (?save=true)
    GET    /api/runs/{run_id}/status - poll run status
"""

from __future__ import annotations

import json
import sys
import webbrowser
from pathlib import Path
from typing import Optional

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://smarterplaylists.playlistmachinery.com"
ROOT = Path(__file__).resolve().parents[1]
AUTH_DIR = ROOT / "auth"
SESSION_FILE = AUTH_DIR / "session.json"

# Cookie names that SmarterPlaylights typically sets after Spotify OAuth.
# We accept any non-Spotify cookie on the smarterplaylists domain.
SPOTIFY_COOKIE_PREFIXES = ("sp_", "Optanon")


class SmarterPlaylistsSession:
    """Thin wrapper around requests.Session with persistent cookie storage."""

    def __init__(self, base_url: str = BASE_URL, session_file: Path = SESSION_FILE):
        self.base_url = base_url.rstrip("/")
        self.session_file = session_file
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self._session: Optional[requests.Session] = None

    # ------------------------------------------------------------------ #
    # Session lifecycle
    # ------------------------------------------------------------------ #
    def load(self) -> requests.Session:
        """Return an authenticated requests.Session.

        If ``auth/session.json`` exists and passes ``/api/auth/me``, reuse it.
        Otherwise raise ``RuntimeError`` telling the user to run ``--init``.
        """
        if self._session is not None:
            return self._session

        sess = requests.Session()
        if self.session_file.exists():
            try:
                data = json.loads(self.session_file.read_text(encoding="utf-8"))
                cookies = data.get("cookies", {})
                for k, v in cookies.items():
                    sess.cookies.set(k, v, domain="smarterplaylists.playlistmachinery.com")
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[warn] could not load session file: {exc}")

        if self._is_authenticated(sess):
            self._session = sess
            return sess

        raise RuntimeError(
            "No valid SmarterPlaylights session found. "
            "Run: python tools/sm_session.py --init  (login once with Spotify)"
        )

    def init(self) -> None:
        """Interactive first-time login.

        Steps:
        1. Open /api/auth/login in the browser. This sets the oauth_state cookie
           in the browser AND redirects to the Spotify authorize URL.
        2. User completes Spotify login + authorization.
        3. Spotify redirects back to /api/auth/callback, which validates the
           oauth_state and sets a session cookie on
           smarterplaylists.playlistmachinery.com.
        4. User copies that session cookie (NOT open.spotify.com cookies).
        5. Cookie is validated against /api/auth/me and saved to disk.
        """
        login_url = f"{self.base_url}/api/auth/login"

        # Step 1: open /api/auth/login in the browser so the browser itself
        # receives the oauth_state cookie, then follows the redirect to Spotify.
        print("[1/4] Membuka halaman login SmarterPlaylights di browser:")
        print(f"   {login_url}")
        print("   Browser akan di-redirect otomatis ke Spotify untuk login + authorize.")
        webbrowser.open(login_url)

        # Step 2: wait for user to complete OAuth and paste session cookie.
        print("\n[2/4] Setelah selesai login di Spotify dan redirect KEMBALI ke smarterplaylights:")
        print("   • Tunggu hingga alamat browser kembali ke smarterplaylists.playlistmachinery.com")
        print("   • Buka DevTools (F12) > Application > Cookies")
        print("   • Pilih domain: smarterplaylists.playlistmachinery.com")
        print("   • Copy cookie SESI (bukan sp_* dari open.spotify.com), format:")
        print("     name=value; name2=value2")
        print()
        raw = input("Paste cookie sesi SmarterPlaylights di sini: ").strip()
        if not raw:
            raise RuntimeError("Tidak ada cookie yang diberikan — dibatalkan.")

        cookies = {}
        for part in raw.split(";"):
            part = part.strip()
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip()

        # Filter out obvious Spotify / consent cookies to reduce noise.
        for k in list(cookies):
            if k.startswith(SPOTIFY_COOKIE_PREFIXES) or k in (
                "OptanonConsent",
                "OptanonAlertBoxClosed",
                "eupubconsent-v2",
            ):
                print(f"   [skip] {k} (bukan cookie sesi SmarterPlaylights)")
                del cookies[k]

        if not cookies:
            raise RuntimeError(
                "Tidak ditemukan cookie sesi SmarterPlaylights yang valid. "
                "Pastikan Anda menyalin cookie dari domain smarterplaylists.playlistmachinery.com, "
                "bukan dari open.spotify.com."
            )

        # Step 3: validate against /api/auth/me.
        print("\n[3/4] Memvalidasi sesi ke /api/auth/me...")
        sess = requests.Session()
        for k, v in cookies.items():
            sess.cookies.set(k, v, domain="smarterplaylists.playlistmachinery.com")

        if not self._is_authenticated(sess):
            raise RuntimeError(
                "Cookie tidak terautentikasi. Pastikan Anda menyalin cookie SETELAH "
                "redirect kembali ke smarterplaylights selesai, dan dari domain "
                "smarterplaylists.playlistmachinery.com (bukan open.spotify.com)."
            )

        payload = {"cookies": cookies, "base_url": self.base_url}
        self.session_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self._session = sess
        print(f"   Sesi valid dan disimpan ke {self.session_file}")
        print(f"   Cookie yang tersimpan: {', '.join(sorted(cookies))}")

    def logout(self) -> None:
        sess = self.load()
        try:
            sess.post(f"{self.base_url}/api/auth/logout", timeout=15)
        finally:
            if self.session_file.exists():
                self.session_file.unlink()
            self._session = None
        print("Logged out. Session file removed.")

    # ------------------------------------------------------------------ #
    # API helpers
    # ------------------------------------------------------------------ #
    def _is_authenticated(self, sess: requests.Session) -> bool:
        try:
            r = sess.get(f"{self.base_url}/api/auth/me", timeout=15)
            return r.ok
        except requests.RequestException:
            return False

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.load().get(f"{self.base_url}{path}", timeout=30, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.load().post(f"{self.base_url}{path}", timeout=30, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.load().put(f"{self.base_url}{path}", timeout=30, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.load().delete(f"{self.base_url}{path}", timeout=30, **kwargs)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="SmarterPlaylights session manager")
    ap.add_argument("--init", action="store_true", help="interactive first-time login")
    ap.add_argument("--check", action="store_true", help="check whether current session is valid")
    ap.add_argument("--logout", action="store_true", help="remove saved session")
    args = ap.parse_args()

    sm = SmarterPlaylistsSession()

    if args.init:
        sm.init()
        return
    if args.check:
        try:
            sm.load()
            print("Session is valid.")
        except RuntimeError as exc:
            print(str(exc))
            sys.exit(1)
        return
    if args.logout:
        sm.logout()
        return

    ap.print_help()


if __name__ == "__main__":
    main()
