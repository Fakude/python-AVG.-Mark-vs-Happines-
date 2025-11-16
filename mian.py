import matplotlib.pyplot as plt 
import numpy as np
# numpy array 
x = np.array([2022,2023,2024,2025,2026,2027])
y1 = np.array([53,63,70,75.5,80,85])
y2 =np.array([75,38,55,64,75,90])

#font dictionary 
title = dict(fontsize =15,
            family ="Arial",
            fontweight="bold",
            )

label1 = dict(fontsize =15,
            family ="Arial",
             )

label2 = dict(fontsize =15,
            family ="Arial",
             )

plt.grid()

plt.title("Avg Mark vs Avg Happiness",**title)

plt.xlabel("Year",**label1)
plt.ylabel("Average Index Score",**label2)


# Line color dictionary
line_style1 = dict(marker ="o",
                    markerfacecolor ="#1858ed",
                      markeredgecolor="#1858ed",
                    linewidth=3,
                    color="#ed1818")

line_style2 = dict(marker ="o",
                    markerfacecolor ="#1858ed",
                      markeredgecolor="#1858ed",
                    linewidth=3,
                    color="#0ee93aec" )


plt.plot(x,y1,**line_style1,label="Average Mark")
plt.plot(x,y2,**line_style2,label="Average Happiness ")

plt.legend(loc="upper left")

plt.show()
