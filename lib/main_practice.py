import tkinter
import customtkinter
import yaml


# Load the YAML file
with open("yaml/example.yaml", "r") as file:
    data = yaml.safe_load(file)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#root = Tk()
root = customtkinter.CTk()

root.title("Tkinter.com - CustomTKinter Tabs")
#root.inconbitmap("images/codemy.ico")
root.geometry("700x300")

# create Tabview
my_tab = customtkinter.CTkTabview(root,
                                  width=600,
                                  height=250,
                                  corner_radius=10,
                                  fg_color="silver",
                                  segmented_button_fg_color="black",
                                  segmented_button_selected_color="red",
                                  segmented_button_selected_hover_color="pink",
                                  segmented_button_unselected_color="grey",
                                  segmented_button_unselected_hover_color="blue",
                                  text_color="black") #command=used to inserta a command)
my_tab.pack(pady=10)

# Create tabs
tab_1 = my_tab.add("Tab 1")
tab_2 = my_tab.add("Tab 2")

# Put stuff in tabs
my_button = customtkinter.CTkButton(tab_1,text="click me",fg_color="black")
my_button.pack()

# Run app
root.mainloop()