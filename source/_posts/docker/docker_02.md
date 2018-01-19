title: 容器隔离机制
date: 2015-10-28 10:55:21
tags: [docker]
categories: [容器]
---

## Linux中的隔离机制 ##

Linux中使用namespace做隔离, namespace分为以下6种:

|namespace|系统参数|隔离内容|
|---------|--------|--------|
|UTS|CLONE_NEWUTS|主机名和域名|
|IPC|CLONE_NEWIPC|信号量、消息队列、共享内存|
|PID|CLONE_NEWPID|进程编号|
|Network|CLONE_NEWNET|网络设备、网络栈、端口等|
|Mount|CLONE_NEWNS|挂载点(文件系统)|
|User|CLONE_NEWUSER|用户和用户组|

namespace的4个API:
|API|API定义|说明|
|clone|int clone(int (*child_func)(void* args), void* child_stack, int flags, void* arg))|创建一个子进程并设置namespace|
|setns|int setns(int fd, int nstype)|将当前进程设置已有的namespace, 但当前进程不进入到新的pid namespace, 只有新创建的子进程才加入到已有的pid namesapce中|
|unshare|int unshare(int flags)|在原有进程中创建namespace, 但当前进程并不进入到新的pid namespace, 只有新启动的子进程才会进入创建的pid namespace中|
|/proc/$$/ns|目录下的文件描述符|每个文件对应namespace的文件描述符, []中的编号为namespace编号, 相同namespace表示在同一个namespace下|

/proc/$$/ns下目录文件:

```
dr-x--x--x. 2 root root 0 Oct 28 13:38 .
dr-xr-xr-x. 8 root root 0 Oct 28 13:29 ..
lrwxrwxrwx. 1 root root 0 Oct 28 13:38 ipc -> ipc:[4026531839]
lrwxrwxrwx. 1 root root 0 Oct 28 13:38 mnt -> mnt:[4026532171]
lrwxrwxrwx. 1 root root 0 Oct 28 13:38 net -> net:[4026531956]
lrwxrwxrwx. 1 root root 0 Oct 28 13:38 pid -> pid:[4026531836]
lrwxrwxrwx. 1 root root 0 Oct 28 13:38 uts -> uts:[4026531838]
```

## 隔离机制测试 ##
1. utc namespace测试

测试过程:
a. 启动test_utc.o, shell中的hostname为程序中指定的hostname, 使用uname -a查询hostname信息为设置的SilenceHostName
b. exit结束进程后, shell的hostname恢复, 并且使用uname -a命令查询仍然是系统默认hostname

代码:
```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];

char* const child_args[] = {
    "/bin/bash",
    NULL
};

int child_main(void* args) {
    printf("子进程启动\n");
    sethostname("SilenceHostName", 15);
    execv(child_args[0], child_args);
    return 1;
}

int main(int argc, char** argv) {
    printf("父进程启动\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("父进程结束\n");
    return 0;
}
```

编译:
```
gcc -Wall test_utc.c -o test_utc.o && ./test_utc.o
```

2. ipc namespace

可以使用命令ipcmk -Q创建一个进程间通信的消息队列, 使用ipcs -q查询所有消息队列, 使用ipcrm -q msqid删除消息队列

测试过程:
a. 使用ipcmk -Q创建消息队列
b. 启动test_ipc.o, 在shell中使用ipcs -q查询消息队列, 并使用ipcrm -q删除
c. exit结束进程后, 使用ipcs -q查询消息队列

代码:
```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];

char* const child_args[] = {
    "/bin/bash",
    NULL
};

int child_main(void* args) {
    printf("子进程启动\n");
    sethostname("SilenceHostName", 15);
    execv(child_args[0], child_args);
    return 1;
}

int main(int argc, char** argv) {
    printf("父进程启动\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWIPC | CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("父进程结束\n");
    return 0;
}
```

3. pid namesapce

测试过程:
a. 在shell中启动进程`/bin/bash -c "while true; do echo test; sleep 1; done" >/dev/null 2>&1`
b. 启动test_pid.o, 在shell中使用查看当前shell的进程id是否为1(`echo $$`)
c. ps aux查看进程信息, 并使用kill -9删除步骤一中进程
d. exit结束进程后, 使用ps aux查看刚刚删除的pid是否存储

代码:
```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];

char* const child_args[] = {
    "/bin/bash",
    NULL
};

int child_main(void* args) {
    printf("子进程启动\n");
    sethostname("SilenceHostName", 15);
    execv(child_args[0], child_args);
    return 1;
}

int main(int argc, char** argv) {
    printf("父进程启动\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("父进程结束\n");
    return 0;
}
```

测试结果:
a. test_pid.o启动后查看, shell进程id为1, 说明该shell进程为init进程
b. ps aux可以看到系统所有的进程信息
c. kill -9 不能删除系统中的进程
d. 系统中进程未kill

对于b步骤可以看到所有进程信息当时是不合理, 原因是test_pid.o启动的进程中的proc目录挂载到了系统中的/proc目录:
a. 可以使用mount重新挂载/proc目录: `mount -t proc proc /proc`, 此时使用ps aux只能看到两个进程信息
b. 发现在exit子进程后, 发现ps aux命令报错, 可以执行`mount -t proc proc /proc`修复，在此程序中未进行mount namespace隔离文件, 此时修改已影响到系统的文件系统信息

4. mount namespace

设置挂载传播事件状态:
```
mount --make-shared <mount-object>      # 设置为共享挂载
mount --make-private <mount-object>     # 设置为私有挂载
mount --make-slave <mount-object>       # 设置为从属挂载
mount --make-unbindable <mount-object>  # 设置为不可绑定挂载
```

测试过程:
a. 设置/proc目录为私有挂载
b. 启动test_ns.o, 在shell中挂载proc目录
c. exit子进程后, 使用ps aux查看进程信息是否报错

代码:
```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char child_stack[STACK_SIZE];

char* const child_args[] = {
    "/bin/bash",
    NULL
};

int child_main(void* args) {
    printf("子进程启动\n");
    sethostname("SilenceHostName", 15);
    execv(child_args[0], child_args);
    return 1;
}

int main(int argc, char** argv) {
    printf("父进程启动\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("父进程结束\n");
    return 0;
}
```

测试结果:
a. 启动test_ns.o并执行mount -t proc proc /proc后使用ps aux只可看到两个进程
b. exit退出口使用ps aux可以看到系统上运行的所有进程

5. netwrok namespace

6. user namespace

测试过程:
a. 安装libcap-dev包，用来获取用户权限
b. 使用uid为1000的user编译test_user.c文件，并运行test_user.o

代码:
```
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/capability.h>
#include <stdio.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)
#define PATH_SIZE 1024

static char child_stack[STACK_SIZE];

char* const child_args[] = {
    "/bin/bash",
    NULL
};

int set_map(pid_t pid, char* map_type, int inside_id, int outside_id, int length) {
    char path[PATH_SIZE];
    sprintf(path, "/proc/%d/%s", getpid(), map_type);
    printf("%s %d %d %d\n", path, inside_id, outside_id, length);
    FILE* handler = fopen(path, "w");
    fprintf(handler, "%d %d %d", inside_id, outside_id, length);
    fclose(handler);
    return 0;
}

int child_main(void* args) {
    printf("子进程启动\n");
    set_map(getpid(), "gid_map", 0, 1000, 1);
    set_map(getpid(), "uid_map", 0, 1000, 1);
    cap_t caps;
    printf("eUID=%d, eGID=%d\n", geteuid(), getegid());
    caps = cap_get_proc();
    printf("capabilities:%s\n", cap_to_text(caps, NULL));
    execv(child_args[0], child_args);
    return 1;
}

int main(int argc, char** argv) {
    printf("父进程启动\n");
    int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWUSER | SIGCHLD, NULL);
    //int child_pid = clone(child_main, child_stack + STACK_SIZE, CLONE_NEWUSER | CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWIPC | CLONE_NEWUTS | SIGCHLD, NULL);
    waitpid(child_pid, NULL, 0);
    printf("父进程结束\n");
    return 0;
}
```

测试结果:
a. 启动test_user.o发现用户id已经修改为0
b. 组ID失败(需要查找原因)