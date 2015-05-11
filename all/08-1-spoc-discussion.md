# 死锁与IPC(lec 20) spoc 思考题


- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。

## 个人思考题

### 死锁概念
 - 尝试举一个生活中死锁实例。
 - 可重用资源和消耗资源有什么区别？

### 可重用和不可撤销；
 - 资源分配图中的顶点和有向边代表什么含义？
 - 出现死锁的4个必要条件是什么？

### 死锁处理方法
 - 死锁处理的方法有哪几种？它们的区别在什么地方？
 - 安全序列的定义是什么？

### 进程的最大资源需要量小于可用资源与前面进程占用资源的总合；
 - 安全、不安全和死锁有什么区别和联系？

### 银行家算法
 - 什么是银行家算法？
 - 安全状态判断和安全序列是一回事吗？

### 死锁检测
 - 死锁检测与安全状态判断有什么区别和联系？

> 死锁检测、安全状态判断和安全序列判断的本质就是资源分配图中的循环等待判断。

### 进程通信概念
 - 直接通信和间接通信的区别是什么？
  本质上来说，间接通信可以理解为两个直接通信，间接通信中假定有一个永远有效的直接通信方。
 - 同步和异步通信有什么区别？
### 信号和管道
 - 尝试视频中的信号通信例子。
 - 写一个检查本机网络服务工作状态并自动重启相关服务的程序。
 - 什么是管道？

### 消息队列和共享内存
 - 写测试用例，测试管道、消息队列和共享内存三种通信机制进行不同通信间隔和通信量情况下的通信带宽、通信延时、带宽抖动和延时抖动方面的性能差异。

## 小组思考题

 - （spoc） 每人用python实现[银行家算法](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab7/deadlock/bankers-homework.py)。大致输出可参考[参考输出](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab7/deadlock/example-output.txt)。除了`YOUR CODE`部分需要填写代码外，在算法的具体实现上，效率也不高，可进一步改进执行效率。

程序和对应的输出见
<https://github.com/cjld/ucore_lab/blob/master/related_info/lab7/deadlock/bankers-homework.py>
和
<https://github.com/cjld/ucore_lab/blob/master/related_info/lab7/deadlock/output.txt>


 - (spoc) 以小组为单位，请思考在lab1~lab5的基础上，是否能够实现IPC机制，请写出如何实现信号，管道或共享内存（三选一）的设计方案。

以实现信号为例, 在现有的 proc struct 中增加一个 signal_handle 的函数指针, 用于
储存信号处理程序

当一个进程向另一个进程发送信号时, 我们修改目标进程的栈, 将信号处理程序压入栈
中, 同时将对应的参数也一并压入栈中

 - (spoc) 扩展：用C语言实现某daemon程序，可检测某网络服务失效或崩溃，并用信号量机制通知重启网络服务。[信号机制的例子](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab7/ipc/signal-ex1.c)

这里我们可以通过 `int kill(pid_t pid, int signo);` 发送0信号的返回值来判断
进程是否存活

部分代码如下:
```

int main()
{
   pid_t deamon_pid = get_deamon_pid();

   while(1)
   {
      sleep(1000);
      int a = kill(deamon_pid, 0);
      if (a == -1)
        deamon_pid = restart_proc();
   }
   return EXIT_SUCCESS;
}
```

 - (spoc) 扩展：用C语言写测试用例，测试管道、消息队列和共享内存三种通信机制进行不同通信间隔和通信量情况下的通信带宽、通信延时、带宽抖动和延时抖动方面的性能差异。[管道的例子](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab7/ipc/pipe-ex2.c)


测试程序如下:
```
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctime>
int
main(int argc, char *argv[])
{
    int pipefd[2];
    pid_t cpid;
    char buf;
    int n;
    long long tt;
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <string>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    n = atoi(argv[1]);
    fprintf(stdout, "size %d\n", argc);
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    cpid = fork();
    if (cpid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }
    tt = clock();
    if (cpid == 0) {    /* Child reads from pipe */
        close(pipefd[1]);          /* Close unused write end */
        while (read(pipefd[0], &buf, 1) > 0);
        //write(STDOUT_FILENO, "\n", 1);
        close(pipefd[0]);
        _exit(EXIT_SUCCESS);
    } else {            /* Parent writes argv[1] to pipe */
        close(pipefd[0]);          /* Close unused read end */
        while (n--)
          write(pipefd[1], " ", 1);
        close(pipefd[1]);          /* Reader will see EOF */
        wait(NULL);                /* Wait for child */

        fprintf(stdout, "time %f", (clock()-tt)*1. / CLOCKS_PER_SEC);
        fflush(stdout);
        exit(EXIT_SUCCESS);
    }
}

```

测试结果如下:
```
size 10
time 0.000142
size 100
time 0.001112
size 1000
time 0.006507
size 10000
time 0.062490
size 100000
time 0.614841
size 1000000
time 5.929161
```
