from html.parser import HTMLParser
from html import escape
class Node:
 def __init__(self,tag='',attrs=(),parent=None,text=''):
  self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[];self.data=text
 def all(self,test):
  out=[]
  for c in self.children:
   if test(c):out.append(c)
   out.extend(c.all(test))
  return out
 def has(self,cl):return cl in self.attrs.get('class','').split()
 def text(self):return self.data if not self.tag else ''.join(c.text() for c in self.children if c.tag not in ('script','style'))
 def html(self):
  if not self.tag:return escape(self.data)
  at=''.join(' '+k+'="'+escape(v or '',quote=True)+'"' for k,v in self.attrs.items())
  return '<'+self.tag+at+'>'+('' if self.tag in Parser.void else ''.join(c.html() for c in self.children)+'</'+self.tag+'>')
class Parser(HTMLParser):
 void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.root=Node('root');self.cur=self.root;self.feed(s)
 def handle_starttag(self,t,a):
  n=Node(t,a,self.cur);self.cur.children.append(n)
  if t not in self.void:self.cur=n
 def handle_startendtag(self,t,a):self.handle_starttag(t,a);self.handle_endtag(t)
 def handle_endtag(self,t):
  n=self.cur
  while n.parent:
   if n.tag==t:self.cur=n.parent;return
   n=n.parent
 def handle_data(self,d):self.cur.children.append(Node(parent=self.cur,text=d))
def parse(s):return Parser(s).root
