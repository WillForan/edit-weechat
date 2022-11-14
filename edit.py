# Open your $EDITOR to compose a message in weechat
#
# Usage:
# /edit
#
# Optional settings:
# /set plugins.var.python.edit.editor "vim -f"
# /set plugins.var.python.edit.terminal "xterm"
# /set plugins.var.python.edit.run_externally "false"
# /set plugins.var.python.edit.paste_file "/path/to/external_clipboard.txt"
#
# History:
# 20221113WF
# Version 1.1.0: paste_file opt. '/edit fc' msg.md from paste_file as code blk
# Version 1.0.3: /edit arguments written to file. file is .md
# 10-18-2015
# Version 1.0.2: Add the ability to run the editor in a external terminal
# Version 1.0.1: Add configurable editor key
# Version 1.0.0: initial release

import os
import os.path
import shlex
import subprocess
import weechat


__VERSION__ = "1.1.0"


def xdg_cache_dir():
    return os.path.expanduser(os.environ.get("XDG_CACHE_HOME", "~/.cache/"))


def weechat_cache_dir():
    cache_dir = os.path.join(xdg_cache_dir(), "weechat")
    if os.path.exists(cache_dir):
        return cache_dir
    return os.path.expanduser(os.environ.get("WEECHAT_HOME", "~/.weechat/"))


PATH = os.path.join(weechat_cache_dir(), "message.md")


def editor_process_cb(data, command, return_code, out, err):
    buf = data

    if return_code != 0:
        cleanup(PATH, buf)
        weechat.prnt("", "{}: {}".format(
            err.strip(),
            return_code
        ))
        return weechat.WEECHAT_RC_ERROR

    if return_code == 0:
        read_file(PATH, buf)
        cleanup(PATH, buf)

    return weechat.WEECHAT_RC_OK


def cleanup(path, buf):
    try:
        os.remove(path)
    except (OSError, IOError):
        pass

    weechat.command(buf, "/window refresh")


def read_file(path, buf):
    try:
        with open(PATH) as f:
            text = f.read().strip()
        weechat.buffer_set(buf, "input", text)
        weechat.buffer_set(buf, "input_pos", str(len(text)))

    except (OSError, IOError):
        pass

    weechat.command(buf, "/window refresh")


def hook_editor_process(terminal, editor, path, buf):
    term_cmd = "{} -e".format(terminal)
    editor_cmd = "{} {}".format(editor, path)
    weechat.hook_process("{} \"{}\"".format(
        term_cmd,
        editor_cmd
    ), 0, "editor_process_cb", buf)


def run_blocking(editor, path, buf):
    cmd = shlex.split(editor) + [path]
    code = subprocess.Popen(cmd).wait()

    if code != 0:
        cleanup(path,  buf)

    read_file(path, buf)


def edit(data, buf, args):
    editor = (weechat.config_get_plugin("editor")
              or os.environ.get("EDITOR", "vim -f"))

    terminal = (weechat.config_get_plugin("terminal")
                or os.getenv("TERMCMD"))

    terminal = terminal or "xterm"

    run_externally = weechat.config_string_to_boolean(
        weechat.config_get_plugin("run_externally")
    )
    run_externally = bool(run_externally)

    # paste from file.
    # /edit f => default content pulled from paste_file
    # /edit fc => as above but with ``` code blocks
    # if not f or fc, use whatever was provided as file contents
    # /edit hello world => message.md will start with "hello world"
    if args in ["fc", "f"]:
        file = (weechat.config_get_plugin("paste_file") or
                "/mnt/storage/dl/slack/upload/upload.txt")
        with open(file, "r") as f:
            file_contents = "\n".join(f.readlines())
            if args == "fc":
                file_contents = "```\n" + file_contents + "\n```"
    else:
        file_contents = args

    with open(PATH, "w+") as f:
        f.write(file_contents)
        f.write(weechat.buffer_get_string(buf, "input"))

    if run_externally:
        hook_editor_process(terminal, editor, PATH, buf)
    else:
        run_blocking(editor, PATH, buf)

    return weechat.WEECHAT_RC_OK


def main():
    if not weechat.register("edit", "Keith Smiley", __VERSION__, "MIT",
                            "Open your $EDITOR to compose a message", "", ""):
        return weechat.WEECHAT_RC_ERROR

    weechat.hook_command("edit", "Open your $EDITOR to compose a message", "",
                         "", "", "edit", "")


if __name__ == "__main__":
    main()
