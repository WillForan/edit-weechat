# edit-weechat

This simple [weechat](https://weechat.org/) plugin allows you to
compose messages in your `$EDITOR`.

`message.md` in `~/.cache/weechat/` or `~/.weechat`
is used to set and get message text.

# Usage

```sh
/edit
# Type some stuff in your editor
# Save and quit
```


```sh
some message that got too long [Ctrl-a] /edit 
# editor starts with "some message that got too long"
```

## Clipboard
The workstation clipboard might not be accessible if weechat is, for example, in tmux on a remote machine with outX11Forwarding. The kludge available here: send clipboard contents to a file on the weechat host. Pull from that file.

```sh
/edit f
# intial message.md contents copied from plugins.var.python.edit.paste_file
```

```sh
/edit fc
# same as above, but surrounded by a markdown code fence (useful for wee-slack)
```

Whether this is any better than <kbd>Shift+Insert</kbd> from within the editor, isn't answered here. Neither is idea. [ (1) greenclip + enter to sync primary and clipboard (2) sync clip with server (3) fc alt+e VS (1) /edit (2) shift+insert (3) add bottom fence (4) go to top and add top fence ]

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

Set the file `/edit f` and `/edit fc` use
```sh
/set plugins.var.python.edit.paste_file "/path/to/clipboard.txt"
```

# Installation

Copy the script to `~/.weechat/python/autoload`

```
mkdir -p ${XDG_DATA_HOME:-~/.local/share}/weechat/python/autoload/
wget https://raw.githubusercontent.com/WillForan/edit-weechat/master/edit.py $_
```


