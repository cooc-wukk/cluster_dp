# cluster_dp
> 论文实验代码及数据

这里是介绍呀......


## git 使用

掌握主要是几个命令就行了，没那么复杂，想深入了解学习可以看推荐的教程。

### 具体步骤

#### 前期配置
- 1. 保证 `git` 命令能用，mac 上直接使用自带的终端就行，windows 要安装 GitBash 客户端；

- 2. 配置用户名和邮箱，命令如下：
```
git config --global user.name "wukunkun"
git config --global user.email "wukkgong@163.com"
```

- 3. 配置密匙。输入 `ssh-keygen` 命令生成公钥和私钥，并将生成的公钥配置到 github 上，具体操作请看[这篇文章](https://www.cnblogs.com/yangshifu/p/9919817.html)

#### 正式使用
- 1. 克隆仓库，只用以下命令就可以将 github 上的项目下载下来：
```
git clone git@github.com:cooc-wukk/cluster_dp.git
```
- 2. 代码修改之后，需要保存代码，将代码推送到远程，需要在项目文件夹下依次执行以下三个命令：
```
git add .

git commit -m '描述的话.......'

git push
```

#### 推荐教程：
- [git 简易指南](https://www.bootcss.com/p/git-guide/)
- [廖雪峰 Git 教程](https://www.liaoxuefeng.com/wiki/896043488029600)