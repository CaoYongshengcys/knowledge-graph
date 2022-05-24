import pandas as pd
from py2neo import Node, Graph, Relationship, NodeMatcher

path = r'Invoice_data_Demo.xls'
invoice_data = pd.read_excel(path, header = 0)
# 把发票名称抽取出来
invoice_name_list = []
for i in range(0, len(invoice_data)):
    invoice_name_list.append(invoice_data['发票名称'][i])
invoice_name_list = list(set(invoice_name_list)) #去重
invoice_name_list # 第一类label的节点

# 把除了发票代码这一列去掉，所有的都抽取了，一共抽取了35 * 26 = 910个数据
invoice_value_list = []
for i in range(0, len(invoice_data)):
    for j in range(1, len(invoice_data.columns)):
        invoice_value_list.append(invoice_data[invoice_data.columns[j]][i])

invoice_value_list = list(set(invoice_value_list))# 

# 转变为str类型
invoice_value_list = [str(i) for i in invoice_value_list]

name1_list = []
name2_list = []
rel_list = []
for i in range(0, len(invoice_data)): # 35
    for j in range(1, len(invoice_data.columns)): # 1--26
        name1_list.append(invoice_data[invoice_data.columns[0]][i]) # 第一类label属性的节点
        rel_list.append(invoice_data.columns[j]) # 关系
        name2_list.append(invoice_data[invoice_data.columns[j]][i])

name2_list = [str(i) for i in name2_list] # 里面有整数和浮点数，要变成str
tuple_total = list(zip(name1_list,rel_list,name2_list))
graph = Graph('http://localhost:7474/browser/', auth = ('neo4j','123456'))
graph.delete_all() # 清除neo4j里面的所有数据
label_1 = '发票名称'
label_2 = '发票值'

#把节点导入neo4j中
def create_node(invoice_name_list, invoice_value_list):
    for name in invoice_name_list:
        node_1 = Node(label_1, name = name)
        graph.create(node_1)
    for name in invoice_value_list:
        node_2 = Node(label_2, name = name)
        graph.create(node_2)
create_node(invoice_name_list, invoice_value_list)
matcher = NodeMatcher(graph)

# 导入关系
for i in range(0, len(tuple_total)):
    rel = Relationship(matcher.match(label_1, name = tuple_total[i][0]).first(),
                      tuple_total[i][1],
                      matcher.match(label_2, name = tuple_total[i][2]).first()
                      )
    graph.create(rel)

