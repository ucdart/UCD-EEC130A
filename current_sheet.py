# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:52:44 2015

@author: Xiaoguang
"""

import matplotlib 
matplotlib.use('nbagg')

#%matplotlib inline

# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import numpy as np
from itertools import product, combinations

from matplotlib.patches import Rectangle, PathPatch

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

#plotting

#view angle
ax.view_init(elev=45., azim=25.)

#do not show axis
plt.axis('off')
plt.show()

#constants
h = 0.8
w = 1.5

p_ds = np.array([0.7,0.7,0])

#point of observation
p_Ob = np.array([0,0,h])

#current vector
v_Js = np.array([0,1,0])

#draw current rectangle
#alpha controls the transparency
p = Rectangle((0,-5), w, 10, alpha=0.1)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0,zdir="z")


def draw_problem():
    ax.clear()
    
    #draw x, y, z axes
    from matplotlib.patches import FancyArrowPatch
    from mpl_toolkits.mplot3d import proj3d
    
    class Arrow3D(FancyArrowPatch):
        def __init__(self, xs, ys, zs, *args, **kwargs):
            FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
            self._verts3d = xs, ys, zs
    
        def draw(self, renderer):
            xs3d, ys3d, zs3d = self._verts3d
            xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
            self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
            FancyArrowPatch.draw(self, renderer)
    
    x_axis = Arrow3D([0,1],[0,0],[0,0], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    y_axis = Arrow3D([0,0],[0,1],[0,0], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    z_axis = Arrow3D([0,0],[0,0],[0,1], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    
    ax.add_artist(x_axis)
    ax.add_artist(y_axis)
    ax.add_artist(z_axis)

    #draw current vector
    Js = Arrow3D([p_ds[0],p_ds[0]],[p_ds[1],p_ds[1]+0.2],[0,0], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    ax.add_artist(Js)
    
    #draw ds rectangle
    print('p_ds='+str(p_ds))
    p = Rectangle((p_ds[0]-0.05,p_ds[1]-0.05), 0.1, 0.1, alpha=0.2)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=0,zdir="z")
    
    #draw R vector
    v_R = p_Ob - p_ds
    R = Arrow3D([p_ds[0],p_Ob[0]],[p_ds[1],p_Ob[1]],[p_ds[2],p_Ob[2]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax.add_artist(R)
    
    #dH vector
    v_dH = np.cross(v_Js, v_R)
    dH = Arrow3D([p_Ob[0],p_Ob[0]+v_dH[0]],[p_Ob[1],p_Ob[1]+v_dH[1]],[p_Ob[2],p_Ob[2]+v_dH[2]], mutation_scale=10, lw=1, arrowstyle="-|>", color="r")
    ax.add_artist(dH)

draw_problem()

##widgets
axcolor = 'lightgoldenrodyellow'
ax_ds_x = plt.axes([0.25, 0.04, 0.5, 0.03], axisbg=axcolor)
s_ds_x = Slider(ax_ds_x, 'x position of ds', 0.1, w, valinit=0.7)

ax_ds_y = plt.axes([0.25, 0.00, 0.5, 0.03], axisbg=axcolor)
s_ds_y = Slider(ax_ds_y, 'y position of ds', -w, w, valinit=0.7)

def update(val):
    print(s_ds_x.val)
    print(s_ds_y.val)
    global p_ds
    p_ds = np.array([s_ds_x.val,s_ds_y.val,0])
    draw_problem()    
    fig.canvas.draw_idle()
s_ds_x.on_changed(update)
s_ds_y.on_changed(update)


