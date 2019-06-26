# Git结构

<img style='center' src="./data/git.png" width="800"/>

```bash
  > Workspace: 工作区
  > Index/Stage: 缓冲区
  > Repository: 仓库区(本地仓库)
  > Remote: 远程仓库
```

# git command
## git信息配置
## git代码提交
- git status
  - 说明：查看各个文件的修改状态
- git diff [filename]
  - 说明：查看该文件了和上一个版本的差异
- git add [filename]|[directory]
  - 说明：将修改的或者新的文件或者文件夹添加到缓冲区
- git commit -m "[description]"
  - 说明：将add的文件或者文件夹添加到本地仓库
- git push
  - git push
    - 说明：当命令行不指定使用<repository>参数推送的位置时，将查询当前分支的branch.*.remote配置以确定要在哪里推送。 如果配置丢失，则默认为origin


  - git push [remote branch] [local branch]

## git分支
## git状态信息查看
## git远程同步
## git撤销修改
