from pmm import *
from random import *

root_node = mem_node(0, 1024)
px = pmm_manager(root_node)

ps = []
for i in range(1000):
    print(i, len(ps))
    #while px.free_mem < 700:
    #    node = ps.pop( randint(0, len(ps)-1) )
    #    px.free_node(node)

    mem_size = randint(1,100)
    while 1:
        node = px.alloc_node(mem_size)
        if node is None:
            node = ps.pop( randint(0, len(ps)-1) )
            px.free_node(node)
        else:
            break
    ps.append(node)
