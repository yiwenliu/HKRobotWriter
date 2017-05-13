#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/28

import os
import sys
if __name__ == '__main__':
    '''
    #import demo2
    print os.path.join('D:/foo','foo')
    print 'cwd:  {}'.format(os.getcwd())
    #print sys.argv[0]
    print os.path.join(sys.argv[0], os.pardir)
    print os.path.abspath(os.path.join(sys.argv[0], os.pardir))
    print os.path.abspath('template')
    #print '-----'
    #print os.path.realpath('.')
    #print __file__ if os.path.isabs(__file__) else os.path.abspath(__file__)
    print sys.path
    print os.path.join(sys.path[0], os.pardir)
    print os.path.abspath(os.path.join(sys.path[0], os.pardir))
    print '-----'
    #print sys.argv
    '''
    print os.getcwd()
    print os.path.join(os.path.dirname(sys.argv[0]), os.pardir)
    print os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))
    os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))
    print os.path.exists(os.path.join('templates', 'closing_fx_en'))
    print os.path.join('templates', 'closing_fx_en')