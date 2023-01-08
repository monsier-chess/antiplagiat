import ast
from functools import lru_cache

# Поиск расстояния Ливенштейна между двумя строками
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

# Предобработка кода через ast
class Standardizator(ast.NodeTransformer):
    
    def __init__(self):
        self.names = {}

    # Вычисление тривиальных арифметических операций + и *
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

    # Замена имён переменных
    def visit_Name(self, node: ast.Name):
        if (node.id) in self.names:
            node.id = self.names[node.id]
        else:
            new_id = f"a{str(hex(len(self.names)))[2:]}"
            self.names[node.id] = new_id
            node.id = new_id
        return node

if __name__ == '__main__':
    
    # Обрабатываются сразу несколько способов плагиата:
    # 1) Замены констант на простые числовые выражения
    # 2) Замена имён переменных
    # 3) Изменения, никак не влияющие на код (например, добавление пустых строк,
    # пробелов между операндами, комментариев)
    
    # Примеры полного плагиата кода
    str1 = "y = 3+4;z = 2*2*y;\n#комментарий\nprint(y+z)"
    str2 = "variable1=7;variable2=     (4 * variable1); print(variable1 + variable2)"
    
    std1 = Standardizator()
    clean1 = ast.unparse(std1.visit(ast.parse(str1)))
    std2 = Standardizator()
    clean2 = ast.unparse(std2.visit(ast.parse(str2)))
    
    print(clean1)
    print(clean2)
    
    print(difference(clean1, len(clean1), clean2, len(clean2))/max(len(clean1), len(clean2)))
