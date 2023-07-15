
# LIBRARIES WE HAD USED IN THIS PROJECT

from tkinter import *
from functools import partial
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter.ttk import Entry
import tkinter.messagebox as tmsg
import random



'''                              THIS  PROGRAM IS CREATED BY 
                                       MUHAMMAD TAYYAB IFTIKHAR (00000406493)
                                       MUHAMMAD MAHAD (00000408576) 
                                       KHAWAJA HAMZA SIDDIQUI (00000409366)'''


# STANDARD CMS ID LENGTH IS ELEVEN IN OUR PROJECT SUCH AS 00000000000

# ALL THE FUNCTIONS ARE GIVEN BELOW

# FUNCTION TO LOGOUT

def BACK_TO_MAIN():
    ret = tmsg.askquestion("MAIN PAGE", "DO YOU WANT TO LOGOUT")
    if ret == 'yes':
        main()
    if ret == 'no':
        EXECUTION()


# FUNCTION FOR DISPLAYING INFORMATION ENTER BY USERS

def SEARCH_ALL():
    app_list.delete(0, END)
    f = open('user_element_info.txt', 'r')
    student_count = 0
    while 1:
        index = 0
        line = f.readline()
        data = line.split('***')
        student_count += 1
        app_list.insert(END, ' ')
        app_list.insert(END, f" STUDENT : {student_count} :-\n")
        detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
        for i in data:
            app_list.insert(END, f"{detail_list[index]} {i}\n")
            index += 1
        if not line:
            print("if not line is true")
            break


# FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON ELEMENT BASIS

def SEARCH_BY_ELEMENT():
    flag = 0
    if element_var.get().strip() == '':
        tmsg.showinfo("Error", "Invalid Entries!")
        return
    app_list.delete(0, END)
    f = open('user_element_info.txt', 'r')
    student_count = 0
    while 1:
        index = 0
        line = f.readline()
        if element_var.get().lower().strip() in line.lower():
            flag = 1
            student_count += 1
            data = line.split('***')
            app_list.insert(END, ' ')
            app_list.insert(END, f"DATA # : {student_count} :-\n")
            for i in data:
                detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
                app_list.insert(END, f"{detail_list[index]} {i}\n")
                index += 1
        if not line:
            break
    if flag == 0:
        tmsg.showinfo("Sorry", "element not found!")
    return


# FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON CMS ID BASIS

def DISPLAY_USER_INFO():
    flag = 0
    if len(str(cms1_var.get().strip())) != 11:
        tmsg.showinfo("Error", "Invalid Entries ... PLEASE TRY AGAIN !")
        return
    app_list.delete(0, END)
    f = open('user_element_info.txt', 'r')
    student_count = 0
    while 1:

        index = 0
        line = f.readline()
        data = line.split('***')
        if cms1_var.get().strip() in data:
            flag = 1
            student_count += 1
            app_list.insert(END, ' ')
            app_list.insert(END, f"DATA # 1 :  {student_count} :-\n")
            detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
            for i in data:
                app_list.insert(END, f"{detail_list[index]} {i}\n")
                index += 1
        if not line:
            break
    if flag == 0:
        tmsg.showinfo("Sorry", "student not found!")
        return


# FUNCTION FOR DISPLAYING LAYOUT OF USER's INFORMATION

def SHOW_BUTTON():
    search_rectangle = Canvas(root, bg="#051047", height=700, width=1900)
    search_rectangle.place(x=0, y=180)
    Label(search_rectangle, text="SEARCH BY CMS ID:", font=('Segoe UI', 24), fg="#FFFF00", bg='#051047').place(x=20,
                                                                                                               y=20)
    Label(search_rectangle, text="SEARCH BY ELEMENT:", font=('Segoe UI', 24), fg="#FFFF00", bg='#051047').place(x=20,
                                                                                                                y=200)
    global cms1_var
    global element_var
    cms1_var = StringVar()
    element_var = StringVar()
    Entry(search_rectangle, textvariable=cms1_var, width=30, font=20).place(x=20, y=70)
    Entry(search_rectangle, textvariable=element_var, width=30, font=20).place(x=20, y=250)

    Button(search_rectangle, text="Search", font="SegoeUI 11", command=DISPLAY_USER_INFO).place(x=300, y=100)
    Button(search_rectangle, text="Search", font="SegoeUI 11", command=SEARCH_BY_ELEMENT).place(x=300, y=280)
    Button(search_rectangle, text="Search All", font="SegoeUI 25", height=1, width=10, command=SEARCH_ALL).place(x=100,
                                                                                                                 y=320)
    sby = Scrollbar(search_rectangle)
    sby.place(x=1200, y=150)
    global app_list
    app_list = Listbox(search_rectangle, height=10, width=70, font="SegoeUI 15", yscrollcommand=sby.set, fg="#FFFF00",
                       bg="#4169E1")
    app_list.place(x=500, y=150)
    sby.config(command=app_list.yview)

    Button(root, text="BACK", font="arial 11", bg="LIGHTBLUE", command=USER_INFO).place(x=1300, y=710)


# FUNCTION FOR WRITING USER INFORMATION IN TEXT FILE

def WRITING_USER_INFO():

    f = open("user_element_info.txt", 'a')
    f.write(
        f"{cms_var.get().strip()}***{user_name_var.get().strip()}***{ele_name_var.get().strip()}***{user_info_var.get()}\n")
    f.close()
    tmsg.showinfo("information", "INFORMATION ADDED SUCCESSFULLY")
    user_info_var.set('')
    user_name_var.set('')
    ele_name_var.set('')
    cms_var.set('')


# FUNCTON THAT WILL ASK USER TO ENTER INFORMATION IF HE/SHE WANTS

def USER_INFO():

    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    Label(rectangle_doc, text="CMS ID", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=100)
    Label(rectangle_doc, text="NAME", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=200)
    Label(rectangle_doc, text="ELEMENT NAME", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=300)
    Label(rectangle_doc, text="INFORMATION", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=400)

    # DISPLAYING BUTTONS FOR INFORMATION ASKED BY USER

    global user_info_var
    global user_name_var
    global ele_name_var
    global cms_var
    user_info_var = StringVar()
    user_name_var = StringVar()
    ele_name_var = StringVar()
    cms_var = StringVar()
    Entry(rectangle_doc, textvariable=cms_var, width=30, font=20).place(x=750, y=100)
    Entry(rectangle_doc, textvariable=user_name_var, width=30, font=20).place(x=750, y=200)
    Entry(rectangle_doc, textvariable=ele_name_var, width=30, font=20).place(x=750, y=300)
    Entry(rectangle_doc, textvariable=user_info_var, width=30, font=20).place(x=750, y=400)
    Button(rectangle_doc, text="SAVE", font="arial 11", bg='lightblue', command=WRITING_USER_INFO).place(x=1040, y=450)
    Button(rectangle_doc, text="SHOW INFORMATION", font="arial 11", bg='lightblue', command=SHOW_BUTTON).place(x=750,
                                                                                                               y=450)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# TO SEARCH IMAGE ON THE BASIS OF ITS ATOMIC NUMBER

def update_image():
    global image_index
    label.configure(image=images[image_index - 1])
    Label(root, text=elements[image_index - 1], width='15', font="SegoeUI 15 bold").place(x=500, y=679)


# FUNCTION TO GO TO NEXT IMAGE

def NEXT_IMAGE():
    global image_index
    image_index += 1
    if image_index >= len(images):
        image_index = 0
    update_image()


# FUNCTION TO GO TO PREVIOUS IMAGE

def PREV_IMAGE():
    global image_index
    image_index -= 1
    if image_index < 0:
        image_index = len(images) - 1
    update_image()


# FUNCTION UPDATE INDEX OF IMAGE

def UPDATE_INDEX():
    global image_index
    try:
        image_index = int(entry_var.get())
        if image_index < 1 or image_index >= len(images) + 1:
            tmsg.showerror('Error', 'Invalid Atomic Number')
        else:
            update_image()
    except ValueError:
        tmsg.showerror('Error', 'Invalid Atomic Number')


# FUNCTION TO PRESENT PICTURES OF ELEMENTS

def PICTURES():
    Label(text=" ELEMENTAL GALLERY ", font="SegueUI 40 bold", bg="#FFFFF0").place(x=350, y=70)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    # LIST OF ELEMENT PICTURES

    image_files = ['1.PNG', '2.PNG', '3.PNG', '4.PNG', '5.PNG', '6.PNG', '7.PNG', '8.PNG', '9.PNG', '10.PNG', '11.PNG',
                   '12.PNG', '13.PNG', '14.PNG', '15.PNG', '16.PNG', '17.PNG', '18.PNG', '19.PNG', '20.PNG', '21.PNG',
                   '22.PNG', '23.PNG', '24.PNG', '25.PNG', '26.PNG', '27.PNG', '28.PNG', '29.PNG', '30.PNG', '31.PNG',
                   '32.PNG', '33.PNG', '34.PNG', '35.PNG', '36.PNG', '37.PNG', '38.PNG', '39.PNG', '40.PNG', '41.PNG',
                   '42.PNG', '43.PNG', '44.PNG', '45.PNG', '46.PNG', '47.PNG', '48.PNG', '49.PNG', '50.PNG', '51.PNG',
                   '52.PNG', '53.PNG', '54.PNG', '55.PNG', '56.PNG', '57.PNG', '58.PNG', '59.PNG', '60.PNG', '61.PNG',
                   '62.PNG', '63.PNG', '64.PNG', '65.PNG', '66.PNG', '67.PNG', '68.PNG', '69.PNG', '70.PNG', '71.PNG',
                   '72.PNG', '73.PNG', '74.PNG', '75.PNG', '76.PNG', '77.PNG', '78.PNG', '79.PNG', '80.PNG', '81.PNG',
                   '82.PNG', '83.PNG', '84.PNG', '85.PNG', '86.PNG', '87.PNG', '88.PNG', '89.PNG', '90.PNG', '91.PNG',
                   '92.PNG', '93.PNG', '94.PNG', '95.PNG', '96.PNG', '97.PNG', '98.PNG', '99.PNG', '100.PNG', '101.PNG',
                   '102.PNG', '103.PNG', '104.PNG', '105.PNG', '106.PNG', '107.PNG', '108.PNG', '109.PNG', '110.PNG',
                   '111.PNG', '112.PNG', '113.PNG', '114.PNG', '115.PNG', '116.PNG', '117.PNG', '118.PNG']

    # LIST OF ELEMENT NAMES

    global elements

    elements = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine',
                'Neon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon',
                'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt',
                'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton',
                'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium',
                'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine',
                'Xenon', 'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium',
                'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium',
                'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum',
                'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium',
                'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium',
                'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium',
                'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium',
                'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine',
                'Oganesson']

    global images
    images = [PhotoImage(file=f) for f in image_files]

    global image_index
    image_index = 0

    # DISPLAYING BUTTONS FOR PICTURES TO MOVE FORWARD AND BACKWARD

    global label
    label = Label(root, image=images[0])
    label.place(x=500, y=250)
    Label(rectangle_doc, text=elements[image_index], width='15', height='1', font="SegueUI 15 bold").place(x=500, y=500)
    Button(rectangle_doc, text='Previous', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=PREV_IMAGE).place(
        x=10, y=400)
    Button(rectangle_doc, text='Next', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=NEXT_IMAGE).place(x=100,
                                                                                                                 y=400)

    Label(rectangle_doc, text='ENTER THE ATOMIC NUMBER ', fg="#FFFF00", bg="#4169E1", font="SegueUI 15 bold").place(
        x=10, y=40)
    global entry_var
    entry_var = StringVar()
    Entry(rectangle_doc, textvariable=entry_var, width=30, font=('aerial', 10)).place(x=10, y=75)
    Button(rectangle_doc, text='Update', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=UPDATE_INDEX).place(
        x=10, y=100)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# TO CHECK ANS ENTER BY USER IS CORRECT OR NOT

def guess_check():
    root.title("QUIZ GAME")
    global score
    if ANS_VAR.get().strip().lower() == element.lower():
        Label(text="CORRECT ANSWER", font=('Segue UI', 25), fg="#FFFF00", bg="#051047").place(x=50, y=500)
        score += 10
        del elements[element]
        quiz()
    else:
        Label(text="WRONG ANSWER    ", font=('Segue UI', 25), fg="#FFFF00", bg="#051047").place(x=50, y=500)
        Label(text=f"YOUR SCORE IS {score}", font=('Se-geo UI', 25), fg="#FFFF00", bg="#051047").place(x=50, y=550)
        ret = tmsg.askquestion("quiz game", "DO YOU WANT TO PLAY AGAIN")
        if ret == 'yes':
            QUIZ_GAME()
        if ret == 'no':
            EXECUTION()


# TO ASK QUIZ TO THE USER

def quiz():
    root.title("QUIZ GAME")
    global element
    element = random.choice(list(elements.keys()))

    # DISPLAYING INFO FOR QUIZ IN LISTBOX

    game_listbox = Listbox(root, width=80, height=5, font="calibre 25", bg="lightblue")
    game_listbox.insert(END, f"Atomic Number: {elements[element]['Atomic Number']}")
    game_listbox.insert(END, f"Properties: {elements[element]['Properties']}")
    game_listbox.insert(END, f"Symbol: {elements[element]['Symbol']}")
    game_listbox.insert(END, f"Group: {elements[element]['Group']}")
    game_listbox.insert(END, f"Period: {elements[element]['Period']}")
    game_listbox.place(x=50, y=200)
    Label(text="ENTER THE ANSWER", font=('Se-geo UI', 25), fg="#FFFF00", bg="#051047").place(x=50, y=445)
    global ANS_VAR
    ANS_VAR = StringVar()
    Entry(textvariable=ANS_VAR, width=30, font=20).place(x=450, y=450)
    Button(text="CHECK", font="arial 11", command=guess_check).place(x=720, y=500)

    Button(root, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=750)


# FUNCTION CONTAINING DATA FOR THE QUIZ

def QUIZ_GAME():
    root.title("QUIZ GAME")
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    global score
    score = 0

    # CREATING NESTED DICTIONARY FOR QUIZ

    global elements

    elements = {
        "Hydrogen": {"Atomic Number": 1,
                     "Properties": "This element is the lightest and most abundant element in the universe.",
                     "Symbol": "H", "Group": 1, "Period": 1},
        "Helium": {"Atomic Number": 2,
                   "Properties": "This element is a colorless, odorless, tasteless gas.",
                   "Symbol": "He", "Group": 18, "Period": 1},
        "Lithium": {"Atomic Number": 3,
                    "Properties": "This element is a silvery-white metal that is highly reactive.",
                    "Symbol": "Li", "Group": 1, "Period": 2},
        "Beryllium": {"Atomic Number": 4,
                      "Properties": "This element is a highly reactive, silvery-white metal that is"
                                    " widely used in the production of steel.",
                      "Symbol": "Be", "Group": 2, "Period": 2},
        "Boron": {"Atomic Number": 5,
                  "Properties": "This element is a light, highly reactive metal"
                                " that is used in the production of aluminum.",
                  "Symbol": "B", "Group": 13, "Period": 2},
        "Carbon": {"Atomic Number": 6,
                   "Properties": "This element is a hard, crystalline, "
                                 "black solid that is used in the production of steel and other alloys.",
                   "Symbol": "C", "Group": 14, "Period": 2},
        "Nitrogen": {"Atomic Number": 7,
                     "Properties": "This element is a colorless, odorless, "
                                   "tasteless gas that is used in the production of fertilizers and explosives.",
                     "Symbol": "N", "Group": 15, "Period": 2},
        "Oxygen": {"Atomic Number": 8,
                   "Properties": "It is the third most abundant element in the universe,"
                                 " making up about 21% of the Earth's atmosphere.",
                   "Symbol": "O", "Group": 16, "Period": 2},
        "Fluorine": {"Atomic Number": 9,
                     "Properties": "This element is a pale yellow gas that is used "
                                   "in the production of neon lights and lasers.",
                     "Symbol": "F", "Group": 17, "Period": 2},
        "Neon": {"Atomic Number": 10,
                 "Properties": "is a chemical element that is a colorless, odorless, tasteless, and inert gas at room "
                               "temperature and standard pressure. It is the fifth most abundant element in the "
                               "universe",
                 "Symbol": "Ne", "Group": 18, "Period": 2},
        "Sodium": {"Atomic Number": 11,
                   "Properties": "This element is a silvery-white metal that is highly reactive"
                                 " and is used in the production of aluminum and sodium hydroxide.",
                   "Symbol": "Na", "Group": 1, "Period": 3},
        "Magnesium": {"Atomic Number": 12,
                      "Properties": "This element is a soft, silvery-white metal that is highly reactive"
                                    " and is used in the production of steel and other alloys.",
                      "Symbol": "Mg", "Group": 2, "Period": 3},
        "Aluminum": {"Atomic Number": 13,
                     "Properties": "This element is a soft, silvery-white metal that is highly reactive"
                                   " and is used in the production of steel and other alloys.",
                     "Symbol": "Al", "Group": 13, "Period": 3},
        "Silicon": {"Atomic Number": 14,
                    "Properties": "Exists as a solid at room temperature and pressure.Has a metallic luster."
                                  " It is very brittle. It is a semiconductor",
                    "Symbol": "Si", "Group": 14, "Period": 3},
        "Phosphorus": {"Atomic Number": 15,
                       "Properties": "This element that is a highly reactive, nonmetal at room temperature and "
                                     "standard pressure. "
                                     "It has several allotropic forms. It is an essential element for all known forms "
                                     "of life",
                       "Symbol": "P", "Group": 15, "Period": 3},
        "Sulfur": {"Atomic Number": 16,
                   "Properties": "This element isis a chemical element that is a yellow, brittle solid at room "
                                 "temperature "
                                 "and standard pressure. It is an abundant element that is found in a variety of "
                                 "minerals.",
                   "Symbol": "S", "Group": 16, "Period": 3},
        "Chlorine": {"Atomic Number": 17,
                     "Properties": "This element is a is a chemical element that is a highly reactive, pale green gas "
                                   "at "
                                   " room temperature and standard pressure. It is a halogen.",
                     "Symbol": "Cl", "Group": 17, "Period": 3},
        "Argon": {"Atomic Number": 18,
                  "Properties": "This element is a is a chemical element that is a colorless, odorless, tasteless,"
                                " and inert gas at room temperature and standard pressure. It is the third most"
                                "abundant element in the Earth's atmosphere, making up about 0.9% of the air by "
                                "volume.",
                  "Symbol": "Ar", "Group": 18, "Period": 3},
        "Potassium": {"Atomic Number": 19,
                      "Properties": "This element is a soft, silvery-white metal at room temperature and standard "
                                    "pressure. "
                                    " It is the seventh most abundant element in the Earth's crust",
                      "Symbol": "K", "Group": 1, "Period": 4},
        "Calcium": {"Atomic Number": 20,
                    "Properties": "This element is a soft, silvery-white metal that is highly reactive and "
                                  "is used in the production of steel and other alloys.",
                    "Symbol": "Ca", "Group": 2, "Period": 4},
        "Scandium": {"Atomic Number": 21,
                     "Properties": "This element is a hard, crystalline, black solid that is used in the "
                                   "production of steel and other alloys.",
                     "Symbol": "Sc", "Group": 3, "Period": 4},
        "Titanium": {"Atomic Number": 22,
                     "Properties": "This element is a highly reactive, pale yellow gas that is used in the "
                                   "production of plastics and detergents.",
                     "Symbol": "Ti", "Group": 4, "Period": 4},
        "Vanadium": {"Atomic Number": 23,
                     "Properties": "This element is a pale yellow gas that is used in the production of neon "
                                   "lights and lasers.",
                     "Symbol": "V", "Group": 5, "Period": 4},
        "Chromium": {"Atomic Number": 24,
                     "Properties": "This element is a pale yellow gas that is used in the production of "
                                   "semiconductors and LCD screens.",
                     "Symbol": "Cr", "Group": 6, "Period": 4},
        "Manganese": {"Atomic Number": 25,
                      "Properties": "This element is a hard, lustrous, silver-white metal that is used in the"
                                    " production of stainless steel ",
                      "Symbol": "Mn", "Group": 7, "Period": 4},
        "Iron": {"Atomic Number": 26,
                 "Properties": "This element is a soft, silvery-white metal that is highly reactive and is used"
                               " in the production of steel and other alloys.",
                 "Symbol": "Fe", "Group": 8, "Period": 4},
        "Cobalt": {"Atomic Number": 27,
                   "Properties": "This element is a hard, crystalline, black solid that is used in the production"
                                 " of steel and other alloys",
                   "Symbol": "Co", "Group": 9, "Period": 4},
        "Nickel": {"Atomic Number": 28,
                   "Properties": "This element is a highly reactive, pale yellow gas that is used in the "
                                 "production of plastics and detergents.",
                   "Symbol": "Ni", "Group": 10, "Period": 4},
        "Copper": {"Atomic Number": 29,
                   "Properties": "This element is a pale yellow gas that is used in the production of neon"
                                 " lights and lasers.",
                   "Symbol": "Cu", "Group": 11, "Period": 4},
        "Zinc": {"Atomic Number": 30,
                 "Properties": "This element is a pale yellow gas that is used in the production of "
                               "semiconductors and LCD screens.",
                 "Symbol": "Zn", "Group": 12, "Period": 4},
        "Gallium": {"Atomic Number": 31,
                    "Properties": "This element is a highly reactive, pale yellow gas that is used in the"
                                  " production of plastics and detergents.",
                    "Symbol": "Ga", "Group": 13, "Period": 4},
        "Germanium": {"Atomic Number": 32,
                      "Properties": "This element is a pale yellow gas that is used in the production of "
                                    "neon lights and lasers.",
                      "Symbol": "Ge", "Group": 14, "Period": 4},
        "Arsenic": {"Atomic Number": 33,
                    "Properties": "This element is a pale yellow gas that is used in the production of "
                                  "semiconductors and LCD screens.",
                    "Symbol": "As", "Group": 15, "Period": 4},
        "Selenium": {"Atomic Number": 34,
                     "Properties": "This element is a highly reactive, pale yellow gas that is used in the"
                                   " production of plastics and detergents.",
                     "Symbol": "Se", "Group": 16, "Period": 4},
        "Bromine": {"Atomic Number": 35,
                    "Properties": "This element is a pale yellow gas that is used in the production of neon"
                                  " lights and lasers.",
                    "Symbol": "Br", "Group": 17, "Period": 4},
        "Krypton": {"Atomic Number": 36,
                    "Properties": "This element is a pale yellow gas that is used in the production of "
                                  "semiconductors and LCD screens.",
                    "Symbol": "Kr", "Group": 18, "Period": 4},
        "Rubidium": {"Atomic Number": 37,
                     "Properties": "This element is a soft, silvery-white metal that is highly reactive."
                                   " It is used in lasers, atomic clocks, and pyrotechnics.",
                     "Symbol": "Rb", "Group": 1, "Period": 5},
        "Strontium": {"Atomic Number": 38,
                      "Properties": " This element is a soft, silvery-white metal that is highly reactive. "
                                    "It is used in fireworks, rat poison, and nuclear reactor control rods.",
                      "Symbol": "Sr", "Group": 2, "Period": 5},
        "Yttrium": {"Atomic Number": 39,
                    "Properties": "This element is a hard, crystalline, black solid that is used in the production "
                                  "of steel and other alloys.",
                    "Symbol": "Y", "Group": 3, "Period": 5},
        "Zirconium": {"Atomic Number": 40,
                      "Properties": "This element is a hard, silver-gray metal that is highly reactive. It "
                                    "is used in nuclear power plants, surgical implants, and abrasives.",
                      "Symbol": "Zr", "Group": 4, "Period": 5},
        "Niobium": {"Atomic Number": 41,
                    "Properties": "This element is a soft, gray, metallic element that is highly reactive."
                                  " It is used in superconductors, aircraft, and jewelry.",
                    "Symbol": "Nb", "Group": 5, "Period": 5},
        "Molybdenum": {"Atomic Number": 42,
                       "Properties": "This element is a hard, silver-gray metal that is highly reactive. "
                                     "It is used in steelmaking, electronics, and catalysts.",
                       "Symbol": "Mo", "Group": 6, "Period": 5},
        "Technetium": {"Atomic Number": 43,
                       "Properties": "This element is a silvery-gray, radioactive metal that is highly reactive. "
                                     "It is used in medicine and in oil refining.",
                       "Symbol": "Tc", "Group": 7, "Period": 5},
        "Ruthenium": {"Atomic Number": 44,
                      "Properties": "This element is a hard, silver-gray metal that is highly reactive. "
                                    "It is used in electrical contacts, pigments, and catalysts.",
                      "Symbol": "Ru", "Group": 8, "Period": 5},
        "Rhodium": {"Atomic Number": 45,
                    "Properties": "This element is a hard, silver-white metal that is highly reactive. "
                                  "It is used in catalysts, jewelry, and electrical contacts.",
                    "Symbol": "Rh", "Group": 9, "Period": 5},
        "Palladium": {"Atomic Number": 46,
                      "Properties": "This element is a soft, silver-white metal that is highly reactive. "
                                    "It is used in catalysts, jewelry, and dental fillings.",
                      "Symbol": "Pd", "Group": 10, "Period": 5},
        "Silver": {"Atomic Number": 47,
                   "Properties": "This element is a soft, white, metallic element that is highly reactive."
                                 " It is used in jewelry, coins, and electrical conductors.",
                   "Symbol": "Ag", "Group": 11, "Period": 5},
        "Cadmium": {"Atomic Number": 48,
                    "Properties": "This element is a soft, bluish-white metal that is highly toxic. "
                                  "It is used in batteries, pigments, and electroplating.",
                    "Symbol": "Cd", "Group": 12, "Period": 5},
        "Indium": {"Atomic Number": 49,
                   "Properties": "This element is a soft, silvery-white metal that is highly reactive."
                                 " It is used in electronics, dental fillings, and bearing alloys.",
                   "Symbol": "In", "Group": 13, "Period": 5},
        "Tin": {"Atomic Number": 50,
                "Properties": "This element is a soft, silvery-white metal that is highly reactive. "
                              "It is used in tin cans, soldering, and bronzes.",
                "Symbol": "Sn", "Group": 14, "Period": 5},
        "Antimony": {"Atomic Number": 51,
                     "Properties": "This element is a hard, bluish-white metalloid that is highly reactive. "
                                   "It is used in flame retardants, batteries, and cosmetics.",
                     "Symbol": "Sb", "Group": 15, "Period": 5},
        "Tellurium": {"Atomic Number": 52,
                      "Properties": "This element is a highly reactive, silver-white metalloid that is "
                                    "used in solar cells, catalysts, and steelmaking.",
                      "Symbol": "Te", "Group": 16, "Period": 5},
        "Iodine": {"Atomic Number": 53,
                   "Properties": "This element is a violet-black, metallic solid that is highly reactive. "
                                 "It is used in medicine, disinfectants, and photographic film.",
                   "Symbol": "I", "Group": 17, "Period": 5},
        "Xenon": {"Atomic Number": 54,
                  "Properties": "This element is a colorless, odorless gas that is used in fluorescent lights"
                                " and in medicine for anesthesia.",
                  "Symbol": "Xe", "Group": 18, "Period": 5},
        "Cesium": {"Atomic Number": 55,
                   "Properties": "This element is a soft, silvery-white metal that is highly reactive. "
                                 "It is used in atomic clocks, pyrotechnics, and vacuum tubes.",
                   "Symbol": "Cs", "Group": 1, "Period": 6},
        "Barium": {"Atomic Number": 56,
                   "Properties": "This element is a soft, silvery-white metal that is highly reactive. "
                                 "It is used in rat poison, fireworks, and oil drilling.",
                   "Symbol": "Ba", "Group": 2, "Period": 6},
        "Lanthanum": {"Atomic Number": 57,
                      "Properties": "This element is a soft, silvery-white metal that is highly reactive. "
                                    "It is used in catalysts, batteries, and fluorescent lights.",
                      "Symbol": "La", "Group": 3, "Period": 6},
        "Cerium": {"Atomic Number": 58,
                   "Properties": "This element is a malleable, soft, ductile, iron-grey metal, slightly harder"
                                 " than lead. It is used in catalysts, polishing, and lighter flints.",
                   "Symbol": "Ce", "Group": "Lanthanides", "Period": 6},
        "Praseodymium": {"Atomic Number": 59,
                         "Properties": "This element is a soft, silvery, lustrous, metallic, ductile metal."
                                       " It readily reacts with water to form hydroxides and air to form oxides.",
                         "Symbol": "Pr", "Group": "Lanthanides", "Period": 6},
        "Neodymium": {"Atomic Number": 60,
                      "Properties": "This element is a hard, silvery-white metal that is highly reactive. "
                                    "It is used in magnets, lasers, and alloys.",
                      "Symbol": "Nd", "Group": "Lanthanides", "Period": 6},
        "Promethium": {"Atomic Number": 61,
                       "Properties": "This element is used for research purpose. It can be used as beta radiation"
                                     " source in luminous paint, in nuclear batteries for guided missiles, watches,"
                                     " pacemakers and rados, and as a light source for signals.",
                       "Symbol": "Pm", "Group": "Lanthanides", "Period": 6},
        "Samarium": {"Atomic Number": 62,
                     "Properties": "This element is a hard, silvery-white metal that is highly reactive."
                                   " It is used in lasers, magnets, and catalysts.",
                     "Symbol": "Sm", "Group": "Lanthanides", "Period": 6},
        "Europium": {"Atomic Number": 63,
                     "Properties": "This element is a soft, silvery-white metal that is highly reactive. "
                                   "It is used in fluorescent lights, lasers, and catalysts.",
                     "Symbol": "Eu", "Group": "Lanthanides", "Period": 6},
        "Gadolinium": {"Atomic Number": 64,
                       "Properties": "This element is a soft, shiny, ductile, silvery metal. It reacts slowly "
                                     "with water and dissolves in acids and becomes superconductive below 1083 K.",
                       "Symbol": "Gd", "Group": "Lanthanides", "Period": 6},
        "Terbium": {"Atomic Number": 65,
                    "Properties": "This element is a soft, malleable, ductile, silver-gray metal. It is "
                                  "reasonably stable in air, but it is slowly oxidised and it reacts with cold water.",
                    "Symbol": "Tb", "Group": "Lanthanides", "Period": 6},
        "Dysprosium": {"Atomic Number": 66,
                       "Properties": "This element is a lustrous, very soft, silvery metal. It is stable in"
                                     " air at room temperature. It forms several brightly coloured salts.",
                       "Symbol": "Dy", "Group": "Lanthanides", "Period": 6},
        "Holmium": {"Atomic Number": 67,
                    "Properties": "This element is soft, malleable and ductile.  It has the highest magnetic "
                                  "moment of all elements present in nature.",
                    "Symbol": "Ho", "Group": "Lanthanides", "Period": 6},
        "Erbium": {"Atomic Number": 68,
                   "Properties": "This element is soft, malleable, lustrous, silvery metal. Its salts are rose"
                                 "coloured and it has a sharp adsorption spectra in visible, ultraviolet and infrared "
                                 "light.",
                   "Symbol": "Er", "Group": "Lanthanides", "Period": 6},
        "Thulium": {"Atomic Number": 69,
                    "Properties": "This element is a silvery metal that can be cut with a knife due it its"
                                  " soft texture. It is used in lasers, magnets, and alloys.",
                    "Symbol": "Tm", "Group": "Lanthanides", "Period": 6},
        "Ytterbium": {"Atomic Number": 70,
                      "Properties": "This element is soft, malleable and rather ductile element that exhibits"
                                    " a bright silvery luster. A rare earth, the element is easily attacked"
                                    " and dissolved by mineral acids, slowly reacts with water, and oxidizes in air.",
                      "Symbol": "Yb", "Group": "Lanthanides", "Period": 6},
        "Lutetium": {"Atomic Number": 71,
                     "Properties": "This element is silvery-white rare earth metal. It is harder and denser"
                                   " than all lanthanides. It exists in trivalent state in compounds.",
                     "Symbol": "Lu", "Group": "Lanthanides", "Period": 6},
        "Hafnium": {"Atomic Number": 72,
                    "Properties": "This element is a hard, silvery-white metal that is highly reactive. It "
                                  "is used in electronics, nuclear reactor control rods, and high-strength alloys.",
                    "Symbol": "Hf", "Group": 4, "Period": 6},
        "Tantalum": {"Atomic Number": 73,
                     "Properties": "This element is a dark (blue-gray), dense, ductile, very hard, easily"
                                   " fabricated, and highly conductive of heat and electricity. It is almost "
                                   "completely immune to attack by the normally aggressive aqua regia.",
                     "Symbol": "Ta", "Group": 5, "Period": 6},
        "Tungsten": {"Atomic Number": 74,
                     "Properties": "This element is and its alloys are used in many high-temperature applications,"
                                   " such as arc-welding electrodes and heating elements in high-temperature furnaces.",
                     "Symbol": "W", "Group": 6, "Period": 6},
        "Rhenium": {"Atomic Number": 75,
                    "Properties": "This element is silvery white and extremely hard. It resists wear and corrosion"
                                  " very well and has one of the highest melting points of the elements.",
                    "Symbol": "Re", "Group": 7, "Period": 6},
        "Osmium": {"Atomic Number": 76,
                   "Properties": "This element is a Osmium is a bluish-white and shiny metal. It is very hard and "
                                 "is brittle even at very high temperatures.It has the lowast vapor pressure and "
                                 "the highest melting point among the platinum group of metals.",
                   "Symbol": "Os", "Group": 8, "Period": 6},
        "Iridium": {"Atomic Number": 77,
                    "Properties": "This element is hard, brittle, lustrous, dense, transition metal of the platinum"
                                  " family. It is silvery-white and it is notable for being the most corrosion"
                                  " resistant element known. It is unaffected by air, water and acids.",
                    "Symbol": "Ir", "Group": 9, "Period": 6},
        "Platinum": {"Atomic Number": 78,
                     "Properties": "This element is a soft, white, metallic element that is one of the least "
                                   "reactive metals. It is used in jewelry, catalysts, and medical equipment.",
                     "Symbol": "Pt", "Group": 10, "Period": 6},
        "Gold": {"Atomic Number": 79,
                 "Properties": "This element is conducts heat and electricity. It is ductile and malleable. It can "
                               "be drawn out into the thinnest wire. It is highly reflective of heat and light",
                 "Symbol": "Au", "Group": 11, "Period": 6},
        "Mercury": {"Atomic Number": 80,
                    "Properties": "This element is a shiny, silver-white liquid that is highly toxic. It is used in"
                                  " thermometers, switches, and pesticides.",
                    "Symbol": "Hg", "Group": 12, "Period": 6},
        "Thallium": {"Atomic Number": 81,
                     "Properties": "This element is a soft, gray, metallic element that is highly toxic. It is used"
                                   " in rat poison, insecticides, and hair removal products.",
                     "Symbol": "Tl", "Group": 13, "Period": 6},
        "Lead": {"Atomic Number": 82,
                 "Properties": "This element is a bluish-white lustrous metal. It is very soft, highly malleable, "
                               "ductile, and a relatively poor conductor of electricity. It is very resistant to "
                               "corrosion but tarnishes upon exposure to air.",
                 "Symbol": "Pb", "Group": 14, "Period": 6},
        "Bismuth": {"Atomic Number": 83,
                    "Properties": "This element is a rather brittle metal with a somewhat pinkish, silvery metallic"
                                  " lustre. Bismuth is the most diamagnetic of all metals. It undergoes a 3.3 percent"
                                  " expansion when it solidifies from the molten state.",
                    "Symbol": "Bi", "Group": 15, "Period": 6},
        "Polonium": {"Atomic Number": 84,
                     "Properties": "This element is a radioactive, extremely rare semi-metal. It is reactive,"
                                   " silvery-gray, it dissolves in dilute acids, but it is only slightly soluble "
                                   "in alkalis.",
                     "Symbol": "Po", "Group": 16, "Period": 6},
        "Astatine": {"Atomic Number": 85,
                     "Properties": "This element is a highly radioactive element and it is the heaviest known halogen."
                                   " Its chemical properties are believed to be similar to those of iodine.",
                     "Symbol": "At", "Group": 17, "Period": 6},
        "Radon": {"Atomic Number": 86,
                  "Properties": "This element is a colorless at standard temperature and pressure and it is the "
                                "most dense gas known. At temperature below it's freezing point is has a brilliant "
                                "yellow phosphorescence. It is chemically unreactive, it is highly radioactive "
                                "and has a short half life.",
                  "Symbol": "Rn", "Group": 18, "Period": 6},

        "Francium": {"Atomic Number": 87,
                     "Properties": "This element is This element is a highly reactive, radioactive, metallic element"
                                   " that is found in very small amounts in the Earth's crust. It is used in research.",
                     "Symbol": "Fr", "Group": 1,
                     "Period": 7},
        "Radium": {"Atomic Number": 88,
                   "Properties": "This element is silvery, lustrous, soft, intensely radioactive. The heaviest "
                                 "member of the alkaline-earth group it is the most volatile.",
                   "Symbol": "Ra", "Group": 2,
                   "Period": 7},
        "Actinium": {"Atomic Number": 89,
                     "Properties": "This element is a soft, silvery-white radioactive metal. It is a very powerful"
                                   " source of alpha rays, but is rarely used outside research.",
                     "Symbol": "Ac", "Group": 3,
                     "Period": 7},
        "Thorium": {"Atomic Number": 90,
                    "Properties": "This element is a radioactive, silvery-white metal that is used in nuclear power"
                                  " plants and in the production of high-strength alloys.",
                    "Symbol": "Th", "Group": "Actinides",
                    "Period": 7},
        "Protactinium": {"Atomic Number": 91,
                         "Properties": "This element is a silver metallic element that belongs to the actinide group."
                                       " It is malleable, shiny, silver-gray, radioactive. It is superconductive at "
                                       "temperatures below 1.4 K.",
                         "Symbol": "Pa", "Group": "Actinides",
                         "Period": 7},
        "Uranium": {"Atomic Number": 92,
                    "Properties": "This element is a radioactive, heavy, metallic element that is used in nuclear"
                                  " power plants and in the production of nuclear weapons.",
                    "Symbol": "U", "Group": "Actinides",
                    "Period": 7},

        "Neptunium": {"Atomic Number": 93,
                      "Properties": "This element is a radioactive, metallic element that is produced artificially"
                                    "in nuclear reactors. It is used in research and in the production of nuclear "
                                    "weapons.",
                      "Symbol": "Np", "Group": "Actinides", "Period": 7},
        "Plutonium": {"Atomic Number": 94,
                      "Properties": "This element is a radioactive, metallic element that is produced artificially "
                                    "in nuclear reactors. It is used in nuclear power plants and in the production"
                                    " of nuclear weapons.",
                      "Symbol": "Pu", "Group": "Actinides", "Period": 7},
        "Americium": {"Atomic Number": 95,
                      "Properties": "This element is a silvery-white synthetic metal. It slowly tarnishes in"
                                    " dry air, but it is resistent to alkalis. It is denser than lead. ",
                      "Symbol": "Am", "Group": "Actinides", "Period": 7},
        "Curium": {"Atomic Number": 96,
                   "Properties": "This element is a hard, brittle, silvery radioactive metal that tarnishes slowly"
                                 " and which can only be produced in nuclear reactors.",
                   "Symbol": "Cm", "Group": "Actinides", "Period": 7},
        "Berkelium": {"Atomic Number": 97,
                      "Properties": "This element is It is silvery in colour and its chemistry has been investigated"
                                    " to a limited extent and several compounds have been made. Berkelim"
                                    " metal is attacked by oxygen, steam and acids, but not by alkalis.",
                      "Symbol": "Bk", "Group": "Actinides", "Period": 7},
        "Californium": {"Atomic Number": 98,
                        "Properties": "This element is a silvery-white actinide metal. The pure metal is malleable"
                                      " and is easily cut with a razor blade.",
                        "Symbol": "Cf", "Group": "Actinides", "Period": 7},
        "Einsteinium": {"Atomic Number": 99,
                        "Properties": "This element is a can be obtained in milligram quantities from the neutron "
                                      "bombardment of plutonium in a nuclear reactor.",
                        "Symbol": "Es", "Group": "Actinides", "Period": 7},
        "Fermium": {"Atomic Number": 100,
                    "Properties": "This element is a synthetic element. It is an actinide and the heaviest element"
                                  " that can be formed by neutron bombardment of lighter elements, and hence the "
                                  "last element that can be prepared in macroscopic quantities.",
                    "Symbol": "Fm", "Group": "Actinides", "Period": 7},
        "Mendelevium": {"Atomic Number": 101,
                        "Properties": "This element is a radioactive metal, of which only a few atoms have ever "
                                      "been created. It is used only for research. It has no known biological role.",
                        "Symbol": "Md", "Group": "Actinides", "Period": 7},
        "Nobelium": {"Atomic Number": 102,
                     "Properties": "This element is the penultimate actinide transuranic radioactive metal. The "
                                   "reactivity of nobelium is not known due to the limited amount that "
                                   "has been produced.",
                     "Symbol": "No", "Group": "Actinides", "Period": 7},
        "Lawrencium": {"Atomic Number": 103,
                       "Properties": "This element is purely used for scientific research only. Isotopes "
                                     "of this element are radioactive",
                       "Symbol": "Lr", "Group": "Actinides", "Period": 7},
        "Rutherfordium": {"Atomic Number": 104,
                          "Properties": "This element is It is a kind of trans-uranium and radioactive element"
                                        " which cannot be found in nature.It does not have any stable or naturally "
                                        "occurring isotopes.",
                          "Symbol": "Rf", "Group": 4, "Period": 7},
        "Dubnium": {"Atomic Number": 105,
                    "Properties": "This element is does not have any application and little is known about it."
                                  " It is not found free in the environment, it is a synthetic element.",
                    "Symbol": "Db", "Group": 5, "Period": 7},
        "Seaborgium": {"Atomic Number": 106,
                       "Properties": "This element is and its compounds are radioactive. Many experiments state"
                                     " that it behaves as the heavier homolog to Tungsten.",
                       "Symbol": "Sg", "Group": 6, "Period": 7},
        "Bohrium": {"Atomic Number": 107,
                    "Properties": "This element is an artificially produced radioactive element. It is probably"
                                  " silvery or metallic gray. It's most stable isotope, Bh-262 has an "
                                  "half life of 17 seconds.",
                    "Symbol": "Bh", "Group": 7, "Period": 7},
        "Hassium": {"Atomic Number": 108,
                    "Properties": "This element is a synthetic chemical element, expected to have chemical "
                                  "properties similar to those of osmium and a silvery white or metallic gray colour.",
                    "Symbol": "Hs", "Group": 8, "Period": 7},
        "Meitnerium": {"Atomic Number": 109,
                       "Properties": "This element is a synthetic, radioactive metallic element that was first"
                                     " produced in 1982. It is a highly reactive element that decays quickly"
                                     " into other elements.",
                       "Symbol": "Mt", "Group": 9, "Period": 7},
        "Darmstadtium": {"Atomic Number": 110,
                         "Properties": "This element has no known biological role. A man-made element of which"
                                       " only a few atoms have ever been created. It that is formed by fusing "
                                       "nickel and lead atoms in a heavy ion accelerator.",
                         "Symbol": "Ds", "Group": 10, "Period": 7},
        "Roentgenium": {"Atomic Number": 111,
                        "Properties": "This element is only used in research. It has no known biological role."
                                      " A man-made element of which only a few atoms have ever been created. "
                                      "It is made by fusing nickel and bismuth atoms in a heavy ion accelerator.",
                        "Symbol": "Rg", "Group": 11, "Period": 7},
        "Copernicium": {"Atomic Number": 112,
                        "Properties": "This element, since only a few atoms of it have ever been produced, "
                                      "it currently has no uses outside of basic scientific research.",
                        "Symbol": "Cn", "Group": 12, "Period": 7},
        "Nihonium": {"Atomic Number": 113,
                     "Properties": "This element classified as a post-transition metal, It is a expected to be a"
                                   " solid at room temperature.",
                     "Symbol": "Nh", "Group": 13, "Period": 7},
        "Flerovium": {"Atomic Number": 114,
                      "Properties": "This element is a synthetic, radioactive metallic element that was first "
                                    "produced in 1998. It is produced artificially in nuclear reactors through"
                                    " the bombardment of plutonium with ions of calcium.",
                      "Symbol": "Fl", "Group": 14, "Period": 7},
        "Moscovium": {"Atomic Number": 115,
                      "Properties": "This element is a radioactive, synthetic element about which little is known."
                                    " It is classified as a metal and is expected to be solid at room temperature."
                                    " It decays quickly into other elements, including nihonium.",
                      "Symbol": "Mc", "Group": 15, "Period": 7},
        "Livermorium": {"Atomic Number": 116,
                        "Properties": "This element has no commercial uses. Rather, this element has been used"
                                      " in research, yielding valuable insights into the behavior of superheavy atoms.",
                        "Symbol": "Lv", "Group": 16, "Period": 7},
        "Tennessine": {"Atomic Number": 117,
                       "Properties": "Scientists are investigating the properties of this element and using it to"
                                     " produce atoms of other elements through its decay scheme. "
                                     "There is no known or expected biological role of element 117.",
                       "Symbol": "Ts", "Group": 17, "Period": 7},
        "Oganesson": {"Atomic Number": 118,
                      "Properties": "It is a synthetic, radioactive metallic element that was first produced in 2002."
                                    " Due to its highly reactive nature and short half-life, it has no"
                                    " known practical uses. It is a highly reactive element that decays quickly"
                                    " into other elements. ",
                      "Symbol": "Og", "Group": 18, "Period": 7},

    }

    quiz()


# FUNCTION EXTRACTING INFORMATION FROM TEXT FILE OF ELEMENTS OF PERIODIC TABLE

def txtfile(k):
    print(k)
    root.title("info")
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    f = open("Periodictable.txt", "r", encoding="utf8")
    f.seek(0)

    ALL_COLUMNS = ['Atomic Number : ', 'Symbol : ', 'Element : ', 'Origin of name : ',
                   'Group : ', 'Period : ', 'Atomic weight : ', 'Density (g/cm^3): ',
                   'Melting point (K) : ', 'Boiling point (K): ',
                   'Specific heat capacity (J/g . K): ', 'Electronegativity : ',
                   'Abundance in earth\'s crust (mg/kg): ']

    # CREATING LISTBOX FOR DISPLAYING INFORMATION OF ELEMENTS

    info_listbox = Listbox(root, width=80, height=13, font="calibri 25", bg="lightblue")

    index = 0
    for line in f:
        data = line.split('*')
        if str(k) == data[0].strip():
            for i in data:
                info_listbox.insert(END, f"{ALL_COLUMNS[index]} {i}")
                index += 1
            break
    f.close()
    info_listbox.place(x=80, y=200)

    Button(text="BACK", font="arial 11", bg="LIGHTBLUE", command=INFO_ELEMENTS).place(x=1300, y=750)


# FUNCTON PASSING ARGUMENTS  TO ABOVE ONE FOR DISPLAYING INFORMATION OF ELEMENTS

def INFO_ELEMENTS():
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    Label(rectangle_doc, text="f-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=200,
                                                                                                            y=445)
    Label(rectangle_doc, text="p-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=950, y=20)
    Label(rectangle_doc, text="d-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=600,
                                                                                                            y=100)
    Label(rectangle_doc, text="s-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=100,
                                                                                                            y=200)

    # USING A LOOP TO DISPLAY BUTTONS AND PASSING ATOMIC NUMBER AS ARGUMENTS

    elements = ['H', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']

    d = 100
    e = 1
    c = 0
    for i in range(7):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='orange',
               command=partial(txtfile, e)).place(x=d + 200, y=c + 100)
        if e == 1:
            e += 2
        elif e == 3 or e == 11:
            e += 8
        elif e == 19 or e == 37:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']
    e = 4
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='yellow',
               command=partial(txtfile, e)).place(x=d + 250, y=c + 100)
        if e == 4 or e == 12:
            e += 8
        elif e == 20 or e == 38:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Sc', 'Y', 'Lu', 'Lr']
    e = 21
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 300, y=c + 100)
        if e == 21 or e == 39:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Ti', 'Zr', 'Hf', 'Rf']
    e = 22
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 350, y=c + 100)
        if (e == 22):
            e += 18
        else:
            e += 32
        c += 43

    elements = ['V', 'Nb', 'Ta', 'Db']
    e = 23
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 400, y=c + 100)
        if (e == 23):
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Cr', 'Mo', 'W', 'Sg']
    e = 24
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 450, y=c + 100)
        if e == 24:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Mn', 'Tc', 'Re', 'Bh']
    e = 25
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 500, y=c + 100)
        if e == 25:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Fe', 'Ru', 'Os', 'Hs']
    e = 26
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 550, y=c + 100)
        if e == 26:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Co', 'Rh', 'Ir', 'Mt']
    e = 27
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 600, y=c + 100)
        if e == 27:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Ni', 'Pd', 'Pt', 'Ds']
    e = 28
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 650, y=c + 100)
        if e == 28:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Cu', 'Ag', 'Au', 'Rg']
    e = 29
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 700, y=c + 100)
        if e == 29:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Zn', 'Cd', 'Hg', 'Cn']
    e = 30
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 750, y=c + 100)
        if e == 30:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['B', 'Al', 'Ga', 'In', 'Tl', 'Nh']
    e = 5
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 800, y=c + 100)
        if e == 5:
            e += 8
        elif e == 13 or e == 31:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['C', 'Si', 'Ge', 'Sn', 'Pb', 'Fl']
    e = 6
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 850, y=c + 100)
        if e == 6:
            e += 8
        elif e == 14 or e == 32:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['N', 'P', 'As', 'Sb', 'Bi', 'Mc']
    e = 7
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 900, y=c + 100)
        if e == 7:
            e += 8
        elif e == 15 or e == 33:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['O', 'S', 'Se', 'Te', 'Po', 'Lv']
    e = 8
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 950, y=c + 100)
        if e == 8:
            e += 8
        elif e == 16 or e == 34:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['F', 'Cl', 'Br', 'I', 'At', 'Ts']
    e = 9
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightgreen', command=partial(txtfile, e)).place(x=d + 1000, y=c + 100)
        if e == 9:
            e += 8
        elif e == 17 or e == 35:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']
    e = 2
    c = 0
    for i in range(7):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='grey',
               command=partial(txtfile, e)).place(
            x=d + 1050, y=c + 100)
        if e == 2 or e == 10:
            e += 8
        elif e == 18 or e == 36:
            e += 18
        else:
            e += 32
        c += 43

    c = 0
    elements = ['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    for i in range(14):
        e = 58 + i
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='pink',
               command=partial(txtfile, e)).place(x=c + 400, y=450)
        c += 50

    c = 0
    elements = ['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']
    for i in range(14):
        e = 90 + i
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='lightblue',
               command=partial(txtfile, e)).place(x=c + 400, y=493)
        c += 50

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# FUNCTION TO PRESENT PERIODIC TABLE

def PERIODICTABLE():

    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    rectangle_doc.create_rectangle(0, 0, 2500, 2500)
    rectangle_doc.create_line(0, 2, 5000, 2)
    Label(rectangle_doc, text='''ELEMENTS OF PERIODIC TABLE ARE''', font=" comicsansms 20 bold ", fg="#FFFF00"
          , bg="#4169E1", borderwidth=3, relief=RIDGE).place(x=10, y=10)
    Label(rectangle_doc, text='''     COULMNS
                                       
                                    1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
                                    
                       R       1     H                                                  He
                       O       2     Li Be                               B  C  N  O  F  Ne
                       W       3     Na Mg                               Al Si P  S  Cl Ar
                       S       4     K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
                               5     Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe
                               6     Cs Ba La Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
                               7     Fr Ra Ac Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og

                     LANTHANIDES              Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
                     ACTINIDES                Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr''',
          font="Courier 20 bold roman",
          fg="#FAF9F6",
          bg="#051047").place(x=-250, y=50)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# FUNCTION EXECUTED AFTER LOGIN BUTTON IS PRESSED

def EXECUTION():

    Canvas(root, bg="#FFFFF0", height=300, width=1900).place(x=0, y=0)
    Label(text="PERIODIC TABLE", font="arial 40 bold", bg="#FFFFF0").place(x=500, y=70)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    rectangle_doc.create_rectangle(0, 0, 2500, 2500)
    rectangle_doc.create_line(0, 2, 5000, 2)

    # DISPLAYING BUTTONS FOR DIFFERENT FUNCTIONS

    Button(rectangle_doc, text="PERIODIC TABLE", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=PERIODICTABLE).place(x=350, y=190)
    Button(rectangle_doc, text="ELEMENTAL GALLERY", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=PICTURES).place(x=350,
                                   y=390)
    Button(rectangle_doc, text="ELEMENTAL INFORMATION", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=INFO_ELEMENTS).place(x=350, y=90)
    Button(rectangle_doc, text="PERIODIC QUIZ", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=QUIZ_GAME).place(x=350, y=290)
    Button(rectangle_doc, text="PLAY YOUR PART", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=USER_INFO).place(x=350, y=490)
    Button(root, text="LOGOUT", font="arial 11", bg="LIGHTBLUE", command=BACK_TO_MAIN).place(x=0, y=185)


# FUNCTION WILL VERIFY THAT USERNAME AND PASSWORD ENTER BY USER IS CORRECT OR NOT

def STUDENT_VERIFY():
    flag = 0
    if str(pre_CMS_var.get()).isnumeric() and len(str(pre_CMS_var.get().strip())) == 11:
        j = open('students_account.txt', 'r')
        j.seek(0)
        while 1:
            data = j.readline()
            data1 = data.split('*')
            if pre_CMS_var.get().strip() == data1[0] and pre_pass_var.get().strip() == data1[1].strip('\n'):
                flag = 1
                break
            if not data:
                tmsg.showinfo("Login", "Account not found!")
                break
        j.close()
        if flag == 1:
            EXECUTION()
        return
    else:
        tmsg.showinfo("Login", "Invalid entries!")
        return


# FUNCTION FOR CREATING STUDENTS NEW ACCOUNT TO ACCESS PERIODIC TABLE

def CREATE_ACCOUNT():
    signal = 1

    # CHECKING WHETHER ACCOUNT ALREADY EXIST OR NOT

    if str(new_CMS_var.get()).isnumeric() and len(str(new_CMS_var.get())) == 11:
        c = open('students_account.txt', 'r')
        c.seek(0)
        while 1:
            data = c.readline()
            data1 = data.split('*')
            if new_CMS_var.get().strip() in data1:
                tmsg.showinfo("Account", "Account already exists!")
                signal = 0
                c.close()
                break
            if not data:
                break

    if signal == 0:
        return
    if str(new_CMS_var.get()).isnumeric() and len(str(new_CMS_var.get())) == 11:
        b = open('students_account.txt', 'a')
        student_acc_list = []
        temp1 = new_CMS_var.get() + '*'
        student_acc_list.append(temp1)
        temp2 = new_pass_var.get()
        student_acc_list.append(temp2)
        b.writelines(student_acc_list)
        b.write('\n')
        b.close()
        tmsg.showinfo("Account", "ACCOUNT CREATED SUCCESSFULLY!")
        new_CMS_var.set("")
        new_pass_var.set('')
        return
    else:
        tmsg.showinfo("Error", "CMS ID IS INVALID!")
        return


# WE HAVE TO CREATE THIS FUNCTION FOR LOGOUT PURPOSE

def main():
    global new_CMS_var, new_pass_var, pre_CMS_var, pre_pass_var

    Canvas(root, bg="#FFFFF0", height=300, width=1900).place(x=0, y=0)

    Label(root, text=" MTH ", font=('Segue UI', 44), fg="#FFFF00", bg="#051047").place(x=300, y=45)
    Label(root, text="PERIODIC TABLE ", font=('Segue UI', 34), bg='#FFFFF0').place(x=500, y=50)

    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    Label(rectangle_doc, text="CMS ID:", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=100)
    Label(rectangle_doc, text="Password:", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=150)

    # ALREADY PRESENT ACCOUNT

    pre_CMS_var = StringVar()
    pre_pass_var = StringVar()

    Entry(rectangle_doc, textvariable=pre_CMS_var, width=30, font=20).place(x=550, y=110)
    Entry(rectangle_doc, textvariable=pre_pass_var, width=30, font=20, show='*').place(x=550, y=160)
    Button(rectangle_doc, text="Log in", font="arial 11", relief=GROOVE, command=STUDENT_VERIFY).place(x=830, y=200)
    Label(rectangle_doc, text="STUDENT LOGIN", font=('Segoe UI', 30), fg="#FFFF00", bg="#051047").place(x=550, y=20)

    # NEW ACCOUNT FOR STUDENT

    line = Canvas(rectangle_doc, width=1900, height=5, bg='#4169E1')
    line.place(x=0, y=250)
    line.create_line(0, 10, 2500, 10, fill='#4169E1')
    Label(rectangle_doc, text="PLEASE CREATE ACCOUNT TO ACCESS PERIODIC TABLE", font=('Segue UI', 30), fg="#FFFF00",
          bg="#051047").place(x=250,
                              y=300)
    Label(rectangle_doc, text="CMS ID:", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=400)
    Label(rectangle_doc, text="Password:", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=450)

    new_CMS_var = StringVar()
    new_pass_var = StringVar()

    Entry(rectangle_doc, textvariable=new_CMS_var, width=30, font=20).place(x=550, y=405)
    Entry(rectangle_doc, textvariable=new_pass_var, width=30, font=20, show='*').place(x=550, y=455)
    Button(rectangle_doc, text="Create", font="arial 11", relief=GROOVE, command=CREATE_ACCOUNT).place(x=830, y=500)


# FUNCTON FOR TKINTER

def func():

    # TKINTER MAIN WINDOW

    global root
    root = Tk()
    root.geometry("1500x1000")
    root.title("PERIODIC TABLE")
    main()
    root.mainloop()


# OUR MAIN

func()
