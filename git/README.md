# Git结构

<img style='center' src="./data/git.png" width="800"/>

```bash
  (1) Workspace: 工作区
  (2) Index/Stage: 缓冲区
  (3) Repository: 仓库区(本地仓库)
  (4) Remote: 远程仓库
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
  > 查看工作区文件和暂存区文件的差异
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
------------------------------------------
- git branch
  > 查看本地所有分支
- git branch -r
  > 查看远程所有分支
- git branch -a
  > 查看本地和远程所有分支
- git branch [branch name]
  > 在本地新建一个分支，但是依然停留在当前分支
- git checkout -b [branch name]
  > 在本地新建一个分支，并切换到该分支
- git checkout [branch name]
  > 切换到指定分支，并更新工作区
- git branch --track [branch] [remote-branch]
  > 新建一个分支，与指定的远程分支建立追踪关系
- git branch --set-upstream-to=[remote branch]
  > 在现有分支与指定的远程分支之间建立追踪关系
------------------------------------------
- git branch -d [branch name]
  > 删除本地分支
- git push origin --delete [branch name]
  > 删除远程分支
- git branch -dr [remote branch]
  > 删除远程分支

## git状态查看
- git status
  > 查看文件变更情况
- git log
  > 显示当前分支的版本历史
- git log --pretty --oneline
  > 显示当前分支的版本历史（仅显示一行）
- git diff
  > 查看暂存区和工作区的代码差异
- git diff HEAD
  > 查看工作区与当前分支最新commit之间的差异
- git reflog
  > 查看当前分支的最近几次提交

## git远程同步

## git撤销修改
