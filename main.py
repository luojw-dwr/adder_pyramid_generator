from math import *

class A2_node:
    def __init__(self, t, l, r):
        self.t = t
        self.l = l
        self.r = r
    def __str__(self):
        return "(A2_node: id=" + self.s + str(self.l) +", " + str(self.r) + ")"
    def __repr__(self):
        return str(self)
    def spread(self, s, arr):
        self.s = s
        self.l.spread(s+"0", arr)
        self.r.spread(s+"1", arr)
    def to_fragment(self):
        res = ""
        res += self.l.to_fragment()
        res += self.r.to_fragment()
        res += \
'''    wire[A_B_W-1:0] %so;
    A2_node A2_node_%s(
        .rst(rst),
        .clk(clk),
        .i1(%s0o),
        .i2(%s1o),
        .o(%so)
    );\n''' % (self.s, self.s, self.s, self.s, self.s)
        return res

class in_node:
    def __init__(self):
        self.t = 0
    def __str__(self):
        return "(in_node)"
    def __repr__(self):
        return str(self)
    def spread(self, s, arr):
        self.s = s
        self.i = arr.pop()
    def to_fragment(self):
        res = ""
        res += "    wire[A_B_W-1:0] %so;\n" % (self.s)
        res += "    assign %so = i%d;\n" % (self.s, self.i)
        return res

class z_node:
    def __init__(self, c):
        self.t = 0
        self.c = c
    def __str__(self):
        return "(z_node: id=" + self.s + str(self.c) + ")"
    def __repr__(self):
        return str(self)
    def spread(self, s, arr):
        self.s = s
        self.c.spread(s+"_0", arr)
    def to_fragment(self):
        res = ""
        res += self.c.to_fragment()
        res +=\
'''    wire[A_B_W-1:0] %s_o;
    z_node z_node_%s(
        .rst(rst),
        .clk(clk),
        .i(%s0o),
        .o(%so)
    );''' % (self.s, self.s, self.s, self.s)
        return res

def f(n):
    if n > 0:
        return A2_node(n, f(n-1), f(n-1))
    else:
        return in_node()

def F(n):
    N = floor(log(n)/log(2))
    lst = []
    for i in range(0, N+1):
        if n&(1<<i):
            lst.append(f(i))
    t = 0
    while len(lst) > 1:
        len_lst = len(lst)
        _lst = []
        ind = 0
        while ind < len_lst:
            if t < lst[ind].t:
                _lst.append(lst[ind])
            else:
                if ind+1 < len_lst and t >= lst[ind+1].t:
                    _lst.append(A2_node(0, lst[ind], lst[ind+1]))
                    ind += 1
                else:
                    _lst.append(z_node(lst[ind]))
            ind += 1
        t += 1
        lst = _lst
    return lst[0]

from functools import reduce
def gen(n):
    rt = F(n)
    # generate header
    print(\
'''parameter A_B_W = 32;
module adder_pyramid_%d(
    input rst,
    input clk,
%s    output reg[A_B_W-1:0] o
);\n''' % (n, reduce(lambda a,b: a+b, map(lambda x:"    input[A_B_W-1:0] i%d,\n" % x , range(n)))))
    
    # generate content
    rt.spread("a", list(range(n)))
    print(rt.to_fragment())
    
    # generate footer
    print("endmodule;")

if __name__ == "__main__":
    import sys
    gen(int(sys.argv[1]))
