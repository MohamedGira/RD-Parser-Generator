import graphviz
import os
path=os.path.dirname(os.path.abspath(__file__))
print(path)

class Node:
  def __init__(self, name,children=None,state=0):
    #children: dict of childNode and edgenames
    self.name = name
    self.children = children
    self.state=state
  def __str__(self) :
        return str(self.name)

 

A=Node('A',)
B=Node('B')
C=Node('C')
D=Node('D')
E=Node('E')
F=Node('F')
G=Node('G')
H=Node('H')

tree={A:{B:['ε','-']},
      B:{C:"".join([str(i) for i in range (9)])},
      C:{B:'ε',D:'ε'},
      D:{E:'.',H:'ε'},
      E:{F:'ε',H:'ε'},
      F:{G:"".join([str(i) for i in range (9)])},
      G:{H:'ε',F:'ε'},
      H:{}}

q0=Node('q0')
q1=Node('q1')
q2=Node('q2',state=1)
tree2={
   q0:{q0:'a',q1:'b'},
   q1:{q2:'b',q0:'a'},
   q2:{q2:'ba'}
}


def draw_graph(treedict,labe2l=None):
   # Graphically represents the given ROBDD using graphviz.
    g = graphviz.Digraph(format='pdf')
    g.attr(rankdir='TB')
    g.attr('node', shape='circle')
    g.attr(label=labe2l)
    drawn_nodes=[]

    def draw_node(nodedict):
      """
      takes a dict of node and its node as a key and another dict of each children and edge name as value
      """
      node=list(nodedict.keys())[0]
      print(node)
      """    if node in drawn_nodes:
      # Node has already been drawn, so just create a reference to it
        return """
      # Mark the node as drawn
      drawn_nodes.add(node)
      
      # Node is not a terminal node, so label it with its variable name and draw its children
      g.node(str(id(node)), node.name)
      print(nodedict[node])
      for key in nodedict[node]:
        value=nodedict[node][key]
        for i in value:
          g.edge(str(id(node)), str(id(key)),label=str(i))
    
    
    drawn_nodes = set()
    for key in treedict:
       value=treedict[key]
       draw_node({key:value}) 
    
    return g

def draw_graph_visualized(currentNode,treedict,labe2l=None,at=0,fromedge='',previousnode=''):
   # Graphically represents the given ROBDD using graphviz.
    g = graphviz.Digraph(format='png')
    g.attr(rankdir='TB')
    g.graph_attr['labeljust'] = 'l'
    g.graph_attr['fontname'] = 'Consolas'
    
    g.attr('node', shape='circle')
    s='\l'+'_'*at+'^'+'_'*(len(labe2l)-at)
    if labe2l:
      g.attr(label=labe2l+s)
    drawn_nodes=[]
    
    
    def draw_node(nodedict):
      """
      takes a dict of node and its node as a key and another dict of each children and edge name as value
      """
      node=list(nodedict.keys())[0]
      """    if node in drawn_nodes:
      # Node has already been drawn, so just create a reference to it
        return """
      # Mark the node as drawn
      drawn_nodes.add(node)
      

      if(node==currentNode):
        if node.state==1:
          g.node(str(id(node)), node.name,color='green')
        else:
          g.node(str(id(node)), node.name,color='red')
      else:
        g.node(str(id(node)), node.name)
      for key in nodedict[node]:
        value=nodedict[node][key]
        for i in value:
          if(node==previousnode and i==fromedge and key==currentNode):
            g.edge(str(id(node)), str(id(key)),label=str(i),color='orange')
          else:
             g.edge(str(id(node)), str(id(key)),label=str(i))
    
    drawn_nodes = set()
    for key in treedict:
      value=treedict[key]
      draw_node({key:value}) 
    return g


def processInput(currentNode,treedict,inputstring,label2l=None):  
  outgraphs=[]
  outgraphs.append(draw_graph_visualized(currentNode,treedict,inputstring))

  for ind,i in enumerate(inputstring):
    revelem= {value: key for key, value in treedict[currentNode].items()}
    flag=False
    prevnode=currentNode
    for t in revelem:
      # print( t, i,inputstring,ind)
       if i in t:
          flag=True
          currentNode=revelem[t]
          break 
    if not flag:
       raise Exception("not DFA")
    outgraphs.append(draw_graph_visualized(currentNode,treedict,labe2l=inputstring,at=ind,fromedge=i,previousnode=prevnode))
  return outgraphs


def generate_gif(filepattern):
  from PIL import Image
  import glob

  # Set the file pattern to load the images
  file_pattern = os.path.join(path,str(filepattern)+'_*.png')

  # Set the output GIF filename
  output_gif_filename = os.path.join(path,f'{str(filepattern)}.gif')

  # Load the images into a list
  images = []
  for i,filename in enumerate( (glob.glob(file_pattern))):
      print(filepattern+f'_{i}')
      images.append(Image.open(os.path.join(path,filepattern)+f'_{i}.png'))

  # Save the list of images as a GIF file
  images[0].save(output_gif_filename, save_all=True, append_images=images[1:], duration=800, loop=0)

def myModule(currentNode,treedict,inputstring):
  graphs=processInput(currentNode,treedict,inputstring)
  for i,g in enumerate (graphs):
    g.render(f'{inputstring}_{str(i)}',path)
  
  generate_gif(inputstring)


myModule(q0,tree2,'abababbbaa')