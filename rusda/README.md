

# 注意
> 项目skill：17.6.2/skills/frida-project-architecture

> 大家请务必使用AI Agent辅助操作，熟悉项目！

> 微信公众号：R逆向

## rusda 编译流程

> 建立一个项目目录并拉下frida源码，并进入项目目录


```shell
git clone --recurse-submodules -b 17.6.2 https://github.com/frida/frida frida17.6.2
cd frida
```

此时执行ls ，看到的文件应当是如此

```log
r@russell:~/Project/github/frida/frida17.6.2$ ls
BSDmakefile      COPYING   README.md  configure.bat  meson.build    releng       tools
CONTRIBUTING.md  Makefile  configure  make.bat       meson.options  subprojects
```

> 一键 安装nodejs22

```bash
# 构造下载 URL
NODE_TAR_URL="https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz"
wget $NODE_TAR_URL 
# 解压 Node.js 安装包到用户目录
tar -xf node-v22.12.0-linux-x64.tar.xz -C $HOME/bin
rm -r node-v22.12.0-linux-x64.tar.xz
# 设置 NODE_HOME 和 PATH
export NODE_HOME=$HOME/bin/node-v22.12.0-linux-x64
export PATH=${NODE_HOME}/bin:$PATH
# 打印 Node.js 版本以确认安装成功
node -v
```

```log
(base) r@ubuntu20:~/Documents/FRIDA/frida$ # 构造下载 URL
(base) r@ubuntu20:~/Documents/FRIDA/frida$ NODE_TAR_URL="https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz"
(base) r@ubuntu20:~/Documents/FRIDA/frida$ wget $NODE_TAR_URL 
--2024-12-09 23:31:18--  https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz
正在解析主机 nodejs.org (nodejs.org)... 198.18.1.205
正在连接 nodejs.org (nodejs.org)|198.18.1.205|:443... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度： 29734248 (28M) [application/x-xz]
正在保存至: “node-v22.12.0-linux-x64.tar.xz”

node-v22.12.0-linux-x64.tar.xz          100%[============================================================================>]  28.36M  8.89MB/s    用时 3.2s  

2024-12-09 23:31:21 (8.89 MB/s) - 已保存 “node-v22.12.0-linux-x64.tar.xz” [29734248/29734248])

(base) r@ubuntu20:~/Documents/FRIDA/frida$ # 解压 Node.js 安装包到用户目录
(base) r@ubuntu20:~/Documents/FRIDA/frida$ tar -xf node-v22.12.0-linux-x64.tar.xz -C $HOME/bin
(base) r@ubuntu20:~/Documents/FRIDA/frida$ # 设置 NODE_HOME 和 PATH
(base) r@ubuntu20:~/Documents/FRIDA/frida$ export NODE_HOME=$HOME/bin/node-v22.12.0-linux-x64
(base) r@ubuntu20:~/Documents/FRIDA/frida$ export PATH=${NODE_HOME}/bin:$PATH
(base) r@ubuntu20:~/Documents/FRIDA/frida$ # 打印 Node.js 版本以确认安装成功
(base) r@ubuntu20:~/Documents/FRIDA/frida$ node -v
v22.12.0
(base) r@ubuntu20:~/Documents/FRIDA/frida$ ls
BSDmakefile      COPYING     frida-go    frida-python  frida-swift  Makefile.freebsd.mk  Makefile.sdk.mk                 README.md
config.mk        frida-clr   frida-gum   frida-qml     frida-tools  Makefile.linux.mk    Makefile.toolchain.mk           releng
CONTRIBUTING.md  frida-core  frida-node  frida.sln     Makefile     Makefile.macos.mk    node-v22.12.0-linux-x64.tar.xz
(base) r@ubuntu20:~/Documents/FRIDA/frida$ rm -r node-v22.12.0-linux-x64.tar.xz
(base) r@ubuntu20:~/Documents/FRIDA/frida$ 
```

再make一下

```bash
make
```
发现报错
```log
r@russell:~/Project/github/frida/frida17.6.2$ make
INFO: autodetecting backend as ninja
INFO: calculating backend command to run: /home/r/Project/github/frida/frida17.6.2/deps/toolchain-linux-x86_64/bin/ninja
[1/2] Compiling C object subprojects/frida-python/frida/_frida/_frida.abi3.so.p/extension.c.o
FAILED: subprojects/frida-python/frida/_frida/_frida.abi3.so.p/extension.c.o
/usr/bin/cc -Isubprojects/frida-python/frida/_frida/_frida.abi3.so.p -Isubprojects/frida-python/frida/_frida -I../subprojects/frida-python/frida/_frida -Isubprojects/frida-core/src/api -I../subprojects/frida-core/src/api -Isubprojects/frida-gum -I../subprojects/frida-gum -Isubprojects/frida-gum/gum -I../subprojects/frida-gum/gum -I../subprojects/frida-gum/gum/arch-x86 -I../subprojects/frida-gum/gum/arch-arm -I../subprojects/frida-gum/gum/arch-arm64 -I../subprojects/frida-gum/gum/arch-mips -Isubprojects/frida-gum/libs -I../subprojects/frida-gum/libs -Isubprojects/frida-gum/libs/gum/heap -I../subprojects/frida-gum/libs/gum/heap -Isubprojects/frida-gum/libs/gum/prof -I../subprojects/frida-gum/libs/gum/prof -I../subprojects/frida-gum/gum/backend-linux/include -I../subprojects/frida-gum/gum/backend-elf -I../subprojects/frida-gum/gum/backend-libunwind/include -Isubprojects/frida-gum/bindings -I../subprojects/frida-gum/bindings -I/usr/lib/include/python3.10 -I/usr/lib/include/x86_64-linux-gnu/python3.10 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/glib-2.0 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/lib/glib-2.0/include -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/gee-0.8 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/json-glib-1.0 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/capstone -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/libsoup-3.0 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/gio-unix-2.0 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/libusb-1.0 -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/quickjs -I/home/r/Project/github/frida/frida17.6.2/deps/sdk-linux-x86_64/include/nice -fvisibility=hidden -fdiagnostics-color=always -DNDEBUG -D_FILE_OFFSET_BITS=64 -Wall -Winvalid-pch -Os -g -ffunction-sections -fdata-sections -fPIC -pthread -DNGTCP2_STATICLIB -DNGHTTP2_STATICLIB -DGUM_STATIC -DFFI_STATIC_BUILD -DG_DISABLE_ASSERT -DG_DISABLE_CHECKS -DG_DISABLE_CAST_CHECKS -DPy_LIMITED_API=0x03070000 -MD -MQ subprojects/frida-python/frida/_frida/_frida.abi3.so.p/extension.c.o -MF subprojects/frida-python/frida/_frida/_frida.abi3.so.p/extension.c.o.d -o subprojects/frida-python/frida/_frida/_frida.abi3.so.p/extension.c.o -c ../subprojects/frida-python/frida/_frida/extension.c
../subprojects/frida-python/frida/_frida/extension.c:33:11: fatal error: pyconfig.h: No such file or directory
   33 | # include <pyconfig.h>
      |           ^~~~~~~~~~~~
compilation terminated.
ninja: build stopped: subcommand failed.
Command '['/usr/bin/python3', '/home/r/Project/github/frida/frida17.6.2/releng/meson/meson.py', 'compile']' returned non-zero exit status 1.
make: *** [Makefile:4: all] Error 1
r@russell:~/Project/github/frida/frida17.6.2$

```
原因是Frida 自带的 toolchain 中的 pkg-config 返回了错误的 include 路径
先安装python开发版本，再软链接到frida所使用
```bash
sudo apt install python3.10-dev
sudo ln -s /usr/include /usr/lib/include
```
再次make就可以了
```log
r@russell:~/Project/github/frida/frida17.6.2$ make
INFO: autodetecting backend as ninja
INFO: calculating backend command to run: /home/r/Project/github/frida/frida17.6.2/deps/toolchain-linux-x86_64/bin/ninja
[2/2] Linking target subprojects/frida-python/frida/_frida/_frida.abi3.so
r@russell:~/Project/github/frida/frida17.6.2$
```


> 安装ndk

执行以下命令，查看所需要的ndk版本，得到以下输出

```shell
grep -r "NDK_REQUIRED\|ANDROID_NDK" releng/ .github/
```

```log
r@russell:~/Project/github/frida/frida17.6.2$ grep -r "NDK_REQUIRED\|ANDROID_NDK" releng/ .github/
releng/env_android.py:        ndk_root = Path(environ["ANDROID_NDK_ROOT"])
releng/env_android.py:        raise NdkNotFoundError(f"ANDROID_NDK_ROOT must be set to the location of your r{NDK_REQUIRED} NDK")
releng/env_android.py:        if major_version != NDK_REQUIRED:
releng/env_android.py:            raise NdkVersionError(f"NDK r{NDK_REQUIRED} is required (found r{major_version}, which is unsupported)")
releng/env_android.py:NDK_REQUIRED = 25
grep: releng/__pycache__/env_android.cpython-310.pyc: binary file matches
.github/workflows/ci.yml:  ANDROID_NDK_VERSION: r25b
.github/workflows/ci.yml:          ndk-version: ${{ env.ANDROID_NDK_VERSION }}
.github/workflows/ci.yml:      - name: Add ANDROID_NDK_ROOT to environment
.github/workflows/ci.yml:        run: echo "ANDROID_NDK_ROOT=${{ steps.setup-ndk.outputs.ndk-path }}" >> $GITHUB_ENV
.github/workflows/ci.yml:          ndk-version: ${{ env.ANDROID_NDK_VERSION }}
.github/workflows/ci.yml:          ANDROID_NDK_ROOT: ${{ steps.setup-ndk.outputs.ndk-path }}
.github/workflows/ci.yml:          ndk-version: ${{ env.ANDROID_NDK_VERSION }}
.github/workflows/ci.yml:          ANDROID_NDK_ROOT: ${{ steps.setup-ndk.outputs.ndk-path }}
```

一键安装ndk25

```bash
mkdir ~/bin
wget https://dl.google.com/android/repository/android-ndk-r25c-linux.zip
unzip -q android-ndk-r25c-linux.zip -d $HOME/bin/
rm android-ndk-r25c-linux.zip
export ANDROID_NDK_ROOT=$HOME/bin/android-ndk-r25c
export PATH=$ANDROID_NDK_ROOT:$PATH
ndk-build -v
```
```log
r@russell:~/Project/github/frida/frida17.6.2$ wget https://dl.google.com/android/repository/android-ndk-r25c-linux.zip
unzip -q android-ndk-r25c-linux.zip -d $HOME/bin/
rm android-ndk-r25c-linux.zip
export ANDROID_NDK_ROOT=$HOME/bin/android-ndk-r25c
export PATH=$ANDROID_NDK_ROOT:$PATH
ndk-build -v
--2026-02-06 20:59:36--  https://dl.google.com/android/repository/android-ndk-r25c-linux.zip
Resolving dl.google.com (dl.google.com)... 120.253.250.225
Connecting to dl.google.com (dl.google.com)|120.253.250.225|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 531118193 (507M) [application/zip]
Saving to: ‘android-ndk-r25c-linux.zip’

android-ndk-r25c-linux.zip            100%[========================================================================>] 506.51M  18.8MB/s    in 77s

2026-02-06 21:00:53 (6.58 MB/s) - ‘android-ndk-r25c-linux.zip’ saved [531118193/531118193]

GNU Make 4.3
Built for x86_64-pc-linux-gnu
Copyright (C) 1988-2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```


> 安装依赖

```bash
sudo apt update
sudo apt-get install build-essential git lib32stdc++-9-dev libc6-dev-i386
sudo apt install gcc-multilib g++-multilib libc6-dev-i386
pip3 install lief

```

编译
```bash
rm -rf build
./configure \
    --prefix="dist-android/staging-arm64" \
    --host="android-arm64" \
    --enable-server \
    --enable-gadget \
    --enable-inject
make
make install
```
安装完成后，可执行文件和库会出现在：
dist-android/staging-arm64/bin/frida-server
dist-android/staging-arm64/bin/frida-inject
dist-android/staging-arm64/lib/frida/64/frida-gadget.so


可以使用编译的ssh脚本，大致就是
> $prefix = dist-android/staging-{arch}（如 dist-android/staging-arm64）
> $arch = x86、x86_64、arm、arm64
如果有脚本编译完
```log
Installing /home/r/Project/github/frida/frida17.6.2/build-android-x86_64/meson-private/frida-core-1.0.pc to /home/r/Project/github/frida/frida17.6.2/dist-android/staging-x86_64/lib/pkgconfig
[x86_64] 完成

=== 打包 (官方命名格式: frida-*-{version}-android-{arch}.xz) ===
  frida-server-17.6.2-android-x86.xz
  frida-inject-17.6.2-android-x86.xz
  frida-gadget-17.6.2-android-x86.so.xz
  frida-server-17.6.2-android-x86_64.xz
  frida-inject-17.6.2-android-x86_64.xz
  frida-gadget-17.6.2-android-x86_64.so.xz
  frida-server-17.6.2-android-arm.xz
  frida-inject-17.6.2-android-arm.xz
  frida-gadget-17.6.2-android-arm.so.xz
  frida-server-17.6.2-android-arm64.xz
  frida-inject-17.6.2-android-arm64.xz
  frida-gadget-17.6.2-android-arm64.so.xz

=== 完成 ===
输出目录: /home/r/Project/github/frida/frida17.6.2/dist-android
-rw-r--r-- 1 r r 5.8M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-gadget-17.6.2-android-arm.so.xz
-rw-r--r-- 1 r r 5.8M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-gadget-17.6.2-android-arm64.so.xz
-rw-r--r-- 1 r r 7.6M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-gadget-17.6.2-android-x86.so.xz
-rw-r--r-- 1 r r 7.6M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-gadget-17.6.2-android-x86_64.so.xz
-rw-r--r-- 1 r r 6.6M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-inject-17.6.2-android-arm.xz
-rw-r--r-- 1 r r  15M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-inject-17.6.2-android-arm64.xz
-rw-r--r-- 1 r r  15M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-inject-17.6.2-android-x86.xz
-rw-r--r-- 1 r r  30M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-inject-17.6.2-android-x86_64.xz
-rw-r--r-- 1 r r 6.7M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-server-17.6.2-android-arm.xz
-rw-r--r-- 1 r r  15M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-server-17.6.2-android-arm64.xz
-rw-r--r-- 1 r r  15M Feb  6 22:46 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-server-17.6.2-android-x86.xz
-rw-r--r-- 1 r r  31M Feb  6 22:47 /home/r/Project/github/frida/frida17.6.2/dist-android/frida-server-17.6.2-android-x86_64.xz
```


# 0x2 修改frida

> 工欲善其事必先利其器

## 环境配置好之后用cursor或者claude code，或是其他ai agent，只要不是那种辣鸡模型，都可以，让他帮你apply patch，然后编译即可，然后让其自检

```log
r@russell:~/Project/github/frida/frida17.6.2$ ./tools/build-android-all.sh | grep Patch
[*] Patch frida-agent: subprojects/frida-core/lib/agent/rusda-agent.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0xc4d5d orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xd284c orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xd96ec orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x961c9 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xc4e50 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xb06d8 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x10f49e orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x136447 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x143e10 orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/gadget/rusda-gadget.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0xcddf7 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xdb8f3 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xe29d9 orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x9ee64 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xcde96 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xb95fc orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x1183bc orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x140380 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x14df0e orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/agent/rusda-agent.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0xcb90a orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xd8fd7 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xdfe2e orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x9d7bc orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xcb9fd orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xb77d5 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x1146f7 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x13ba0c orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x149162 orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/gadget/rusda-gadget.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0xc5cf0 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xd3bdd orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0xdacc5 orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x963d5 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xc5d8f orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0xb0fc0 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x111b13 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x139753 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x147540 orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/agent/rusda-agent.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0x19f1af orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1acba0 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1b3a9e orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x1706fc orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x19f2a2 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x18aadf orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x1e92c2 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x21057f orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x21df6c orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/gadget/rusda-gadget.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0x1a0cf0 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1aeaef orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1b5c35 orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x1714c8 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x1a0d8f orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x18bf87 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x1ec507 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x214446 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x222257 orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/agent/rusda-agent.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0x1c30ed orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1d0e15 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1d7d2b orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x194120 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x1c31e0 orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x1ae84a orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x20e3d3 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x235c92 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x24382f orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
[*] Patch frida-agent: subprojects/frida-core/lib/gadget/rusda-gadget.so.tmp
[*] Patch `frida` to `rusda`
[*] Patching section name=.rodata offset=0x1c648e orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1d45f5 orig:FridaScriptEngine new:enignEtpircSadirF
[*] Patching section name=.rodata offset=0x1db79a orig:GLib-GIO new:OIG-biLG
[*] Patching section name=.rodata offset=0x19668e orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x1c652d orig:GDBusProxy new:yxorPsuBDG
[*] Patching section name=.rodata offset=0x1b1537 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x212f6b orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x23b4c4 orig:GumScript new:tpircSmuG
[*] Patching section name=.rodata offset=0x249499 orig:GumScript new:tpircSmuG
[*] Patch `gum-js-loop` to `russellloop`
[*] Patch `gmain` to `rmain`
[*] Patch `gdbus` to `rubus`
[*] Patch Finish
```



## 对于AI时代，检验结果至关重要，也可以使用如下方式自检
```log
r@russell:~/Project/github/frida/frida17.6.2$ python3 tools/verify-patch.py
======================================================================
rusda patch 验证
======================================================================
目录: /home/r/Project/github/frida/frida17.6.2/dist-android
产物数: 12

检查规则:
  ✗ 不应出现 (未 patch): FridaScriptEngine, GLib-GIO, GDBusProxy, GumScript,
                        gum-js-loop, gmain, gdbus
  ✓ 应出现 (已 patch):   enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG,
                        russellloop, rmain, rubus
----------------------------------------------------------------------

rusda-gadget-17.6.2-android-arm.so.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-gadget-17.6.2-android-arm64.so.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-gadget-17.6.2-android-x86.so.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-gadget-17.6.2-android-x86_64.so.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-inject-17.6.2-android-arm.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-inject-17.6.2-android-arm64.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-inject-17.6.2-android-x86.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-inject-17.6.2-android-x86_64.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-server-17.6.2-android-arm.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-server-17.6.2-android-arm64
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-server-17.6.2-android-x86.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

rusda-server-17.6.2-android-x86_64.xz
  状态: ✓ PASS
  已 patch: enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG, russellloop, rmain, rubus

======================================================================
全部通过 ✓
r@russell:~/Project/github/frida/frida17.6.2$
```