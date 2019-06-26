# Git结构

<img style='center' src="./data/git.png" width="800"/>

```bash
  > Workspace: 工作区
  > Index/Stage: 缓冲区
  > Repository: 仓库区(本地仓库)
  > Remote: 远程仓库
```

# git常用命令
## git信息配置
- git config --list
  > 查看当前Git的配置信息
- git config --global user.name "[name]"
  > 设置提交代码时的用户名
- git config --global user.email "[email]"
  > 设置提交代码时的用户邮箱
- git config --global push.default [matching] | [simple]
  > 只推送当前分支叫做simple方式；推送所有对应的远程分支的本地分支叫做matching方式，Git 2.0版本之前默认是matching，现在默认为simple

## git代码提交
- git status
  > 查看各个文件的修改状态
- git diff [filename]
  > 查看该文件了和上一个版本的差异
- git add [filename]|[directory]
  > 将修改的或者新的文件或者文件夹添加到缓冲区
- git commit -m "[description]"
  > 将add的文件或者文件夹添加到本地仓库
- git push
  - git push
    > 不带任何参数的git push默认只推送当前分支，当命令行不指定远程分支名，git将查询当前分支的branch.*.remote配置以确定要在往哪里推送
  - git push origin [local branch]
    > 将本地分支从本地仓库push到远程分支, 当命令行不指定远程分支名，git将查询当前分支的branch.*.remote配置以确定要在往哪里推送，如果远程主机没有对应地分支则创建一个新的分支
  - git push [origin] [local branch]:[remote branch]
    > 将本地指定的分支push到远程指定的分支
  - git push --all origin
    > 将所有分支都push到远程主机

## git分支
## git状态信息查看
## git远程同步
## git撤销修改
