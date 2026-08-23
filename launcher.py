#!/usr/bin/env python3
import functools, http.server, socketserver, threading, sys
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, WebKit, Gio

GAME_DIR = "/app/share/pvzge"
APP_ID = "com.pvzge.PvZGE"
PORT = 43117


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


QuietHandler.extensions_map[".wasm"] = "application/wasm"


def start_server():
    handler = functools.partial(QuietHandler, directory=GAME_DIR)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return PORT


def on_activate(app, port):
    win = Gtk.ApplicationWindow(application=app, title="PvZ2 Gardendless")
    win.set_default_size(1280, 800)

    view = WebKit.WebView()
    s = view.get_settings()
    s.set_enable_webgl(True)
    s.set_enable_developer_extras(True)
    s.set_media_playback_requires_user_gesture(False)
    s.set_enable_write_console_messages_to_stdout(True)

    view.load_uri(f"http://127.0.0.1:{port}/index.html")
    win.set_child(view)
    win.present()


app = Gtk.Application(application_id=APP_ID,
                      flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
port = start_server()
app.connect("activate", on_activate, port)
sys.exit(app.run(None))
