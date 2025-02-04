## 背景

macOS 下使用 [im-select](https://github.com/keaising/im-select.nvim) 切换输入法，但是在远程环境中时，例如服务器使用 `nvim --listen` 启动，本地用 neovide 连接，此时 im-select 是在远端环境执行的，自然没有办法切换输入法，

为了解决这个问题，思路是在本地启一个 socket 的服务，在 ssh 时 Forward 到远端，远端执行命令时转发到本地执行。

因此该项目即实现了该功能。

## 使用方法

1. 本地执行 `./rcmd_server.py`
2. 配置 ssh config，例如：
   ```
   Host server
       RemoteForward 11450 /tmp/rcmd.sock
   ```
3. `ssh server` 到远端
4. 将 `rcmd_client.py` 复制到远端 $PATH 中，并`ln -s rcmd_client.py macism`
5. 在远端执行 `macism` 即可

为了安全性，在 rcmd_server.py 中使用了白名单，目前只允许 macism，可以自行修改。

## vim 配置

强制指定远端（linux 环境）也使用 macism 即可

```
  {
    'keaising/im-select.nvim',
    config = function()
      require('im_select').setup({
        default_command = 'macism'
      })
    end
  },
```

## 开机自动启动

将 com.user.rcmd.plist 复制到 ~/Library/LaunchAgents/ 即可，同时修改 ProgramArguments 为 rcmd_server.py 的路径，然后加载并启动服务

```
launchctl load ~/Library/LaunchAgents/com.user.rcmd.plist
launchctl start com.user.rcmd
```
