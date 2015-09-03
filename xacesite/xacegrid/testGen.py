#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'jcteng'

from layoutGen import  xaceGridNode

tmpstr='''

<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-11">11</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-10 am-u-sm-offset-1">10, offset 1</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-9 am-u-sm-offset-2">9, offset 2</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-8 am-u-sm-offset-3">8, offset 3</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-7 am-u-sm-offset-4">7, offset 4</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-6 am-u-sm-offset-5">6, offset 5</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-5 am-u-sm-offset-6">5, offset 6</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-4 am-u-sm-offset-7">4, offset 7</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-3 am-u-sm-offset-8">3, offset 8</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-2 am-u-sm-offset-9">2, offset 9</div>
</div>
<div class="am-g">
  <div class="am-u-sm-1">1</div>
  <div class="am-u-sm-1 am-u-sm-offset-10">1, offset 10</div>
</div>
'''

root = xaceGridNode()
node1 = xaceGridNode(groupInGrid=False,styleDiv=4)
root.addNode(node1)
node1 = xaceGridNode(groupInGrid=False,styleDiv=4)
root.addNode(node1)
node1 = xaceGridNode(groupInGrid=False,styleDiv=4)
node1.templatePath=tmpstr
root.addNode(node1)
node2 = xaceGridNode()
root.addNode(node2)
node1 = xaceGridNode(groupInGrid=False,styleDiv=4)
root.addNode(node1)
node2 = xaceGridNode()
root.addNode(node2)
print root.to_son()
print root.mergeTemplates()
