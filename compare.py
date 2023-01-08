import ast
from functools import lru_cache

@lru_cache(maxsize=1024)
def difference(str1, len1, str2, len2):
    if len2*len1 > 0:
        # Удаление символа в строке 1
        d1 = difference(str1, len1 - 1, str2, len2) + 1
        # Удаление символа в строке 2
        d2 = difference(str1, len1, str2, len2 - 1) + 1
        # Замена символа в одной из строк
        d3 = (difference(str1, len1 - 1, str2, len2 - 1)
            +int(str1[len1 - 1] != str2[len2 - 1]))
        return min(d1, d2, d3)  
    else:
        return max(len2, len1)

class Standardizator(ast.NodeTransformer):
    
    def __init__(self):
        self.names = {}
    def visit_BinOp(self, node: ast.BinOp):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if isinstance(node.left, ast.Num) and isinstance(node.right, ast.Num):
            if isinstance(node.op, ast.Add):
                result = ast.Num(n = node.left.n + node.right.n)
                node = ast.copy_location(result, node)
            elif isinstance(node.op, ast.Mult):
                result = ast.Num(n = node.left.n * node.right.n)
                node = ast.copy_location(result, node)
        return node
    
    def visit_Name(self, node: ast.Name):
        if (node.id) in self.names:
            node.id = self.names[node.id]
        else:
            new_id = f"a{str(hex(len(self.names)))[2:]}a"
            self.names[node.id] = new_id
            node.id = new_id
        return node
        

tree = ast.parse("y = 2 * 1; y = y + 1; y += 1")
std = Standardizator()
tree = std.visit(tree)

print(ast.dump(tree))
print(ast.unparse(tree))


if __name__ == '__main__':
    str1 = "y = 3+4;z = 2*2*y;print(y+z)"
    str2 = "variable1=7;variable2=     (4 * variable1); print(variable1+variable2)"

    print(round((difference(str1, len(str1), str2, len(str2))/max(len(str1),len(str2)))*100,3))
