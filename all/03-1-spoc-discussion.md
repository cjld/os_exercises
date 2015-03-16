# lec5 SPOC思考题


NOTICE
- 有"w3l1"标记的题是助教要提交到学堂在线上的。
- 有"w3l1"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 个人思考题
---

请简要分析最优匹配，最差匹配，最先匹配，buddy systemm分配算法的优势和劣势，并尝试提出一种更有效的连续内存分配算法 (w3l1)
```
  + 采分点：说明四种算法的优点和缺点
  - 答案没有涉及如下3点；（0分）
  - 正确描述了二种分配算法的优势和劣势（1分）
  - 正确描述了四种分配算法的优势和劣势（2分）
  - 除上述两点外，进一步描述了一种更有效的分配算法（3分）
 ```
- [x]  

>
* 最优匹配:
  * 优点: 可以较好地避免大空间被拆分, 减小外部碎片的大小
  * 缺点: 查找效率慢
* 最差匹配:
  * 优点: 可以避免出现过多的小碎片, 适合中等大小的分配
  * 缺点: 因为每次使用的是最大的空闲块可能导致后期无法分配大空间
* 最先匹配:
  * 优点: 可以较好地避免大空间被拆分, 高地址段可以保留大块空间
  * 缺点: 查找效率慢
* 伙伴系统:
  * 优点: 避免的外部碎片，而且分配和回收都十分高效。
  * 缺点: 内碎片较大, 但最多2倍
* 循环首次匹配，其分配过程类似最先分配，
区别是每次分配都从上一次命中的内存块继续往后搜索；

## 小组思考题

请参考ucore lab2代码，采用`struct pmm_manager` 根据你的`学号 mod 4`的结果值，选择四种（0:最优匹配，1:最差匹配，2:最先匹配，3:buddy systemm）分配算法中的一种或多种，在应用程序层面(可以 用python,ruby,C++，C，LISP等高语言)来实现，给出你的设思路，并给出测试用例。 (spoc)

```
如何表示空闲块？ 如何表示空闲块列表？
[(start0, size0),(start1,size1)...]
在一次malloc后，如果根据某种顺序查找符合malloc要求的空闲块？如何把一个空闲块改变成另外一个空闲块，或消除这个空闲块？如何更新空闲块列表？
在一次free后，如何把已使用块转变成空闲块，并按照某种顺序（起始地址，块大小）插入到空闲块列表中？考虑需要合并相邻空闲块，形成更大的空闲块？
如果考虑地址对齐（比如按照4字节对齐），应该如何设计？
如果考虑空闲/使用块列表组织中有部分元数据，比如表示链接信息，如何给malloc返回有效可用的空闲块地址而不破坏
元数据信息？
伙伴分配器的一个极简实现
http://coolshell.cn/tag/buddy
```

学号尾号为73, 实现最差匹配.
通过参考 `ucore_lab\labcodes_answer\lab8_result\kern\mm\pmm.h` 中的结构,
实现了代码:
* [test.py 测试用例](./src/03-1-spoc/test.py)
* [pmm.py 内存管理算法](./src/03-1-spoc/pmm.py)
我使用python实现的几个结构如下:

```
class mem_node:
    def __init__(self, start, size)
    def __lt__(self, other)
    def __eq__(self, other)
    def split(self, size)
    def del_node(self)

  class pmm_manager:
      def __init__(self, root)
      def alloc_node(self, size)
      def free_node(self, node)
```
mem_node为一个空闲快的数据结构, 在pmm_manager中有一个list, nodes, 储存了所有快的信息.
可以查看对应的free和alloc的代码, 在mem_node中有一个属性`is_used`代表这个内存块是否空闲.

可以直接运行代码[test.py](./src/03-1-spoc/test.py)得到测试结果, 这里我模拟了若干个内存
的申请和释放, 可以将test.py的代码输出结果进行分析
```
alloc mem size : 100/188
Can't alloc new mem (614, 32)
free mem size : (658, 77)/188
alloc mem size : 100/265
(994, 16)
alloc mem size : 69/165
Can't alloc new mem (614, 32)
free mem size : (359, 30)/165
alloc mem size : 69/195
Can't alloc new mem (350, 39)
free mem size : (948, 64)/195
alloc mem size : 69/259
(995, 15)
alloc mem size : 15/190
(996, 16)
alloc mem size : 45/175
Can't alloc new mem (614, 32)
free mem size : (749, 86)/175
alloc mem size : 45/261
(997, 16)
alloc mem size : 36/216
(998, 17)
alloc mem size : 80/180
Can't alloc new mem (614, 32)
free mem size : (172, 88)/180
alloc mem size : 80/268
(999, 17)
```
这里的`alloc mem size : 80/268` 表示剩余内存为268, 申请80, 而从test代码中可以看出我们
的总内存大小为1024, 所以改算法的内存利用率大约为80%左右, 不算太差

test中使用的测试方法是每次生成一个1~100的内存申请, 如果失败则在已申请的内存中随机释放一个,
然后重复这个过程

---

## 扩展思考题

阅读[slab分配算法](http://en.wikipedia.org/wiki/Slab_allocation)，尝试在应用程序中实现slab分配算法，给出设计方案和测试用例。

## “连续内存分配”与视频相关的课堂练习

### 5.1 计算机体系结构和内存层次
MMU的工作机理？

- [x]  

>  http://en.wikipedia.org/wiki/Memory_management_unit

L1和L2高速缓存有什么区别？

- [x]  

>  http://superuser.com/questions/196143/where-exactly-l1-l2-and-l3-caches-located-in-computer
>  Where exactly L1, L2 and L3 Caches located in computer?

>  http://en.wikipedia.org/wiki/CPU_cache
>  CPU cache

### 5.2 地址空间和地址生成
编译、链接和加载的过程了解？

- [x]  

>  

动态链接如何使用？

- [x]  

>  


### 5.3 连续内存分配
什么是内碎片、外碎片？

- [x]  

>  

为什么最先匹配会越用越慢？

- [x]  

>  

为什么最差匹配会的外碎片少？

- [x]  

>  

在几种算法中分区释放后的合并处理如何做？

- [x]  

>  

### 5.4 碎片整理
一个处于等待状态的进程被对换到外存（对换等待状态）后，等待事件出现了。操作系统需要如何响应？

- [x]  

>  

### 5.5 伙伴系统
伙伴系统的空闲块如何组织？

- [x]  

>  

伙伴系统的内存分配流程？

- [x]  

>  

伙伴系统的内存回收流程？

- [x]  

>  

struct list_entry是如何把数据元素组织成链表的？

- [x]  

>  
