# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 19:55:03 2018

@author: duxiaoqin
Functions:
    (1) MCTS Algorithm for TicTacToe
"""

from graphics import *
from tictactoe import *
from tttdraw import *
from tttinput import *
import sys
import time
import math
from random import *

class NodeInfo:
    def __init__(self):
        self.player = None
        self.visit = 0
        self.win = 0

def MCTS(root, nodes_map):
    def Select(node):
        node_key = node.ToString()
        path.append(node_key)
        node_info = nodes_map.get(node_key)
        if node_info == None:
            node_info = NodeInfo()
            node_info.player = node.getPlayer()
            nodes_map[node_key] = node_info
            
        while node.isGameOver() == None and isFullyExpanded(node):
            node = BestUCTChild(node)
            child_key = node.ToString()
            path.append(child_key)
            child_info = nodes_map.get(child_key)
            if child_info == None:
                child_info = NodeInfo()
                child_info.player = node.getPlayer()
                nodes_map[child_key] = child_info
                
        return node
    
    def Expand(node):
        node_key = node.ToString()
        path.append(node_key)
        node_info = nodes_map.get(node_key)
        if node_info == None:
            node_info = NodeInfo()
            node_info.player = node.getPlayer()
            nodes_map[node_key] = node_info
        
        if node.isGameOver() == None:
            node = RandomUnvisitedChild(node)
            child_key = node.ToString()
            path.append(child_key)
            child_info = nodes_map.get(child_key)
            if child_info == None:
                child_info = NodeInfo()
                child_info.player = node.getPlayer()
                nodes_map[child_key] = child_info
            return node
        else:
            return node
        
    def Simulate(node):
        result = node.isGameOver()
        while result == None:
            node = RandomChild(node)
            result = node.isGameOver()
        return result
    
    def Backpropagate(result):
        for node_key in path:
            UpdateStatistics(node_key, result)
            
    def MaxVisitChild(node):
        max_visit_num = -sys.maxsize
        max_visit_child = ()
        moves = node.getAllMoves()
        for move in moves:
            tmp_node = node.clone()
            tmp_node.play(*move)
            child_info = nodes_map.get(tmp_node.ToString())
            if child_info == None:
                continue
            if max_visit_num < child_info.visit:
                max_visit_num = child_info.visit
                max_visit_child = move
        return max_visit_child
    
    def isFullyExpanded(node):
        moves = node.getAllMoves()
        for move in moves:
            tmp_node = node.clone()
            tmp_node.play(*move)
            child_info = nodes_map.get(tmp_node.ToString())
            if child_info == None:
                return False
        return True
    
    def BestUCTChild(node):
        c = 1.4142135623730951
        best_uct = -sys.maxsize
        best_uct_child = None
        node_info = nodes_map[node.ToString()]
        moves = node.getAllMoves()
        for move in moves:
            tmp_node = node.clone()
            tmp_node.play(*move)
            child_key = tmp_node.ToString()
            child_info = nodes_map[child_key]
            ucb1 = child_info.win / child_info.visit + \
                   c * math.sqrt(math.log(node_info.visit) / child_info.visit)
            if best_uct < ucb1:
                best_uct = ucb1
                best_uct_child = move
        if best_uct_child != None:
            node.play(*best_uct_child)
        return node
    
    def RandomChild(node):
        moves = node.getAllMoves()
        node.play(*moves[randint(0, len(moves) - 1)])
        return node

    def RandomUnvisitedChild(node):
        moves = node.getAllMoves()
        while True:
            tmp_node = node.clone()
            move = moves[randint(0, len(moves) - 1)]
            tmp_node.play(*move)
            child_info = nodes_map.get(tmp_node.ToString())
            if child_info == None:
                return tmp_node
    
    def UpdateStatistics(node_key, result):
        node_info = nodes_map[node_key]
        node_info.visit += 1
        if node_info.player == TicTacToe.BLACK:
            if result == -1:
                node_info.win += 1
            elif result == 0:
                node_info.win += 0.5
        else:
            if result == 1:
                node_info.win += 1
            elif result == 0:
                node_info.win += 0.5

    decision_time = 500
    for time in range(decision_time):
        node = root.clone()
        path = []
        node = Select(node)
        simulation_node = Expand(node)
        simulation_result = Simulate(simulation_node)
        Backpropagate(simulation_result)
    return MaxVisitChild(root)

def main():
    win = GraphWin('MCTS for TicTacToe', 600, 600, autoflush=False)
    ttt = TicTacToe()
    tttdraw = TTTDraw(win)
    tttinput = TTTInput(win)
    tttdraw.draw(ttt)
    
    nodes_map = {}
    while win.checkKey() != 'Escape':
        if ttt.getPlayer() == TicTacToe.WHITE:
            move = MCTS(ttt, nodes_map)
            if move != ():
                ttt.play(*move)
        tttinput.input(ttt)
        tttdraw.draw(ttt)
        if ttt.isGameOver() != None:
            time.sleep(1)
            ttt.reset()
            tttdraw.draw(ttt)
            #win.getMouse()
    win.close()
    
if __name__ == '__main__':
    main()