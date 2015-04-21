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
![](./pic/541.png)
![](./pic/542.png)

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

**答**

首先, 我们在`schedule`函数中添加代码, 这样就可以非常方便的
看到我们进程切换的过程, 添加的 `cprintf` 函数如下:
```
void
schedule(void) {
    bool intr_flag;
    list_entry_t *le, *last;
    struct proc_struct *next = NULL;
    local_intr_save(intr_flag);
    {
    	struct proc_struct* tmp = current;
    	cprintf("schedule proc %d, state %s\n", current->pid,
    			get_state_str(current->state));
        current->need_resched = 0;
        last = (current == idleproc) ? &proc_list : &(current->list_link);
        le = last;
        do {
            if ((le = list_next(le)) != &proc_list) {
                next = le2proc(le, list_link);
                if (next->state == PROC_RUNNABLE) {
                    break;
                }
            }
        } while (le != last);
        if (next == NULL || next->state != PROC_RUNNABLE) {
            next = idleproc;
        }
        next->runs ++;
        if (next != current) {
            proc_run(next);
        	cprintf("my state become %s\n", get_state_str(tmp->state));
        	cprintf("switch proc %d, state %s, run time %d\n",
        			next->pid, get_state_str(next->state), next->runs);
        } else {
        	cprintf("my state become %s\n", get_state_str(tmp->state));
        	cprintf("continue run proc %d, run time %d\n",
        			current->pid, current->runs);
        }
        cprintf("\n");
    }
    local_intr_restore(intr_flag);
}
```

其中 `get_state_str` 是一个用来把 proc state 转换成
字符串的小函数, 他的定义如下:
```
const char * get_state_str(enum proc_state state) {
#define ck_state(STATE) \
	if (state == STATE) \
		return "'"#STATE"'";

	ck_state(PROC_UNINIT);
	ck_state(PROC_SLEEPING);
	ck_state(PROC_RUNNABLE);
	ck_state(PROC_ZOMBIE);
}
```
然后我们运行 qemu, 因为我们得到了以下输出:
```
I am the parent. Forking the child...
I am parent, fork a child pid 3
I am the parent, waiting now..
schedule proc 2, state 'PROC_SLEEPING'
I am the child.
schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 2

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 3

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 4

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 5

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 6

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 7

schedule proc 3, state 'PROC_RUNNABLE'
my state become 'PROC_RUNNABLE'
continue run proc 3, run time 8

schedule proc 3, state 'PROC_ZOMBIE'
my state become 'PROC_RUNNABLE'
switch proc 3, state 'PROC_ZOMBIE', run time 8

waitpid 3 ok.
exit pass.
schedule proc 2, state 'PROC_ZOMBIE'
my state become 'PROC_RUNNABLE'
switch proc 2, state 'PROC_ZOMBIE', run time 2

```

运行的程序是`user/exit.c`我们来分析一下运行状态:

*   首先父进程fork一个子进程, 这时候并没有什么变化
*   父进程使用`waitpid`, 等待子进程, 这时候父进程变为
    `PROC_SLEEPING`, 然后唤醒子进程, 子进程变为`PROC_RUNNABLE`
*   子进程这时候使用`yield`, 重新返回调度器, 但是可以`runable`的进程仍然是
    自己, 所以我们可以发现中间若干次`yield`都重新切换回了自己
*   子进程退出, 变为`PROC_ZOMBIE`, 父进程重新可以调用, 变成`PROC_RUNNABLE`
*   父进程退出, 也变为`PROC_ZOMBIE`

关于资源分配情况, 我们可以在`struct proc_struct`中找到内存管理结构体
`struct mm_struct *mm`, 我们跟踪这个结构体, 发现

*   他在`load_icode`被创建
*   在`do_execve`和`do_exit`中通过统计引用计数被释放

加入对应`cprintf`函数, 发现输出符合我们的预期.

代码详见<https://github.com/cjld/ucore_lab/tree/master/related_info/lab5/lab5-spoc-discuss/kern/process>
和<https://github.com/cjld/ucore_lab/tree/master/related_info/lab5/lab5-spoc-discuss/kern/schedule>
