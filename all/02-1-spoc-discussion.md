#lec 3 SPOC Discussion

## 第三讲 启动、中断、异常和系统调用-思考题

## 3.1 BIOS
 1. 比较UEFI和BIOS的区别。
 1. 描述PXE的大致启动流程。

## 3.2 系统启动流程
 1. 了解NTLDR的启动流程。
 1. 了解GRUB的启动流程。
 1. 比较NTLDR和GRUB的功能有差异。
 1. 了解u-boot的功能。

## 3.3 中断、异常和系统调用比较
 1. 举例说明Linux中有哪些中断，哪些异常？
 1. Linux的系统调用有哪些？大致的功能分类有哪些？  (w2l1)

Linux 系统调用大约320个

* 进程控制
  * fork 创建一个子进程
  * exit 终止发出调用的进程
  * exec 以新进程代替原有进程，但PID保持不变
  * ......

* 文件系统控制

其中包含文件读写操作，文件系统操作。如read, write.

* 系统控制

ioctl I/O总控制函数
uname	获取当前UNIX系统的名称、版本和主机等信息

* 内存管理等

brk 改变数据段地址
mlock 内存页面加锁。
mmap	映射虚拟内存页

* 网络管理

getdomainname 取域名

* socket控制

socket 建立socket。

* 用户管理

getuid 获取用户标识号

* 进程间通信

其中包括信号，消息，管道，信号量，共享内存。

```
  + 采分点：说明了Linux的大致数量（上百个），说明了Linux系统调用的主要分类（文件操作，进程管理，内存管理等）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```

 1. 以ucore lab8的answer为例，uCore的系统调用有哪些？大致的功能分类有哪些？(w2l1)
 在`syscall.c`文件中, 包括了所有系统调用

 *进程管理*

    sys_exit, sys_fork, sys_wait, sys_exec, sys_yield, sys_kill, sys_getpid, sys_sleep.

 *文件系统控制*

   sys_pgdir, sys_gettime, sys_open, sys_close, sys_read, sys_write, sys_seek, sys_fstat, sys_dup, sys_getdirentry.

 *内存管理*

   sys_lab6_set_priority, sys_fsync, sys_getcwd, sys_putc.


 ```
  + 采分点：说明了ucore的大致数量（二十几个），说明了ucore系统调用的主要分类（文件操作，进程管理，内存管理等）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```

## 3.4 linux系统调用分析
 1. 通过分析[lab1_ex0](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex0.md)了解Linux应用的系统调用编写和含义。(w2l1)

 objdump: display information from object files. 主要功能有对可执行程序进行反汇编.

 nm: 查看文件符号表, 如下为nm的输出信息


     0804a01c d hello
    08048294 T _init
    08049f0c t __init_array_end
    08049f08 t __init_array_start
    0804847c R _IO_stdin_used
    00000006 a IPPROTO_TCP
             w _ITM_deregisterTMCloneTable
             w _ITM_registerTMCloneTable
    08049f10 d __JCR_END__
    08049f10 d __JCR_LIST__
             w _Jv_RegisterClasses
    08048460 T __libc_csu_fini
    080483f0 T __libc_csu_init
             U __libc_start_main@@GLIBC_2.0

  file 查看文件类型


 ```
  + 采分点：说明了objdump，nm，file的大致用途，说明了系统调用的具体含义
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）

 ```

 1. 通过调试[lab1_ex1](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex1.md)了解Linux应用的系统调用执行过程。(w2l1)


  strace : trace system calls and signals, 可以通过 strace 命令查看系统调用和信号.
  如下为使用 strace 分析 lab-ex0.exe 中系统调用的过程, 可以清晰的看到系统调用的参数和返回值.


    execve("./lab1-ex0.exe", ["./lab1-ex0.exe"], [/* 74 vars */]) = 0
    [ Process PID=6871 runs in 32 bit mode. ]
    brk(0)                                  = 0x8b19000
    access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
    mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff7753000
    access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
    open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
    fstat64(3, {st_mode=S_IFREG|0644, st_size=93381, ...}) = 0
    mmap2(NULL, 93381, PROT_READ, MAP_PRIVATE, 3, 0) = 0xfffffffff773c000
    close(3)                                = 0
    access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
    open("/lib32/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
    read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\300\233\1\0004\0\0\0"..., 512) = 512
    fstat64(3, {st_mode=S_IFREG|0755, st_size=1742588, ...}) = 0
    mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff773b000
    mmap2(NULL, 1751676, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0xfffffffff758f000
    mmap2(0xf7735000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a5000) = 0xfffffffff7735000
    mmap2(0xf7738000, 10876, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xfffffffff7738000
    close(3)                                = 0
    mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff758e000
    set_thread_area(0xffb35790)             = 0
    mprotect(0xf7735000, 8192, PROT_READ)   = 0
    mprotect(0x8049000, 4096, PROT_READ)    = 0
    mprotect(0xf7775000, 4096, PROT_READ)   = 0
    munmap(0xf773c000, 93381)               = 0
    write(1, "hello world\n", 12hello world
    )           = 12
    exit_group(12)                          = ?




 ```
  + 采分点：说明了strace的大致用途，说明了系统调用的具体执行过程（包括应用，CPU硬件，操作系统的执行过程）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```

## 3.5 ucore系统调用分析
 1. ucore的系统调用中参数传递代码分析。
 1. ucore的系统调用中返回结果的传递代码分析。
 1. 以ucore lab8的answer为例，分析ucore 应用的系统调用编写和含义。
 1. 以ucore lab8的answer为例，尝试修改并运行ucore OS kernel代码，使其具有类似Linux应用工具`strace`的功能，即能够显示出应用程序发出的系统调用，从而可以分析ucore应用的系统调用执行过程。

## 3.6 请分析函数调用和系统调用的区别
 1. 请从代码编写和执行过程来说明。
   1. 说明`int`、`iret`、`call`和`ret`的指令准确功能
