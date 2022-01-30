##############Initialisation################

from tkinter import *
import random,sqlite3,os
LoggedIn=False

##############Account Functions################

#Login window
def login():

    #function called to log in to account
    def submit():
        #makes ID global so it is accesible from anywhere in the program
        global ID
        #stores user inputs as variables
        ID=entry1.get()
        password=entry2.get()
        #gets password from database
        c.execute("SELECT Password from Students where Login_ID = ?", (ID,))
        Password = str(c.fetchone())
        #changes password to standard format for comparison with user input
        Password = Password.replace("(", "").replace(",", "").replace(")","").replace("'", "")
        #validation of password
        if password == Password:
            op.destroy()
            window.config(menu=menubar2)
            global LoggedIn
            LoggedIn=True
            
    #creates login window
    op = Toplevel()
    op.geometry('240x150')
    op.resizable(False,False)
    op.configure(bg='light gray')
    #defines features on login window
    label1 = Label(op, font =("Arial", 20), text ="Login ID",bg='light gray')
    label1.grid(row=0,column=0,padx=10)
    entry1= Entry(op, width=20, bg='white')
    entry1.grid(row=1,column=0,sticky=E)
    label2 = Label(op, font =("Arial", 20), text ="Password",bg='light gray')
    label2.grid(row=2,column=0)
    entry2= Entry(op, width=20, bg='white',show="*")
    entry2.grid(row=3,column=0,sticky=E)
    button1 = Button(op, font=("Tahoma",10),text='Submit',pady=10,command=submit,fg="white",bg="#383a39")
    button1.grid(row=1,column=1,rowspan=2,pady=20,padx=30)


#changes the program to a logged out state
def logout():
    window.config(menu=menubar)
    global LoggedIn
    LoggedIn=False
    
#create account window    
def createacc():
    
    #function called to create the account
    def genacc():
        global ID
        #storing user inputs as variables
        ID=entry3.get()
        Password=entry4.get()
        Fname=entry1.get()
        Sname=entry2.get()
        #validating length of user inputs
        if len(Password)<4:
            labeldis2.configure(text='Make password longer')
        elif len(ID)<1:
            labeldis.configure(text='Make login longer')
        else:
            #creates account in database
            try:
                c.execute('''INSERT INTO Students(Login_ID, Password, Students_firstname, Students_surname)
                                VALUES(?,?,?,?)''', (ID,Password,Fname,Sname) )
                c.execute('''INSERT INTO Progress(Login_ID, Prev1,Prev2,Prev3,Overall_Score,Overall_Attempts)
                                VALUES(?,?,?,?,?,?)''', (ID,0,0,0,0,0) )
                ent.destroy()
                db.commit()
                #changes the program to a logged in state
                window.config(menu=menubar2)
                global LoggedIn
                LoggedIn=True
            #error exception for when the ID is not unique    
            except:
                labeldis.configure(text='ID already exists')
                        
    #creates 'Create account' window       
    ent=Toplevel()
    ent.resizable(False,False)
    #defines features on create account window
    label1=Label(ent, font =("Arial",18), text ="First Name:")
    label1.grid(column=0,row=0,padx=10,pady=10)
    label2=Label(ent,font =("Arial",18), text ="Last Name:")
    label2.grid(column=1,row=0,padx=10,pady=10)
    entry1=Entry(ent)
    entry1.grid(row=1,column=0)
    entry2=Entry(ent)
    entry2.grid(row=1,column=1,pady=10)
    label3=Label(ent, font =("Arial",18), text ="Login ID:")
    label3.grid(column=0,row=2,pady=10)
    entry3=Entry(ent)
    entry3.grid(column=0,row=3,padx=10,pady=10)
    labeldis=Label(ent,font =("Arial",12), text ="",fg="red")
    labeldis.grid(column=1,row=2,rowspan=2)
    label4=Label(ent, font =("Arial",18), text ="Password:")
    label4.grid(column=0,row=4,pady=10)
    entry4=Entry(ent)
    entry4.grid(column=0,row=5,pady=10)
    labeldis2=Label(ent,font =("Arial",12), text ="",fg="red")
    labeldis2.grid(column=1,row=4,rowspan=2)
    button1=Button(ent,font =("Arial",18), text ="Create",command=genacc)
    button1.grid(column=0,columnspan=2,row=6)
        
        
#Progress window
def progdis():
    #creates Progress window
    prog = Toplevel()
    prog.resizable(False,False)
    prog.title('Progress')
    #gets student name from database
    c.execute("SELECT Students_firstname, Students_surname from Students where Login_ID = ?", (ID,))
    names=c.fetchone()
    #defines some features on Progress window
    labeltext1=str(names[0])+' '+str(names[1])+"'s Progress"
    l11=Label(prog,font=("Tahoma",20),text = labeltext1)
    l11.grid(column=0,row=0,padx=20,pady=20,columnspan=3)
    l01=Label(prog,font=("Tahoma",20),text = "Last Three Scores:")
    l01.grid(column=0,row=1,padx=20,pady=20)
    #gets progress data from database
    c.execute("SELECT Prev1, Prev2, Prev3, Overall_Score, Overall_Attempts from Progress where Login_ID = ?", (ID,))
    Row = c.fetchone()
    #calculates average score
    if Row[4]==0:
        dinom=1
    else:
        dinom=Row[4]
    avscore=int(int(Row[3])/int(dinom))
    #defines features on Progress window
    avscoredis=str(avscore)+' / 18'
    totalscoredis=str(Row[3])+' / '+str(int(Row[4])*18)
    l11=Label(prog,font=("Tahoma",20),text = Row[0])
    l11.grid(column=0,row=2,padx=20,pady=20)
    l12=Label(prog,font=("Tahoma",20),text = Row[1])
    l12.grid(column=0,row=3,padx=20,pady=20)
    l13=Label(prog,font=("Tahoma",20),text = Row[2])
    l13.grid(column=0,row=4,padx=20,pady=20)
    l21=Label(prog,font=("Tahoma",20),text = "Total Score:")
    l21.grid(column=2,row=1,padx=20,pady=20)
    l22=Label(prog,font=("Tahoma",20),text = totalscoredis)
    l22.grid(column=2,row=2,padx=20,pady=20)
    l23=Label(prog,font=("Tahoma",20),text = "Total Attempts:")
    l23.grid(column=2,row=3,padx=20,pady=20)
    l24=Label(prog,font=("Tahoma",20),text = Row[4])
    l24.grid(column=2,row=4,padx=20,pady=20)
    l31=Label(prog,font=("Tahoma",20),text = "Average Score:")
    l31.grid(column=1,row=1,padx=20,pady=20)
    l32=Label(prog,font=("Tahoma",20),text = avscoredis)
    l32.grid(column=1,row=2,padx=20,pady=20)
    
##############Learn Window################
    
#Learn window    
def learn(sub):
    #creates Learn window
    lp= Toplevel()
    lp.title("Learn Algorithms and Examples")
    lp.resizable(False,False)
    
    #displays images when topic button clicked
    def bubbleDisplay():
        l1.configure(text="Bubble Sort")        
        display.configure(image = img1)
    def shuttleDisplay():
        l1.configure(text="Shuttle Sort")
        display.configure(image = img2)
    def shellDisplay():
        l1.configure(text="Shell Sort")
        display.configure(image = img3)
    def quickDisplay():
        l1.configure(text="Quick Sort")
        display.configure(image = img4)

    #defines features on Learn window    
    #buttons and label for sort type
    b1 = Button(lp,text = "Bubble Sort",font = ("Comic Sans MS", 16),command=bubbleDisplay)
    b1.grid(column=0,row=1,padx=10,pady=20)
    b2 = Button(lp,text = "Shuttle Sort",font = ("Comic Sans MS", 16),command=shuttleDisplay)
    b2.grid(column=0,row=2,padx=10,pady=20)
    b3 = Button(lp,text = "Shell Sort",font = ("Comic Sans MS", 16),command=shellDisplay)
    b3.grid(column=0,row=3,padx=10,pady=20)
    b4 = Button(lp,text = "Quick Sort",font = ("Comic Sans MS", 16),command=quickDisplay)
    b4.grid(column=0,row=4,padx=10,pady=20)
    l1 = Label(lp,font=("Tahoma",20),text = "Bubble Sort")
    l1.grid(column=1,row=0,padx=10)
    #defines images
    img1 = PhotoImage(file="bub.png")
    img2 = PhotoImage(file="shu.png")
    img3 = PhotoImage(file="she.png")
    img4 = PhotoImage(file="qui.png")
    #defines image label
    display= Label(lp,image=img1)
    display.grid(column=1,row=1,rowspan=4,padx=10)
    
    #redefines everything in Learn window for Graphs topics
    if sub==2:
        #displays images when topic button clicked
        def graphDisplay():
            l1.configure(text="Graphs")        
            display.configure(image = img5)
        def kruskalDisplay():
            l1.configure(text="Kruskal's - Minimum Spanning Tree")
            display.configure(image = img6)
        def primsDisplay():
            l1.configure(text="Prims' - Minimum Spanning Tree")
            display.configure(image = img7)
        def dijkstraDisplay():
            l1.configure(text="Dijkstra's - Shortest Path")
            display.configure(image = img8)
        #defines features on Learn window     
        b1.configure(text="Graphs",command=graphDisplay)
        b2.configure(text="Kruskal's",command=kruskalDisplay)
        b3.configure(text="Prims'",command=primsDisplay)
        b4.configure(text="Dijkstra's",command=dijkstraDisplay)
        l1.configure(text="Graphs")
        img5= PhotoImage(file="gra.png")
        img6= PhotoImage(file="kru.png")
        img7= PhotoImage(file="pri.png")
        img8= PhotoImage(file="dij.png")
        display.configure(image=img5)

##############Sorting Algorithms################        

#Generates random List for sorting algorithm question
def gen(Length,sort):
    Numbers = []    
    while len(Numbers) < Length:
        No = False
        Num = random.randrange(0,25)
        for Past in Numbers:
            if Num == Past:
                No = True
        if No == False:
            Numbers.append(Num)
    #calls next function in the sorting algorithm question process
    PC3(Numbers,sort)

#Bubbles Sort algorithm
def bubble(Numbers,display2,passdis,compdis,swapdis,prime):
        #Initialises algorithm
        title="Bubble Sort"
        L= len(Numbers)
        Comparisons = 0
        Swaps = 0
        passnum=1
        #algorithm
        #carries out one pass of bubble sort every iteration (changes the numbers list)
        while True:
            Swapped = 0
            Compared = 0
            #iterates through every number in list and compares with the number infront then swaps if necessary
            for n in range(0,L-1):
                Compared += 1
                if Numbers[n] > Numbers[n+1]:
                    Numbers.insert(n+1,Numbers.pop(n))
                    Swapped += 1
            #updates display strings and answer variables at end of pass
            for num in Numbers:
                display2+=str(num)+" "
            Comparisons += Compared
            passdis+=str(passnum) + "\n"
            compdis+=str(Compared) + "\n"
            swapdis+=str(Swapped) + "\n"
            Swaps += Swapped
            if Swapped ==0 or Compared==1:
                break
            L -=1
            display2+= "\n"
            passnum+=1    
        #defines display strings at end of algorithm
        comptext='Total='+str(Comparisons)
        swaptext='Total='+str(Swaps)
        #returns answer display strings and title string for Sorting Algorithm Question window
        return display2,passdis,compdis,swapdis,comptext,swaptext,title

#Shuttle Sort Algorithm
def shuttle(Numbers,display2,passdis,compdis,swapdis,prime):
    #Initialises algorithm
    if prime:
        title="Shuttle Sort"
    L= len(Numbers)
    Comparisons = 0
    Swaps = 0
    passnum=0
    #Algorithm
    #carries out one pass of shuttle sort every iteration (changes the numbers list)
    for n in range(0,L-1):
        Swapped=0
        Compared=0
        #iterates until number being compared is in correct position for current pass
        while True:
            #no numbers left to compares so updates display strings and answer variables at end of pass
            if n<0:
                if prime:
                    for num in Numbers:
                        display2+=str(num)+" "
                    passnum+=1
                    display2+= "\n" 
                Comparisons += Compared
                passdis+=str(passnum) + "\n"
                compdis+=str(Compared) + "\n"
                swapdis+=str(Swapped) + "\n"
                Swaps += Swapped
                break
            #Compares number with number in front in list
            else:
                Compared += 1
                if Numbers[n] > Numbers[n+1]:
                    Numbers.insert(n+1,Numbers.pop(n))
                    Swapped += 1
                    n-=1
                #no swaps on this pass signifies end of pass so updates display strings and answer variables at end of pass
                else:
                    if prime:
                        for num in Numbers:
                            display2+=str(num)+" "
                        passnum+=1
                        display2+= "\n" 
                    Comparisons += Compared
                    passdis+=str(passnum) + "\n"
                    compdis+=str(Compared) + "\n"
                    swapdis+=str(Swapped) + "\n"
                    Swaps += Swapped
                    break            
    #returns answer display strings and title string for Sorting Algorithm Question window
    if prime:
        comptext='Total='+str(Comparisons)
        swaptext='Total='+str(Swaps)
        return display2,passdis,compdis,swapdis,comptext,swaptext,title
    #if function is used part way through shuttle sort returns these values
    else:
        return Numbers,Comparisons,Swaps

#Shell Sort Algorithm
def shell(Numbers,display2,passdis,compdis,swapdis,prime):
    #Initialises algorithm
    title="Shell Sort"
    passnum=0
    L= len(Numbers)
    #uses 2D array for sublists
    lists = []
    numoflists= L
    Comparisons = 0
    Swaps = 0
    passnum=1
    passdis,swapdis,compdis='\n','\n','\n'
    #Algorithm
    #carries out one pass of shell sort every iteration (changes the numbers list)
    while True:
        #stores end of the first line in a pass as a string variable for adding to display later and for having the number of lists needed to use during this pass of the algorithm 
        oldnum=numoflists
        numoflists= int(numoflists/2)
        intdis=' INT('+str(oldnum)+'/2) ='+str(numoflists)
        #add first line of pass to display string
        for num in Numbers:
            if len(str(num))==1:
                display2+=' '
            display2+=str(num)+" "
        display2+= intdis
        display2+= "\n"
        #carries out final pass when 1 sublist is needed for pass
        if numoflists == 1:
            Numbers,Compared,Swapped=shuttle(Numbers,"","","","",False)
            Comparisons +=Compared
            passdis+=str(passnum) + "\n"
            compdis+=str(Compared) + "\n"
            swapdis+=str(Swapped) + "\n"
            Swaps+=Swapped
            for num in Numbers:
                if len(str(num))==1:
                    display2+=' '
                display2+=str(num)+" "
            display2+= "            \n"
            comptext='Total='+str(Comparisons)
            swaptext='Total='+str(Swaps)
            return display2,passdis,compdis,swapdis,comptext,swaptext,title
            break
        #carries out rest of any pass other than the final pass (using multiple sublists)
        else:
            #creates required number of sublists
            for x in range(0,numoflists):
                d=x
                lists.append([])
                #splits current list of numbers up into the sublists
                while True:
                    lists[d].append(Numbers[x])
                    x += numoflists
                    if x > L-1:
                        break
            #spaces out the characters on each line in the display string so the numbers appear displayed in a grid form for the correct way to set out the answer
            gap=' '
            for n in range(0,numoflists-1):
                gap+='   '
            for x in lists:
                passdis+='\n'
                swapdis+='\n'
                compdis+='\n'
                lineadd=''
                for n in range(0,lists.index(x)):
                    lineadd+="   "
                for num in x:
                    if len(str(num))==1:
                        lineadd+=' '
                    if x.index(num)!=0:
                        lineadd+=gap+str(num)
                    else:
                        lineadd+=str(num)
                #makes all display string lines same length                    
                while len(lineadd)<12+(L*3):
                    lineadd+=' '
                display2+=lineadd+'\n'  
            Compared=0
            Swapped=0
            #uses shuttle sort on each sublist to put them in the right order and get number of comparisons and swaps used on each sublists
            for y in range(0,numoflists):
                lists[y],Comp,Swap=shuttle(lists[y],"","","","",False)
                #adds comparisons and swaps for sublist to total comparisons and swaps in pass
                Compared+=Comp
                Swapped+=Swap
            Comparisons +=Compared
            passdis+=str(passnum) + "\n"
            compdis+=str(Compared) + "\n"
            swapdis+=str(Swapped) + "\n"
            Swaps+=Swapped
            b = 0
            #puts together the sublists in the right order
            Numbers=[]
            for a in range(0,L):
                c = a - b*numoflists
                Numbers.append(lists[c][b])
                if c == numoflists-1:
                    b += 1
            passnum+=1
        #resets 2D array for next pass
        lists = []

#Quick Sort Algorithm
def quick(Nums,display2,passdis,compdis,swapdis,prime):
    #Initialises algorithm
    title="Quick Sort"
    Numbers=[]
    passnum=0
    for x in Nums:
        Numbers.append([x,0])
    #Algorithm
        
    #performs one single pass, called when sort algorithm incomplete
    def OnePass(display2,passnum,passdis):
        #Initialises pass
        TempNumbers=[]
        NewNumbers=[]
        TempAnswerLine=[]
        for x in Numbers:
            #adds current number in list to TempNumbers to be pivoted about a chosen pivot as it is neither a pivot or a used pivot
            if x[1] ==0:
                TempNumbers.append(x)
                #chooses pivot for next pass
                if len(TempNumbers)==1:
                    TempNumbers[0][1]=1
            #makes temporary list for all numbers that needed to be moved about pivot
            else:
                #adds current numbers to display line of the previous pass before new pass is performed
                TempAnswerLine+=TempNumbers
                #marks old pivots as used pivots
                x[1]=2
                #adds used pivots to answer display
                TempAnswerLine.append(x)
                #when numbers need moving about pivot
                if len(TempNumbers)!=0:
                    lower=[]
                    higher=[]
                    pivot=TempNumbers.pop(0)
                    #sorts numbers into higher and lower than pivot lists
                    for num in TempNumbers:                        
                        if num[0]<pivot[0]:
                            lower.append(num)
                        else:
                            higher.append(num)
                    #Combines lower list pivot and higher list into one list
                    NewNumbers+=lower
                    NewNumbers.append(pivot)
                    NewNumbers+=higher
                    #resets array for next pass
                    TempNumbers=[]
                NewNumbers.append(x)
        #(sorts all elements in TempNumbers about a pivot) like the code above but putting this into a procedure was ineffective because of all the variables that would need to be passed back and forth as well as the code would need modifying to allow for the changes
        if len(TempNumbers) != 0:
            TempAnswerLine+=TempNumbers
            lower=[]
            higher=[]
            pivot=TempNumbers.pop(0)
            for num in TempNumbers:
                if num[0]<pivot[0]:
                    lower.append(num)
                else:
                    higher.append(num)
            NewNumbers+=lower
            NewNumbers.append(pivot)
            NewNumbers+=higher
            TempNumbers=[]
        #gives pivots and used pivot brackets and square braket respectively for the display string
        for num in TempAnswerLine:
            if num[1] == 0:
                display2+=str(num[0])+" "
            if num[1] == 1:
                display2+=('('+str(num[0])+') ')
            if num[1] == 2:
                display2+=('['+str(num[0])+'] ')
        #updates display strings and answer variables at end of pass
        display2+="\n"
        passnum+=1
        passdis+=str(passnum) + "\n"
        return NewNumbers,display2,passnum,passdis
    
    #carries out one pass of quick sort every iteration (changes the numbers list)
    while True:
        #checks if any numbers are not yet boxed off (if the algorithm is incomplete)
        stop=True
        for num in Numbers:
            if num[1] != 2:
                stop= False
        #calls the function to carry out another pass
        if not stop:
            Numbers,display2,passnum,passdis=OnePass(display2,passnum,passdis)
        #returns answer display strings and title string for Sorting Algorithm Question window    
        else:
            comptext,swaptext='N/A','N/A'
            return display2,passdis,compdis,swapdis,comptext,swaptext,title

##############Sorting Algorithm Functions################
        
#Sort Algorithm Question window
def PC3(Numbers,sort):
    #makes window global so it can be changed or closed from another function during a topic test
    global pc3
    #creates Sort Algorithm Question window
    pc3=Toplevel()
    pc3.title("Practice")
    pc3.configure(bg='light grey')
    #defines feature on the Sort Algorithm Question window
    #defines labels that display original list of numbers before it is sorted
    display1=""
    for num in Numbers:
        display1+=str(num)+" "
    label7 = Label(pc3,font=("Tahoma",18),text = display1,bg='light grey')
    label7.grid(column=2,row=3,pady=10)
    label8 = Label(pc3,font=("Tahoma",18),text = display1,bg='light grey')
    label8.grid(column=1,row=3)
    #function called to get answer display strings and title string
    display2,passdis,compdis,swapdis,comptext,swaptext,title = sort(Numbers,"","","","",True)
    print(display2)
    #defines features on the Sort Algorithm Question window
    label1 = Label(pc3,font=("Tahoma",24),text = title,bg='light grey')
    label1.grid(column=0,row=1,columnspan=5)
    label3 = Label(pc3,font=("Tahoma",18),text = "Correct Answer",bg='light grey')
    label3.grid(column=2,row=2,padx=20,pady=10)
    label4 = Label(pc3,font=("Tahoma",18),text = "Your Answer",bg='light grey')
    label4.grid(column=1,row=2,padx=20,pady=10)
    label5 = Label(pc3,font=("Tahoma",18),text = "Pass",bg='light grey')
    label5.grid(column=0,row=2,padx=20,pady=10)
    label9 = Label(pc3,font=("Tahoma",18),text = "Comparisons",bg='light grey')
    label9.grid(column=3,row=2,padx=20,pady=10)
    label10 = Label(pc3,font=("Tahoma",18),text = "Swaps",bg='light grey')
    label10.grid(column=4,row=2,padx=20,pady=10)
    #text box for user input
    entry1= Text(pc3, width=35, bg='white',font=("Consolas",18))
    entry1.grid(row=4,column=1,pady=10)
    #defining more labels
    label2 = Label(pc3,font=("Consolas",18),text = display2,bg='light grey',fg='light grey')
    label2.grid(column=2,row=4,sticky=N,pady=9)
    label6 = Label(pc3,font=("Tahoma",18),text = passdis,bg='light grey',fg='light grey')
    label6.grid(column=0,row=4,sticky=N,pady=9)
    label11 = Label(pc3,font=("Tahoma",18),text = compdis,bg='light grey',fg='light grey')
    label11.grid(column=3,row=4,sticky=N,pady=9)
    label12 = Label(pc3,font=("Tahoma",18),text = swapdis,bg='light grey',fg='light grey')
    label12.grid(column=4,row=4,sticky=N,pady=9)
    label13 = Label(pc3,font=("Tahoma",16),text = comptext,bg='light grey',fg='light grey')
    label13.grid(column=3,row=5)
    label14 = Label(pc3,font=("Tahoma",16),text = swaptext,bg='light grey',fg='light grey')
    label14.grid(column=4,row=5)

    #makes answers visible when Show Answer button clicked
    def showAnswer(): 
        label2.configure(fg='black')
        label6.configure(fg='black')
        label11.configure(fg='black')
        label12.configure(fg='black')
        label13.configure(fg='black')
        label14.configure(fg='black')
        #redefines show answer button to hide answer button 
        button1.configure(text="Hide Answer",command=hideAnswer)

    #makes answers invisible when Hide Answer button clicked
    def hideAnswer():
        label2.configure(fg='light grey')
        label6.configure(fg='light grey')
        label11.configure(fg='light grey')
        label12.configure(fg='light grey')
        label13.configure(fg='light grey')
        label14.configure(fg='light grey')
        #redefines hide answer button to show answer button 
        button1.configure(text="Show Answer",command=showAnswer)
        
    #displays correct answer when Confirm Answer button clicked
    def confirm():
        showAnswer()
        button1.destroy()
        #calls next function in test process
        MarkSort(display2,entry1.get("1.0","end-1c"),True,0,False)

    #defines show answer button 
    button1 = Button(pc3,text = "Show Answer",font = ("Tahoma", 16),command=showAnswer)
    button1.grid(column=1,row=1)
    #redefines show answer button to confirm answer button
    if TestType == 'testSort':
        button1.configure(text="Confirm Answer",command=confirm)

    #displays correct answer when Confirm Answer button clicked
    def confirm2(Answer,UserAnswer):
        FinalMark=0
        if Answer == UserAnswer:
            FinalMark=TestQMark
        showAnswer()
        button1.destroy()
        MarkSort('','',False,FinalMark,False)

    #changes text box input to spin box input     
    if TestType == 'testSimple':
        entry1.destroy()
        v=IntVar()
        entry1 = Spinbox(pc3,textvariable=v,from_=0, to = 100)
        entry1.grid(row=4,column=1,pady=10)
        #creates question from two possibilities
        Options=[['Swaps',swaptext,swapdis],['Comparisons',comptext,compdis]]       
        Chosen=Options[random.randrange(0,1)]
        #define questions and answers
        if TestQMark==2:
            simplequestion='How many '+ str(Chosen[0])+' were used?'
            SimpleAnswer = int(Chosen[1][-1:])
        if TestQMark==1:            
            passeslist=makelist(passdis.replace('\n',' '),True)
            numofpass=len(passeslist)
            Pass=random.randrange(1,numofpass+1)
            listofchosen=makelist(Chosen[2].replace('\n',' '),True)
            SimpleAnswer=listofchosen[Pass-1]
            simplequestion='How many '+str(Chosen[0])+' were used on pass '+str(Pass)+'?'
        #defines Sorting Algorithms Question window features
        label8.configure(text=simplequestion)
        label2.configure(fg='black')
        label3.configure(text='Sorting Solution')
        label6.configure(fg='black')
        button1.configure(text="Confirm Answer",command=lambda:confirm2(v.get(),SimpleAnswer))
        
#sets default marks for question 0 and makes variable global
TestQMark=0

#Sorting Algorithms Question Features window    
def praca():
    #updates Test type to default for doing practice questions
    global TestType
    TestType='none'
    #creates Sorting Algorithms Question Features window 
    pc1= Toplevel()
    pc1.title("Questions Features")
    pc1.resizable(False,False)
    pc1.configure(bg="light gray")
    #defines features on Sorting Algorithms Question Features window 
    v=IntVar()
    spin1 = Spinbox(pc1,textvariable=v,from_=4, to = 12)
    spin1.grid(row=2,column=1,rowspan=2,padx=10)
    label1 = Label(pc1,font=("Tahoma",18),text = "Length",bg="light gray")
    label1.grid(column=1,row=1,pady=10,sticky=S)
    label2 = Label(pc1,font=("Tahoma",18),text = "Type",bg="light gray")
    label2.grid(column=2,row=1)
    label3 = Label(pc1,font=("Tahoma",8),text = "OR input your own list:",bg="light gray")
    label3.grid(column=1,row=4,padx=10)
    b1 = Button(pc1,text = "Bubble Sort",font = ("Tahoma", 16),command=lambda:gen(v.get(),bubble))
    b1.grid(column=2,row=2,padx=10,pady=10)
    b2 = Button(pc1,text = "Shuttle Sort",font = ("Tahoma", 16),command=lambda:gen(v.get(),shuttle))
    b2.grid(column=2,row=3,padx=10,pady=10)
    b3 = Button(pc1,text = " Shell Sort  ",font = ("Tahoma", 16),command=lambda:gen(v.get(),shell))
    b3.grid(column=2,row=4,padx=10,pady=10)
    b4 = Button(pc1,text = " Quick Sort ",font = ("Tahoma", 16),command=lambda:gen(v.get(),quick))
    b4.grid(column=2,row=5,padx=20,pady=10)
    b6 = Button(pc1,text="Custom",font = ("Tahoma",16),command=custompc)
    b6.grid(column=1,row=4,rowspan=2)
   
#Custom Sorting Algorithm Question window    
def custompc():

    #Opens Question window with custom question chosen and closes Custom Sorting Algorithm Question window   
    def r5():        
        PC3(makelist(entry1.get(),True),bubble)
        cust.destroy()
    def r6():
        PC3(makelist(entry1.get(),True),shuttle)
        cust.destroy()
    def r7():
        PC3(makelist(entry1.get(),True),shell)
        cust.destroy()
    def r8():
        PC3(makelist(entry1.get(),True),quick)
        cust.destroy()        

    #creates Custom Sorting Algorithm Question window 
    cust=Toplevel()#
    cust.title('Custom Question')
    #defines features on Custom Sorting Algorithm Question window 
    entry1= Entry(cust, width=20, bg='white')
    entry1.grid(row=3,column=1,pady=1)
    b1 = Button(cust,text = "Bubble Sort",font = ("Tahoma", 16),command=r5)
    b1.grid(column=2,row=2,padx=10,pady=10)
    b2 = Button(cust,text = "Shuttle Sort",font = ("Tahoma", 16),command=r6)
    b2.grid(column=2,row=3,padx=10,pady=10)
    b3 = Button(cust,text = " Shell Sort  ",font = ("Tahoma", 16),command=r7)
    b3.grid(column=2,row=4,padx=10,pady=10)
    b4 = Button(cust,text = " Quick Sort ",font = ("Tahoma", 16),command=r8)
    b4.grid(column=2,row=5,padx=20,pady=10)
    
#splits a string up into elements of an array
def makelist(text,num):
    #removes any spaces at start of text string
    while True:
        if text[:1]==' ':
            text=text[1:]
        else:
            break
    #makes list called Numbers from string
    Numbers= []
    tempnum=''
    for x in text:
        if x == ' ':
            if prevx != ' ' and tempnum!='':
                if num:
                    Numbers.append(int(tempnum))
                else:
                    Numbers.append(tempnum)
                tempnum=''
        else:
            tempnum+=x
        prevx=x
    if tempnum!='':
        if num:
            Numbers.append(int(tempnum))
        else:
            Numbers.append(tempnum)
    return Numbers

##############Graphs Functions################

#Graphs Question Feature window
def pracg():
    #updates Test type to default for doing practice questions
    global TestType
    TestType='none'
    #creates Graphs Question Feature window
    pc11= Toplevel()
    pc11.title("Questions Features")
    pc11.resizable(False,False)
    pc11.configure(bg="light gray")
    #defines features on Graphs Question Feature window
    label2 = Label(pc11,font=("Tahoma",18),text = "Type",bg="light gray")
    label2.grid(column=1,row=1)
    b1 = Button(pc11,text = "Kruskal's Algorithm",font = ("Tahoma", 16),command=lambda:genPath("Kruskal's"))
    b1.grid(column=1,row=2,padx=10,pady=10)
    b2 = Button(pc11,text = "  Prims' Algorithm ",font = ("Tahoma", 16),command=lambda:genPath("Prims'"))
    b2.grid(column=1,row=3,padx=10,pady=10)

#chooses a random graphs topic for test question
def genPath(Algo):
    if TestType=='testGraph':
        Graphchoice=Graphs.pop(random.randrange(0,len(Graphs)))
    else:
        Graphchoice=Graphs[random.randrange(0,len(Graphs))]  
    if Algo== "Kruskal's":
        PC10([1],Algo,Graphchoice[0],Graphchoice[1],Graphchoice[3])
    if Algo=="Prims'":
        PC10([1],Algo,Graphchoice[0],Graphchoice[2],'')
        
#Graphs Question window    
def PC10(Shortest,Algo,GraphImage,display2,start):
    global pc10
    #creates Graphs Question window  
    pc10=Toplevel()
    pc10.title("Graphs")
    pc10.resizable(False,False)
    pc10.configure(bg='light grey')
    #defines features on Graphs Question window
    #defines title and question labels
    title=str(Algo)+' Algorithm'
    label1 = Label(pc10,font=("Tahoma",24),text = title,bg='light grey')
    label1.grid(column=1,row=1,columnspan=2)
    questiontext='Use '+str(Algo)+' algorithm to find the minimum spanning tree'
    if Algo=="Kruskal's":
        questiontext+=' starting at node '+start
    label99= Label(pc10,font=("Tahoma",12),text = questiontext,bg='light grey')
    label99.grid(columnspan=5,row=0,column=0)
    #defines labels
    label3 = Label(pc10,font=("Tahoma",18),text = "Correct Answer",bg='light grey')
    label3.grid(column=2,row=2,padx=20,pady=10)
    label4 = Label(pc10,font=("Tahoma",18),text = "Your Answer",bg='light grey')
    label4.grid(column=1,row=2,padx=20,pady=10)
    label5 = Label(pc10,font=("Tahoma",18),text = "Graph",bg='light grey')
    label5.grid(column=0,row=2,padx=20,pady=10)
    #defines entry box
    entry1= Text(pc10, width=10, bg='white',font=("Consolas",18))
    entry1.grid(row=4,column=1,pady=10)
    #defines image label and image
    img1 = PhotoImage(file=GraphImage)
    displayg = Label(pc10,image=img1)
    displayg.image = img1
    displayg.grid(column=0,row=4,sticky=N,pady=9)
    #defines label
    label2 = Label(pc10,font=("Consolas",18),text=display2,bg='light grey',fg='light grey')
    label2.grid(column=2,row=4,sticky=N,pady=9)

    #makes answers visible when Show Answer button clicked
    def showAnswer(): 
        label2.configure(fg='black')
        #redefines show answer button to hide answer button 
        button1.configure(text="Hide Answer",command=hideAnswer)
        
    #makes answers invisible when Hide Answer button clicked
    def hideAnswer():
        label2.configure(fg='light grey')
        #redefines hide answer button to show answer button 
        button1.configure(text="Show Answer",command=showAnswer)

    #displays correct answer when Confirm answer button clicked   
    def confirm():
        showAnswer()
        button1.destroy()
        #calls next function in test process
        MarkSort(display2,entry1.get("1.0","end-1c"),True,0,True)
    #defines Show Answer button    
    button1 = Button(pc10,text = "Show Answer",font = ("Tahoma", 16),command=showAnswer)
    button1.grid(column=0,row=1)
    #redefines show answer button to confirm answer button
    if TestType=='testGraph':
        button1.configure(text='Confirm Answer',command=confirm)

##############Test functions################
        
#stores algorithms/algorithm functions for chosing from when generating test questions
Algos=["Kruskal's","Prims'"]
Types=[bubble,shuttle,shell,quick]

#
def test(sub):
    #resets test settings
    TestReset()
    #picks next question in test
    global NextQuestion
    if sub == 3:
        change=random.randrange(0,2)
        NextQuestion=[NextQuestion.pop(change+3),NextQuestion.pop(change),QuestionG,QuestionG]   
    if sub==2:
        NextQuestion=[QuestionG,QuestionG,QuestionG]
    NextQuestion.pop(random.randrange(0,len(NextQuestion)))()
        
    
def EndOfTest():
    TestRes=Toplevel()
    def endTest():
        TestRes.destroy()
        TestReset()
    display='Final Score: '+str(TotalMarked)+' / 18'
    label=Label(TestRes,text=display)
    label.grid(column=0,row=0,padx=10,pady=10)
    button=Button(TestRes,text='Okay',command=endTest)
    button.grid(column=0,row=1,padx=10,pady=10)
    if LoggedIn:
        updateProgress(TotalMarked)

#Defines question features(topic, list length) and starts the test process by calling gen function
#sorting algorithm-total swaps or comps or passes
def Question1():
    global TestType
    TestType='testSimple'
    global TestQMark
    TestQMark=2
    gen(random.randrange(4,8),Types[random.randrange(0,3)])
#Normal sorting algorithm - 5 marker 
def Question2():
    global TestType
    TestType='testSort'
    global TestQMark
    TestQMark=5
    gen(random.randrange(6,8),Types[random.randrange(0,4)])
#Normal sorting algorithm - 6 marker 
def Question3():
    global TestType
    TestType='testSort'
    global TestQMark
    TestQMark=6
    gen(random.randrange(8,10),Types[random.randrange(2,4)])
#Normal sorting algorithm - 4 marker 
def Question4():
    global TestType
    TestType='testSort'
    global TestQMark
    TestQMark=4
    gen(random.randrange(4,6),Types[random.randrange(0,2)])
#Sorting Algorithm - num of comps or swaps in one pass
def Question5():
    global TestType
    TestType='testSimple'
    global TestQMark
    TestQMark=1
    gen(random.randrange(4,8),Types[random.randrange(0,3)])
#Normal Graphs
def QuestionG():
    global TestType
    TestType='testGraph'
    global TestQMark
    TestQMark=6
    genPath(Algos[random.randrange(0,2)])

#Marks test questions when called by previous test question function in test process
def MarkSort(Answer,UserAnswer,Algo,mark,Graph):

    #starts next question in test or ends test when next button clicked
    def Next():
        #closes current question windows
        if Graph:
            pc10.destroy()
        else:
            pc3.destroy()
        PopUp.destroy()
        #ends test if no more question left to do
        if len(NextQuestion)>0:            
            NextQuestion.pop(random.randrange(0,len(NextQuestion)))()
        else:
            EndOfTest()
    #marks sorting algorithm answers        
    if Algo:
        #gets user answer and correct answer in same format for comparison
        Answer= Answer.replace("\n"," ")
        List1=makelist(Answer,False)
        UserAnswer=UserAnswer.replace('\n',' ')
        List2=makelist(UserAnswer,False)
        count=0
        correct=0
        if len(List2)> len(List1):
            LIST= List1
            LIST2=List2
        else:
            LIST= List2
            LIST2=List1
        #compares answers and marks line by line    
        for num in LIST:
            if Graph:
                if num.upper() == LIST2[count].upper() or num.upper() == (LIST2[count][1:]+LIST2[count][:1]).upper():
                    correct+=1
                count+=1
            else:  
                if num == LIST2[count]:
                    correct+=1
                count+=1
        #calculates mark out of total possible marks
        mark=int((correct/(len(List1)))*TestQMark)
    #adds mark from current question to total test mark
    global TotalMarked
    TotalMarked+=mark
    #creates question score window
    PopUp= Toplevel()
    #defines features on question score window
    textforpop= 'You Scored '+str(mark)+' / '+str(TestQMark)+' Marks for this question.'
    label=Label(PopUp,text=textforpop)
    label.grid(column=0,row=0,padx=10,pady=10)
    button=Button(PopUp,text='Next >',command=Next)
    button.grid(column=0,row=1,padx=10,pady=10)

#Resets global test settings variables to their default    
def TestReset():
    global NextQuestion
    NextQuestion=[Question1,Question2,Question3,Question4,Question5]    
    global TestType
    TestType='none'
    global TotalMarked
    TotalMarked=0
    global Graphs
    #pre defined graphs questions and answers (element indexes for each 1D array:0=graph image 1=kruskal answer 2=prims answer 3=kruskal start node)
    Graphs=[["g0.png",'AB\nBC\nBE\nED\nEF\nEH\nHI\nHG','AB\nHI\nDE\nBC\nHG\nBE\nEF\nEH','A'],["g1.png",'BC\nBD\nBE\nEA','BC\nBD\nAE\nEB','B'],["g2.png",'EC\nBC\nAB\nAD','BC\nEC\nAB\nAD','E'],["g3.png",'FI\nIH\nHG\nGJ','HG\nHI\nFI\nGJ','F'],["g4.png",'AE\nED\nDF\nDC\nBC','DF\nDC\nCB\nDE\nAE','A']]

#sets test settings to default    
TestReset()        
    
##############Database################

#create/open database 
if not os.path.isfile("new_db.db"):
    db = sqlite3.connect("new_db.db")
    c=db.cursor()
    c.execute(''' CREATE TABLE Students
    (Login_ID TEXT PRIMARY KEY,
    Password TEXT,
    Students_firstname TEXT,
    Students_surname TEXT
    )''')
    c.execute(''' CREATE TABLE Progress
    (Login_ID TEXT,
    Prev1 INTEGER,
    Prev2 INTEGER,
    Prev3 INTEGER,
    Overall_Score INTEGER,
    Overall_Attempts INTEGER,
    FOREIGN KEY(Login_ID) REFERENCES Students(Login_ID)
    )''')
    db.commit()
db = sqlite3.connect("new_db.db")
c=db.cursor()

#updates progress data in database
def updateProgress(LastScore):
    #gets previous progress data
    c.execute("SELECT Prev1, Prev2, Prev3, Overall_Score, Overall_Attempts  FROM Progress WHERE Login_ID = ?",(ID,))
    row = c.fetchone()
    #changes data to match current progress (addition of a new test score)
    newOverallScore= row[3] + LastScore
    newOverallAttempts= row[4] + 1
    #updates progress data in database
    c.execute("UPDATE Progress SET Prev1 = ?, Prev2 = ?, Prev3 = ?, Overall_Score = ?, Overall_Attempts = ? WHERE Login_ID = ? ",(LastScore,row[0],row[1],newOverallScore,newOverallAttempts,ID))
    db.commit()

##############Main Menu################

#exits program    
def Exit():
    db.commit()
    db.close()
    window.destroy()
    
#creates Main Menu window
window = Tk()
window.title("Descision 1")
window.configure(bg='#1FAAEE')
window.geometry('690x280')
window.resizable(False,False)
menubar = Menu(window)
#defines logged out menu
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label='Login',command=login)
menu1.add_command(label='Create Account',command=createacc)
menu1.add_command(label='Exit',command=Exit)
menubar.add_cascade(label='Profile',menu=menu1)
#defines logged in menu
menubar2 = Menu(window)
menu2 = Menu(menubar2,tearoff=0)
menu2.add_command(label='Logout',command=logout)
menu2.add_command(label='Progress',command=progdis)
menu2.add_command(label='Exit',command=Exit)
menubar2.add_cascade(label='Profile',menu=menu2)
#defining main menu window features
#menubar
window.config(menu=menubar)    
#title label
label1 = Label(window, font=("Papyrus", 32), text = "Decision 1 Mathematics Tool", fg='black',bg='#1FAAEE',padx=20,pady=25)
label1.grid(column = 1, row = 0,columnspan=4)    
#Sorting algorithms buttons and label
label2 = Label(window, font=("Tahoma",20),text = "Sorting Algorithms",fg='black',bg='#1FAAEE',padx=15,pady=15)
label2.grid(column = 0, row = 1, sticky=W,columnspan=2)
button1 = Button(window, font = ("Comic Sans MS", 16), text = "Learn",command=lambda:learn(1))
button1.grid(column = 2, row = 1)
button2 = Button(window, font = ("Comic Sans MS", 16), text = "Practice",command=praca)
button2.grid(column = 3, row = 1)
button3 = Button(window, font = ("Comic Sans MS", 16), text = "Test",command=lambda:test(1))
button3.grid(column = 4, row = 1)
#Graphs buttons and label
label3 = Label(window, font=("Tahoma",20),text = "Graphs",fg='black',bg='#1FAAEE',pady=15,padx=15)
label3.grid(column = 0, row = 2, sticky=W,columnspan=2)
button4 = Button(window, font = ("Comic Sans MS", 16), text = "Learn",command=lambda:learn(2))
button4.grid(column = 2, row = 2)
button5 = Button(window, font = ("Comic Sans MS", 16), text = "Practice",command=pracg)
button5.grid(column = 3, row = 2)
button6 = Button(window, font = ("Comic Sans MS", 16), text = "Test",command=lambda:test(2))
button6.grid(column = 4, row = 2)
#test button for both
button7 = Button(window, font = ("Comic Sans MS", 18), text = "Test",command=lambda:test(3))
button7.grid(column = 5, row=1,rowspan=2)

