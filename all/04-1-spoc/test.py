
f = open('./../04-1-spoc-memdiskdata.md')

raw = f.readlines()
data_ram = raw[5:133]
data_disk = raw[137:265]

def get_data(data, phy_addr):
    page = phy_addr >> 5
    index = phy_addr % 32 * 3 + 9
    return eval('0x' + data[page][index:index+2])

PDBR = 0xd80

def vtop(v_addr):
    pde = v_addr >> 10
    pde_c = get_data(data_ram, PDBR + pde)
    if (pde_c>>7)==0:
        print "warning, no page"
    pte = pde_c & 0b1111111
    pte_c = get_data(data_ram, pte*32 + ((v_addr>>5)&31))
    p_addr = pte_c*32 + v_addr%32
    return p_addr

def g_data(addr):
    if (addr >> 12) == 0:
        print 1, '%x' % (addr&0xfff)
        return get_data(data_disk, addr&0xfff)
    else:
        print 2, '%x' % (addr&0xfff)
        return get_data(data_ram, addr&0xfff)

print(g_data(vtop(0x6653)))
print(g_data(vtop(0x1c13)))
print(g_data(vtop(0x6890)))
print(g_data(vtop(0x0af6)))
print(g_data(vtop(0x1e6f)))
