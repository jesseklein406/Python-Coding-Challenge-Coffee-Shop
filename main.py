#!/usr/bin/env python
"""A GUI that simulates grinding coffee beans for customers

The 'sell', 'restock', and 'service_grinder' functions
generate functions that are easy to bind to events.
The 'update' function loads the window, i.e. when an event is fired.
My favorite thing about coffee is the spelling.
"""

import Tkinter, tkMessageBox
import coffee


def sell(root, shelf):
    """Return a callable 'sell' function and then refresh the window"""
    def f():
        shelf.sell()
        root.winfo_children()[0].destroy()  # erases old "screen" frame
        update(root, shelf.shop)
    return f


def restock(root, shelf):
    """Return a callable 'restock' function and then refresh the window"""
    def f():
        shelf.restock()
        root.winfo_children()[0].destroy()
        update(root, shelf.shop)
    return f


def service_grinder(root, shop):
    """Return a callable 'service_grinder' function and then refresh the window"""
    def f(event):
        shop.service_grinder()
        root.winfo_children()[0].destroy()
        update(root, shop)
    return f

def update(root, shop):
    """Load the window upon startup or when an event is fired"""
    screen = Tkinter.Frame(root)   # primary frame, entire screen
    screen.pack(padx="10")
    
    left_content = Tkinter.Frame(screen)   # left third, grinder area  
    left_content.pack(side="left")
    
    grinder_image = Tkinter.PhotoImage(file="grinder.gif")
    grinder_button = Tkinter.Label(left_content, image=grinder_image)  # make image clickable
    grinder_button.pack()
    grinder_button.bind("<Button-1>", service_grinder(root, shop))
    
    grinder_label = Tkinter.Label(left_content, text=
    u"Grinds since last serviced: {}\nClick the grinder to service grinder\
    \n\nThe grinder must be serviced every 20 grinds.\nIt costs $40 to service.".format(
        shop.grinder.grinds_since_service))
    
    grinder_label.pack(side="top")
    
    canvas = Tkinter.Canvas(screen, width=280, height=400)   # middle third, drawing area
    canvas.pack(side="left")
    
    # Construct the coffee shelf piece by piece
    shelf_left = canvas.create_line(10, 60, 10, 360, width=10, capstyle="round")
    shelf_right = canvas.create_line(270, 60, 270, 360, width=10, capstyle="round")
    shelf_4 = canvas.create_line(10, 75, 270, 75, width=8)
    shelf_3 = canvas.create_line(10, 165, 270, 165, width=8)
    shelf_2 = canvas.create_line(10, 255, 270, 255, width=8)
    shelf_1 = canvas.create_line(10, 345, 270, 345, width=8)
    
    coffee_image = Tkinter.PhotoImage(file="coffee.gif")
    # Draw an image for the number of bags on each shelf
    # Shelves are counted from the ground up, but customers grab
    # the product from eye level and down
    for i in range(shop.shelf.third_shelf):
        canvas.create_image(15 + 50 * i, 161, image=coffee_image, anchor="sw")
    for i in range(shop.shelf.second_shelf):
        canvas.create_image(15 + 50 * i, 251, image=coffee_image, anchor="sw")
    for i in range(shop.shelf.first_shelf):
        canvas.create_image(15 + 50 * i, 341, image=coffee_image, anchor="sw")
    
    right_content = Tkinter.Frame(screen)   # right third, selling center
    right_content.pack(side="left")
    
    sell_button = Tkinter.Button(right_content, text=u"Sell coffee", command=sell(root, shop.shelf))
    restock_button = Tkinter.Button(right_content, text=u"Restock", command=restock(root, shop.shelf))
    sell_button.pack()
    restock_button.pack(side="top")
    
    instructions = Tkinter.Label(right_content, text=
    u"Your Money: ${}\nWhole bean coffee sells for $8 a bag retail\n\
    and costs $5 a bag wholesale.\n\nHalf your customers will request to have the beans ground.\n\
    You can hold a maximum of 15 bags on your shelf.".format(shop.money))
    
    instructions.pack(side="top")
    
    root.mainloop()
    
def main():
    root = Tkinter.Tk()
    root.title("Coffee Shop")
    shop = coffee.Shop()
    update(root, shop)

if __name__ == "__main__":
    main()