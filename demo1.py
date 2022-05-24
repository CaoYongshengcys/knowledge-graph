from py2neo import Graph, Node, Relationship
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474/browser/', auth = ('neo4j','123456'))
graph.delete_all() #清除neo4j中原有的结点等所有信息
# 创建结点
node1 = Node('person', name = 'cys')   #该结点语义类型是person  结点名字是cys  也是它的属性
node2 = Node('major',name = 'AI')       #该结点语义类型是major  结点名字是AI 也是它的属性
node3 = Node('person',name = 'bobo')          #该结点语义类型是person  结点名字是bobo   也是它的属性
#给结点node1 添加一个属性 age
node1['age'] = 18
#给结点node2 添加一个属性 college
node2['college'] = 'AI college'
#给结点node3 添加一个属性 sex
node3['sex'] = '男'
#把结点实例化 在Neo4j中显示出来
graph.create(node1)
graph.create(node2)
graph.create(node3)
# 创建关系
maojor = Relationship(node1, '专业', node2)
friends = Relationship(node1, '朋友', node3)
maojor1 = Relationship(node3, '专业', node2)
#把关系实例化 在Neo4j中显示出来
graph.create(maojor)
graph.create(maojor1)
graph.create(friends)
