# git结构
  <img style='center' src="./data/git.png" width="800"/>

```bash
  (1) Workspace: 工作区
  (2) Index/Stage: 缓冲区
  (3) Repository: 仓库区(本地仓库)
  (4) Remote: 远程仓库
```

# git命令
## git信息配置
- git config --list
  > 查看当前Git的配置信息
- git config --global user.name "[name]"
  > 设置提交代码时的用户名
- git config --global user.email "[email]"
  > 设置提交代码时的用户邮箱
- git config --global push.default [matching] | [simple]
  > 只推送当前分支叫做simple方式；推送所有对应的远程分支的本地分支叫做matching方式，Git 2.0版本之前默认是matching，现在默认为simple
- git config --global color.ui auto
  > 命令行输出着不同的强调色

## git初始化
- git clone [remote repo url] [your repo name]
  > 从远程主机clone代码到本地
- git init
  > 初始化本地repo
- git remote add origin [remote repo url]
  > 将本地git项目关联到远程

## git代码提交
- git status
  > 查看各个文件的修改状态
- git diff [filename]
  > 查看工作区文件和暂存区文件的差异
- git add [filename]|[directory]
  > 将修改的或者新的文件或者文件夹添加到缓冲区
- git commit -m "[description]"
  > 将add的文件或者文件夹添加到本地仓库

## git分支管理
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
------------------------------------------
- git rm [filename]
  > 删除本地分支某个文件
- git add .
  > 将本地修改添加到缓冲区
- git commit -m 'comments'
  > 将修改添加到本地仓库
- git push [remote] [local branch]:[remote branch]
  > 将本地指定的分支push到远程指定的分支

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
- git push
  - git push
    > 不带任何参数的git push默认只推送当前分支，当命令行不指定远程分支名，git将查询当前分支的branch.*.remote配置以确定要在往哪里推送
  - git push origin [local branch]
    > 将本地分支从本地仓库push到远程分支, 当命令行不指定远程分支名，git将查询当前分支的branch.*.remote配置以确定要在往哪里推送，如果远程主机没有对应地分支则创建一个新的分支
  - git push [origin] [local branch]:[remote branch]
    > 将本地指定的分支push到远程指定的分支
  - git push --all origin
    > 将所有分支都push到远程主机
- git fetch [remote]
  > 下载远程仓库的所有变动
- git reset --hard [remote branch]
  > 远程仓库代码覆盖本地仓库代码
- git merge [branch] | [remote branch]
  > 将某个分支或者某个远程分支合并到当前分支
- git pull [remote] [local branch]
  > 将远程仓库的变化与本地分支合并

## [git撤销修改](https://zhuanlan.zhihu.com/p/22734098)
- git checkout -- [filename]
  > 取消对文件的修改
- git checkout [filename]
  > 恢复暂存区的文件到工作区
- git checkout .
  > 恢复暂存区的所有文件到工作区
- git reset HEAD [filename]
  > 取消git add操作
- git reset --mixed | --soft | --hard HEAD^
  > 取消git commit操作， 其中--mixed表示不删除工作空间改动的代码，撤销commit和add，这是默认参数，--soft不删除改动的代码，撤销commit，不撤销add，--hard删除改动的代码，撤销commit和add， HEAD^表示上一个版本
- git commit --amend
  > 修改上一次commit写错的注释

## git打标签
- git tag
  > 查看所有标签名
- git show [tagname]
  > 查看对应标签名的commit情况
- git tag [tagname]
  > 给当前分支的最新commit打标签
- git tag [tagname] [commit id]
  > 也可以给历史版本打标签，先使用git log找到对应commit的id，然后给对应的commit id打标签
- git tag -a [tagname] -m "description" [commit id]
  > 给对应commit id打标签并写描述内容
- git push [remote] [tagname]
  > 提交tag到远程主机
- git push [remote] --tags
  > 提交所有tag到远程主机
- git tag -d [tagname]
  > 删除本地tag
- git push origin :refs/tags/[tagname]
  > 删除远程tag
- git checkout -b [branchname] [tagname]
  > 新建一个分支，指向某个tag

# git文献
- [git 命令](https://www.cnblogs.com/chenwolong/p/GIT.html)
- [git 教程](https://www.yiibai.com/git)
- [git 图解](https://zhuanlan.zhihu.com/p/22734098)
- [git 手册](https://git-scm.com/book/en/v2)


