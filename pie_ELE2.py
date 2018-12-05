#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pie chart for review paper

import matplotlib.pyplot as plt
import numpy as np

#define stuff
my_blue = np.array([30,144,255])/255
pale_green = np.array([152,251,152])/255
pale_red   = np.array([240,128,128])/255
pale_gray  = np.array([169,169,169])/255

def rotatetext(text):
    angle = np.rad2deg(np.arctan2(*text.get_position()[::-1]))
    text.set(rotation = angle - 90*np.sign(angle), 
             rotation_mode="anchor", ha="center", va="center")
    
    
    
fig, ax = plt.subplots(figsize=(10, 10))

#inner layer: type of networks
group_names = ['Landscape', 'Interaction', 'Others']
group_vals = [46,49,34]
group_colors = ['w']*3

#middle layer: information, suff vs insuff
info_names = ['Suff. Info.', 'Insuff. Info.', \
              'Suff. Info.', 'Insuff. Info.',\
              'Suff. Info.', 'Insuff. Info.']
info_vals = np.array([[27,19],[25,24],[14,20]])
info_colors = [my_blue,'gray']*3

#outer layer: numbers
corr_vals = np.array([[25,0,0,0,2], [0,6,4,9,0],\
                     [23,0,0,0,2], [0,8,5,11,0],\
                     [13,0,0,0,1], [0,4,9,7,0]])
corr_colors = ['green',pale_green,pale_gray,pale_red,'red']*6

#inner layer
pie_properties1 = ax.pie(group_vals, radius=1/1.9, colors=group_colors, 
       labels=group_names, labeldistance=.8, textprops={'fontsize': 18},
       wedgeprops=dict(width=0.3/1.9, edgecolor='k', linewidth=2))

for text in pie_properties1[1]:
    rotatetext(text)

#middle layer
pie_properties2 = ax.pie(info_vals.flatten(), radius=(1+0.4)/1.9, colors=info_colors,
       labels=info_names, labeldistance=.82, textprops={'fontsize': 15},
       wedgeprops=dict(width=0.4/1.9, edgecolor='w'))

for text in pie_properties2[1]:
    rotatetext(text)

#outer layer
corr_labs = np.array([[25,'','','',' '], ['',6,' ',9,''],\
                 [23,'','','',2], ['',8,5,11,''],\
                 [13,'','','',' '], ['',4,9,7,'']]) #'' are zeros
                                                                 #' ' are labels that need
                                                                 #to be placed manually to
                                                                 #look good
pie_properties3, texts = ax.pie(corr_vals.flatten(), radius=(1+0.4+0.5)/1.9, colors=corr_colors,
       labels=corr_labs.flatten(), labeldistance=0.83, textprops={'fontsize': 16},
       wedgeprops=dict(width=0.5/1.9, edgecolor='w'))

#Lines
in_rad = (1-0.3)/1.9;
mid_rad = 1.01/1.9;
out_rad = (1+0.4+0.49)/1.9;

angle1 = group_vals[0]/sum(group_vals)*360
angle2 = group_vals[1]/sum(group_vals)*360
angle3 = group_vals[2]/sum(group_vals)*360

midangle1 = info_vals[0][0]/sum(group_vals)*360
midangle2 = (sum(info_vals[0])+info_vals[1][0])/sum(group_vals)*360
midangle3 = (sum(info_vals[0])+sum(info_vals[1])+info_vals[2][0])/sum(group_vals)*360

#all layers
ax.plot([in_rad, out_rad], [0, 0], linewidth=2.5, color='k', clip_on=False)

ax.plot([in_rad*np.cos(np.radians(angle1)), out_rad*np.cos(np.radians(angle1))], \
         [in_rad*np.sin(np.radians(angle1)), out_rad*np.sin(np.radians(angle1))], \
         linewidth=2.5, color='k', clip_on=False)

ax.plot([in_rad*np.cos(np.radians(-angle3)), out_rad*np.cos(np.radians(-angle3))], \
         [in_rad*np.sin(np.radians(-angle3)), out_rad*np.sin(np.radians(-angle3))], \
         linewidth=2.5, color='k', clip_on=False)

#2nd and 3rd layer
ax.plot([mid_rad*np.cos(np.radians(midangle1)), out_rad*np.cos(np.radians(midangle1))], \
         [mid_rad*np.sin(np.radians(midangle1)), out_rad*np.sin(np.radians(midangle1))], \
         linewidth=2.5, color='k', clip_on=False)

ax.plot([mid_rad*np.cos(np.radians(midangle2)), out_rad*np.cos(np.radians(midangle2))], \
         [mid_rad*np.sin(np.radians(midangle2)), out_rad*np.sin(np.radians(midangle2))], \
         linewidth=2.5, color='k', clip_on=False)

ax.plot([mid_rad*np.cos(np.radians(midangle3)), out_rad*np.cos(np.radians(midangle3))], \
         [mid_rad*np.sin(np.radians(midangle3)), out_rad*np.sin(np.radians(midangle3))], \
         linewidth=2.5, color='k', clip_on=False)

#legend
wedges = pie_properties3[0:4]
lbl = ['Correct','Seem correct','Unclear','Seem wrong','Wrong']
ax.legend(wedges, lbl,
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1),prop={'size': 16})

#fix rogue labels
ax2=fig.add_axes([0,0,1,1], frameon=False)
ax2.set_yticklabels([]) #comment this when placing labels. it helps.
ax2.set_xticklabels([]) #this too
ax2.tick_params(axis='both', which='both', length=0)

ax2.text(0.583, 0.74, '2', fontsize=16)
ax2.text(0.47, 0.745, '4', fontsize=16)
ax2.text(0.65, 0.265, '1', fontsize=16)

ax.set(aspect="equal")#, title='Pie plot with `review`')
plt.show()


fig.savefig('pie_ELE1.png', bbox_inches='tight', dpi=1000)