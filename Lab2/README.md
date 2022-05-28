# 环境要求

## 安装[Nodejs](https://nodejs.org/en/)

```shell
node -v # 当前版本是 v16.15.0
```

## 安装包管理工具

```shell
# 安装 yarn 包管理工具, 并设置国内软件源

npm install -g yarn --registry http://registry.npm.taobao.org/ # 只需要安装一次, 安装在用户 home 目录
# npm uninstall -g yarn # 卸载 yarn
yarn config set registry http://registry.npm.taobao.org/ # yarn 换国内源
```

## 安装后端第三方包

```shell
cd Lab2
yarn # 每当增加新的依赖包后, 都需要安装一次, 安装在 ./node_modules 目录
```

## 安装前端第三方包

```shell
cd Lab2/app
yarn # 每当增加新的依赖包后, 都需要安装一次, 安装在 ./node_modules 目录
```

# 运行

## 准备前端静态文件

```shell
# 将 Lab2/app 目录下的文件编译、压缩、打包, 生成到 Lab2/app/build 目录

cd Lab2/app
yarn build # 调用 package.json 中 script.build 对应的命令
```

## 启动服务器

```shell
# 需要事前将 main.ts 编译成 main.js

cd Lab2
node main.js
```

or

```shell

# 安装 typescript 直接运行 ts 代码

# ps. 如果提示没有 ts-node 命令, 则先执行以下命令
npm install -g ts-node

yarn global add typescript # 只需要安装一次, 安装在用户 home 目录
# yarn global remove typescript # 卸载 typescript
ts-node -v # 当前版本 v9.1.1

cd Lab2
ts-node main.ts
```

or

```shell
# 安装 typescript, 将 main.ts 编译成 main.js, 然后运行 js 代码

yarn global add typescript # 只需要安装一次, 安装在用户 home 目录
# yarn global remove typescript # 卸载 typescript
ts-node -v # 当前版本 v9.1.1

cd Lab2
tsc # 使用当前目录的 tsconfig.json 配置, 将 main.ts 编译成 main.js
node main.js
```

## 打开浏览器

```shell
chrome http://localhost:8080/
```

## python 环境

### 创建虚拟环境

```shell
virtualenv venv
```

### 启用虚拟环境
```shell
.\venv\Scripts\activate
```
### 下载依赖库

```shell
pip install jieba
pip install gensim==3.4.0

```