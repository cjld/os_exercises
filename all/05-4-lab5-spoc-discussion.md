# lab5 spoc 思考题

- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。


## 个人思考题

### 总体介绍

 - 第一个用户进程创建有什么特殊的？
 - 系统调用的参数传递过程？
 - getpid的返回值放在什么地方了？

### 进程的内存布局

 - 尝试在进程运行过程中获取内核堆栈和用户堆栈的调用栈？
 - 尝试在进程运行过程中获取内核空间中各进程相同的页表项（代码段）和不同的页表项（内核堆栈）？

### 执行ELF格式的二进制代码-do_execve的实现

 - 在do_execve中进程清空父进程时，当前进程是哪一个？在什么时候开始使用新加载进程的地址空间？
 - 新加载进程的第一级页表的建立代码在哪？

### 执行ELF格式的二进制代码-load_icode的实现

 - 第一个内核线程和第一个用户进程的创建有什么不同？
 - 尝试跟踪分析新创建的用户进程的开始执行过程？

### 进程复制

 - 为什么新进程的内核堆栈可以先于进程地址空间复制进行创建？
 - 进程复制的代码在哪？复制了哪些内容？
 - 进程复制过程中有哪些修改？为什么要修改？

### 内存管理的copy-on-write机制
 - 什么是写时复制？
 - 写时复制的页表在什么时候进行复制？共享地址空间和写时复制有什么不同？

## 小组练习与思考题

### (1)(spoc) 在真实机器的u盘上启动并运行ucore lab,

请准备一个空闲u盘，然后请参考如下网址完成练习

https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-boot-with-grub2-in-udisk.md

> 注意，grub_kernel的源码在ucore_lab的lab1_X的git branch上，位于 `ucore_lab/labcodes_answer/lab1_result`

(报告可课后完成)请理解grub multiboot spec的含义，并分析ucore_lab是如何实现符合grub multiboot spec的，并形成spoc练习报告。

**答**

出现问题:

*   `nasm` not found, 我们apt-get 一个即可
*   在真机上测试之前, 先尝试是否可以使用virtualbox来boot我们的u盘,
    使用virtualbox boot u 盘的方法[在此](http://www.pendrivelinux.com/boot-a-usb-flash-drive-in-virtualbox/)

然后就可以在真机以及虚拟机里跑了
![](./pic/541.jng)
![](./pic/542.jng)

**理解grub multiboot spec**

我们 diff Lab1-X 和 Lab1, 可以发现主要增加了一个文件夹 `mboot`, 其中的文件包含了
为了支持grub所需要做的事情

在文件`entry.asm`里面能看到这么一段代码
```
; This is the GRUB Multiboot header. A boot signature
dd MULTIBOOT_HEADER_MAGIC
dd MULTIBOOT_HEADER_FLAGS
dd MULTIBOOT_CHECKSUM
dd 0, 0, 0, 0, 0 ; address fields
```
这段代码是 GRUB Multiboot 的头, 有我们提供给 grub, 告诉grub启动方式

调查规范, 发现每一项的功能主要如下:
```
0  u32  magic  必需   magic域是标志头的魔数，它必须等于十六进制值0x1BADB002。
4  u32  flags  必需   flags域指出OS映像需要引导程序提供或支持的特性
8  u32  checksum  必需    域checksum是一个32位的无符号值，当与其他的magic域（也就是magic和flags）相加时，结果必须是32位的无符号值0（即magic + flags + checksum = 0）。
12  u32  header_addr  包含对应于Multiboot头的开始处的地址——这也是magic值的物理地址。这个域用来同步OS映象偏移量和物理内存之间的映射。
16  u32  load_addr  如果flags[16]被置位
20  u32  load_end_addr  如果flags[16]被置位
24  u32  bss_end_addr  如果flags[16]被置位
28  u32  entry_addr  如果flags[16]被置位
32  u32  mode_type  如果flags[2]被置位
36  u32  width  如果flags[2]被置位
40  u32  height  如果flags[2]被置位
44  u32  depth  如果flags[2]被置位
```

然后就是 grub 启起来以后, 给我们kernel提供的信息, 其中
eax为magic number `0x2BADB002`, ebx 里包含了我们的**引导信息**
我们可以在multiboot.h中找到定义, 也就是结构`multiboot_info_t`

`multiboot_info_t` 的加载代码可以在`entry.asm`里面找到这么一段代码
```
; interpret multiboot information
    extern multiboot_init
    push ebx
    call multiboot_init
```
这样就完成了我们对引导信息的加载

### (2)(spoc) 理解用户进程的生命周期。

> 需写练习报告和简单编码，完成后放到git server 对应的git repo中

### 练习用的[lab5 spoc exercise project source code](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab5/lab5-spoc-discuss)


#### 掌握知识点
1. 用户进程的启动、运行、就绪、等待、退出
2. 用户进程的管理与简单调度
3. 用户进程的上下文切换过程
4. 用户进程的特权级切换过程
5. 用户进程的创建过程并完成资源占用
6. 用户进程的退出过程并完成资源回收

> 注意，请关注：内核如何创建用户进程的？用户进程是如何在用户态开始执行的？用户态的堆栈是保存在哪里的？

阅读代码，在现有基础上再增加一个用户进程A，并通过增加cprintf函数到ucore代码中，
能够把个人思考题和上述知识点中的内容展示出来：即在ucore运行过程中通过`cprintf`函数来完整地展现出来进程A相关的动态执行和内部数据/状态变化的细节。(约全面细致约好)

请完成如下练习，完成代码填写，并形成spoc练习报告
