# lab4 spoc 思考题

- 有"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的ucore_code和os_exercises的git repo上。

## 个人思考题

### 总体介绍

(1) ucore的线程控制块数据结构是什么？

### 关键数据结构

(2) 如何知道ucore的两个线程同在一个进程？

(3) context和trapframe分别在什么时候用到？

(4) 用户态或内核态下的中断处理有什么区别？在trapframe中有什么体现？

### 执行流程

(5) do_fork中的内核线程执行的第一条指令是什么？它是如何过渡到内核线程对应的函数的？
```
tf.tf_eip = (uint32_t) kernel_thread_entry;
/kern-ucore/arch/i386/init/entry.S
/kern/process/entry.S
```

(6)内核线程的堆栈初始化在哪？
```
tf和context中的esp
```

(7)fork()父子进程的返回值是不同的。这在源代码中的体现中哪？

(8)内核线程initproc的第一次执行流程是什么样的？能跟踪出来吗？

## 小组练习与思考题

(1)(spoc) 理解内核线程的生命周期。

> 需写练习报告和简单编码，完成后放到git server 对应的git repo中

### 掌握知识点
1. 内核线程的启动、运行、就绪、等待、退出
2. 内核线程的管理与简单调度
3. 内核线程的切换过程

### 练习用的[lab4 spoc exercise project source code](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab4/lab4-spoc-discuss)


请完成如下练习，完成代码填写，并形成spoc练习报告

### 1. 分析并描述创建分配进程的过程

> 注意 state、pid、cr3，context，trapframe的含义

首先是`proc_state`, 可以发现主要包含了4个枚举类, 可以发现在
`do_wait`和`do_exit`几个函数里有对proc_state的转换代码.
```
// process's state in his life cycle
enum proc_state {
    PROC_UNINIT = 0,  // uninitialized
    PROC_SLEEPING,    // sleeping
    PROC_RUNNABLE,    // runnable(maybe running)
    PROC_ZOMBIE,      // almost dead, and wait parent proc to reclaim his resource
};
```

`pid` 这是进程的唯一标示符

然后是cr3, 我们可以发现在`proc_run`这个函数里有通过lcr3来改变cr3, 进而通过switch_to
来切换进程.

```
uintptr_t cr3;                              // CR3 register: the base addr of Page Directroy Table(PDT)
```

context 和 trapframe 则保存了切换上下文时需要保存的东西.



### 练习2：分析并描述新创建的内核线程是如何分配资源的

> 注意 理解对 kstack, trapframe, context等的初始化

首先在 `kernel_thread` 函数中设置trapframe, 然后调用 do_fork 来完成剩下的任务

其主要流程有

*   alloc_proc:   create a proc struct and init fields (lab4:exercise1)
*   setup_kstack: alloc pages with size KSTACKPAGE as process kernel stack
*   copy_thread:  setup the trapframe on the  process's kernel stack top and
    setup the kernel entry point and stack of process
*   hash_proc:    add proc into proc hash_list
*   get_pid:      alloc a unique pid for process
*   wakup_proc:   set proc->state = PROC_RUNNABLE



当前进程中唯一，操作系统的整个生命周期不唯一，在get_pid中会循环使用pid，耗尽会等待

### 练习3：阅读代码，在现有基础上再增加一个内核线程，并通过增加cprintf函数到ucore代码中
能够把进程的生命周期和调度动态执行过程完整地展现出来

这里我修改了 init_main 函数, 使其创建一个子进程

```
static int child_main(void *arg) {
    cprintf("child kernel_thread, pid = %d, ppid = %d, name = %s\n", current->pid,
    		current->parent->pid,  get_proc_name(current));
    return 0;
}

// init_main - the second kernel thread used to create user_main kernel threads
static int
init_main(void *arg) {
    cprintf(" kernel_thread, pid = %d, name = %s\n", current->pid, get_proc_name(current));
    kernel_thread(child_main, "child", 0);
	schedule();
    cprintf(" kernel_thread, pid = %d, name = %s , arg  %s \n", current->pid, get_proc_name(current), (const char *)arg);
	schedule();
    cprintf(" kernel_thread, pid = %d, name = %s ,  en.., Bye, Bye. :)\n",current->pid, get_proc_name(current));
    return 0;
}
```

通过`make qemu` 获得了一下输出:
```
kernel_thread, pid = 1, name = init1
kernel_thread, pid = 2, name = init2
child kernel_thread, pid = 3, ppid = 1, name =
do_exit: proc pid 3 will exit
do_exit: proc  parent c02ff070
child kernel_thread, pid = 4, ppid = 2, name =
do_exit: proc pid 4 will exit
do_exit: proc  parent c02ff0d8
kernel_thread, pid = 1, name = init1 , arg  init main1: Hello world!!
kernel_thread, pid = 2, name = init2 , arg  init main2: Hello world!!
kernel_thread, pid = 1, name = init1 ,  en.., Bye, Bye. :)
do_exit: proc pid 1 will exit
do_exit: proc  parent c02ff008
kernel_thread, pid = 2, name = init2 ,  en.., Bye, Bye. :)
do_exit: proc pid 2 will exit
do_exit: proc  parent c02ff008
do_wait: begin
do_wait: has kid find child  pid1
do_wait: begin
do_wait: has kid find child  pid2
do_wait: begin
do_wait: has kid find child  pid3
do_wait: begin
do_wait: has kid find child  pid4
do_wait: begin
```
在这里我们可以看到, 父进程调用子进程, 然后子进程成功print并且找到父进程的pid

以及running, exit等生命周期

具体代码详见 <https://github.com/cjld/ucore_lab/tree/master/related_info/lab4/lab4-spoc-discuss>

### 练习4 （非必须，有空就做）：增加可以睡眠的内核线程，睡眠的条件和唤醒的条件可自行设计，并给出测试用例，并在spoc练习报告中给出设计实现说明

### 扩展练习1: 进一步裁剪本练习中的代码，比如去掉页表的管理，只保留段机制，中断，内核线程切换，print功能。看看代码规模会小到什么程度。
