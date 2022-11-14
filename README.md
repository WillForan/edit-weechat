# edit-weechat

This simple [weechat](https://weechat.org/) plugin allows you to
compose messages in your `$EDITOR`.

`message.md` in `~/.cache/weechat/` or `~/.weechat`
is used to set and get message text.

# Usage

```sh
/edit
# Type some stuff
# Save and quit
```

# Configuration

If you'd like to customize the editor you use outside of the `$EDITOR`
environment variable, you can set it in weechat.

```sh
/set plugins.var.python.edit.editor "vim -f"
```

You can also bind <kbd>alt-e</kbd> to quickly edit whatever has been written so far. (NB. `\u0020` is space)

```sh
/key bind meta-e /input move_beginning_of_line; /input insert /edit\u0020; /input return
```

# Installation

Copy the script to `~/.weechat/python/autoload`

```
mkdir -p ${XDG_DATA_HOME:-~/.local/share}/weechat/python/autoload/
wget https://raw.githubusercontent.com/WillForan/edit-weechat/master/edit.py $_
```


