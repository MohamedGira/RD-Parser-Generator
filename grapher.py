import re
import graphviz
import os
path=os.path.join( os.path.dirname(os.path.abspath(__file__)))
print(path)
from myutils import *
from PIL import Image, ImageTk
import imageio.v2 as imageio
import glob
import os
import time


class Node:
  def __init__(self, name,children=None,state=0):
    #children: dict of childNode and edgenames
    self.name = name
    self.children = children
    self.state=state
  def __str__(self) :
        return f'{self.name} , {self.state}'

 

A=Node('A',)
B=Node('B')
C=Node('C')
D=Node('D')
E=Node('E')
F=Node('F')
G=Node('G')
H=Node('H')

tree={A:{B:'ε-'},
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




""" 
fortran_words='program implicit none end if else end integer real parameter do character print* read*'
fortran_words=fortran_words.split(' ')
for word in fortran_words:
  draw_graph_no_splt(accept_word(word)).render(word.replace('*',''),cleanup=True,directory=os.path.join(path,'outputs'))
 """

""" while(1):
  word=input('enter word to create DFA for: ')
  draw_graph_no_splt(accept_word(word)).render(word,cleanup=True,directory=os.path.join(path,'outputs')) """

class Visualizer:
    
    def __init__(self) -> None:
      pass
    @staticmethod
    def draw_graph_no_splt(treedict,labe2l=None):
    # Graphically represents the given ROBDD using graphviz.
      g = graphviz.Digraph(format='png')
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
        
        
        if node.state==1:
          g.node(str(id(node)), node.name,shape='doublecircle')
        else:
          g.node(str(id(node)), node.name)
        print(nodedict[node])
        for key in nodedict[node]:
          value=nodedict[node][key]
          
          g.edge(str(id(node)), str(id(key)),label=value)
      
      
      drawn_nodes = set()
      for key in treedict:
        value=treedict[key]
        draw_node({key:value}) 
      
      return g
    @staticmethod
    def draw_graph(treedict,labe2l=None):
      # Graphically represents the given ROBDD using graphviz.
        g = graphviz.Digraph(format='png')
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
    @staticmethod
    def draw_graph_visualized(currentNode,treedict,labe2l='None',at=0,fromedge='',previousnode='',theme=None):
      # Graphically represents the given tree using graphviz.
        

        
        if theme not in themes:
          theme = list(themes.keys())[0]
        palette=themes[theme]
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='TB')
        g.graph_attr['labeljust'] = 'l'
        g.graph_attr['bgcolor'] = palette['graph_bg_color']
        g.attr(dpi='300')
        g.node_attr['fontname']=g.edge_attr['fontname']='Arial'
        #g.node_attr['fontcolor']='grey'
        #g.edge_attr['fontcolor']='grey'
        g.graph_attr['fontname'] = 'Consolas'
        g.attr('node', shape='circle')
        s='\l'+' '*at+'^'+' '*(len(labe2l)-at)
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
              g.node(str(id(node)), node.name,color=palette['picked_node_color_final'],shape='doublecircle',style='filled', fillcolor=palette['picked_node_bg_color_final'])
            else:
              g.node(str(id(node)), node.name,color=palette['picked_node_color_non_final'],style='filled', fillcolor=palette['picked_node_bg_color_non_final'])
          else:
            if node.state==1:
              g.node(str(id(node)), node.name,color=palette['node_color'],shape='doublecircle')
            else:
              g.node(str(id(node)), node.name,color=palette['node_color'])
        
          for key in nodedict[node]:
            value=nodedict[node][key]
            for i in value:
              print(node,previousnode,i,fromedge, key,currentNode ,node==previousnode and i==fromedge and key==currentNode)
              print()
              if(node==previousnode and i==fromedge and key==currentNode):
                g.edge(str(id(node)), str(id(key)),label=str(i),color=palette['picked_edge_color'],penwidth='2.0',fontcolor=palette['picked_font_color'])
              else:
                g.edge(str(id(node)), str(id(key)),label=str(i),color=palette['edge_color'])
        
        drawn_nodes = set()
        for key in treedict:
          value=treedict[key]
          draw_node({key:value}) 
        return g
    @staticmethod
    def draw_graph_visualized_no_split(currentNode,treedict,labe2l='None',at=0,fromedge='',previousnode='',theme=None):
      # Graphically represents the given ROBDD using graphviz.
        from myutils import themes

        
        if theme not in themes:
          theme = list(themes.keys())[0]
        palette=themes[theme]
        g = graphviz.Digraph(format='png')
        g.attr(rankdir='TB')
        g.graph_attr['labeljust'] = 'l'
        g.graph_attr['bgcolor'] = palette['graph_bg_color']
        g.attr(dpi='100')
        g.node_attr['fontname']=g.edge_attr['fontname']='Arial'
        #g.node_attr['fontcolor']='grey'
        #g.edge_attr['fontcolor']='grey'
        g.graph_attr['fontname'] = 'Consolas'
        g.attr('node', shape='circle')
        s='\l'+' '*at+'^'+' '*(len(labe2l)-at)
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
              g.node(str(id(node)), node.name,color=palette['picked_node_color_final'],shape='doublecircle',style='filled', fillcolor=palette['picked_node_bg_color_final'])
            else:
              g.node(str(id(node)), node.name,color=palette['picked_node_color_non_final'],style='filled', fillcolor=palette['picked_node_bg_color_non_final'])
          else:
            if node.state==1:
              g.node(str(id(node)), node.name,color=palette['node_color'],shape='doublecircle')
            else:
              g.node(str(id(node)), node.name,color=palette['node_color'])
        
          for key in nodedict[node]:
            value=nodedict[node][key]
            
            i=value
        
            if(node==previousnode and i==fromedge and key==currentNode):
              g.edge(str(id(node)), str(id(key)),label=str(i),color=palette['picked_edge_color'],penwidth='2.0',fontcolor=palette['picked_font_color'])
            else:
              g.edge(str(id(node)), str(id(key)),label=str(i),color=palette['edge_color'])
        
        drawn_nodes = set()
        for key in treedict:
          value=treedict[key]
          draw_node({key:value}) 
        return g

    @staticmethod
    def generate_gif(graphs,path=path,name=None):
      if name==None:
        output_gif_filename=f'{str(int(time.time()))}.gif'
      writer = imageio.get_writer(output_gif_filename, mode='I', duration=0.8*len(graphs))
      print(0.8*len(graphs))
      for graph in graphs:
          # Render the graph as a PNG
          png_bytes = graph.pipe(format='png')

          # Read the PNG bytes into an imageio image
          img = imageio.imread(png_bytes)

          # Add the image to the writer
          writer.append_data(img)

      # Close the writer to finalize the GIF
      writer.close()
      return output_gif_filename
    @staticmethod
    def processInput(currentNode,treedict,inputstring,label2l=None,style=None):  
      outgraphs=[]
      outgraphs.append(Visualizer.draw_graph_visualized(currentNode,treedict,inputstring,theme=style))

      for ind,i in enumerate(inputstring):
        #revelem:reverse dict for the current node's {Node-> Char that leads to it}
        revelem= {value: key for key, value in treedict[currentNode].items()}
        flag=False
        prevnode=currentNode
        for t in revelem:
          if i in t:
              flag=True
              currentNode=revelem[t]
              break 
        if not flag:
          raise Exception("not DFA")
        outgraphs.append(Visualizer.draw_graph_visualized(currentNode,treedict,labe2l=inputstring,at=ind,fromedge=i,previousnode=prevnode,theme=style))
      return outgraphs

    @staticmethod
    def processInput_no_split(currentNode,treedict,inputstring,label2l=None,style=None):  
      outgraphs=[]
      outgraphs.append(Visualizer.draw_graph_visualized_no_split(currentNode,treedict,inputstring,theme=style))

      for ind,i in enumerate(inputstring):
        revelem= {value: key for key, value in treedict[currentNode].items()}
        flag=False
        prevnode=currentNode
        for t in revelem:
          #print(f"pattern: {t} ,string: {repr(re.escape(i))}")
          if re.findall (t,re.escape(i)):
              flag=True
              currentNode=revelem[t]
              break 
        if not flag:
          raise Exception("not DFA")
        outgraphs.append(Visualizer.draw_graph_visualized_no_split(currentNode,treedict,labe2l=inputstring,at=ind,fromedge=t,previousnode=prevnode,theme=style))
      return outgraphs
    @staticmethod
    def GIF(currentNode,treedict,inputstring,remove_source_images=False,style=None):  
      graphs=Visualizer.processInput(currentNode,treedict,inputstring,style=style)
      Visualizer.generate_gif(graphs,os.path.join(path,'animations'))
      
    @staticmethod
    def GIF_NO_SPLIT(currentNode,treedict,inputstring,remove_source_images=False,style=None):
      if currentNode==None:
        currentNode=treedict.keys()[0]
      graphs=Visualizer.processInput_no_split(currentNode,treedict,inputstring,style=style)
      fpath=Visualizer.generate_gif(graphs,os.path.join(path,'animations'))

      return fpath
    
class DFA:
  def __init__(self,accpets):
    self.word=accpets
    self.dict=self.accept_word(accpets)
  @staticmethod
  def accept_word(word)->dict:
    nodearr=[]
    reg=Node('reject')
    
    for i in range(len(word)+1):
        nodearr.append(Node(f'{i+1}'))
    nodearr[-1].state=1

    tree={}
    
    for i in range(len(nodearr)-1):
        tree.update({nodearr[i]:{nodearr[i+1]:f'{re.escape( word[i].lower())}|{re.escape(word[i].upper())}',
                                 reg:f'[^({re.escape(word[i].lower())}|{re.escape(word[i].upper())})]'}})
        #tree[word[i]]={tree[word[i+1]]:l,reg:f'[^{word[i]}]'}
    tree.update({reg:{reg:('(.)+')}})
    tree.update({nodearr[-1]:{reg:('(.)+')}})
    
    return tree
    #draw_graph(tree)
  def try_word(self,word):
     return Visualizer.GIF_NO_SPLIT(list(self.dict.keys())[0],self.dict,word,True)
  def __str__(self) -> str:
    return str(self.dict)


""" A=DFA('implicit')
A.try_word('IMpldsicit')
  """

""" q3=Node('q3')
q4=Node('q4',state=1)
rejectt=Node('rejectt')
tree2={
   q3:{q4:']',rejectt:'[^(])]'},
   q4:{rejectt:'[^(])]'},
   rejectt:{rejectt:'(.)+'}
}
Visualizer.GIF(q0,tree2,'ababaabbbaa',remove_source_images=True,style='modern')

 """

#Visualizer.draw_graph_no_splt(DFA.accept_word(']')).render(']',cleanup=True,directory=os.path.join(path,'outputs'))
A=DFA(']')
A.try_word(']]]')
  