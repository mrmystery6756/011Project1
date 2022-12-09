import sys
import time
import os
import urllib.request, urllib.error, urllib.parse
from netmiko import ConnectHandler
#above is where i've imported all of the libraries i am using in the project


def choose():
	choice = input("""
	*************************************************
	*	please select an option(1-5 or Q)	*
	*	1. Show date and time			*
	*	2. Show IP address			*
	*	3. Show remote home directory listing	*
	*	4. Backup remote file			*
	*	5. Save web page			*
	*	Q. quit					*
	*************************************************
	""")
	choice = str(choice.upper()) #makes sure that the character is uppercase
	return choice
#The choose function allows the user to input what option they want

def Date():
	print("The current date and time is:")
	os.system("date")
#the date function prints the date and time of the local computer

def IP():
	print("The IP address of this machine is:")
	os.system("hostname -I")
#The IP function shows the local IP of the system

def List_Dir():
	try:
		net_connect = ConnectHandler( #ConnectHandler makes the connection between the local PC and the remote PC
			device_type="linux",
			host="127.0.0.1",
			port="5679",
			username=input("please enter your username: "),
			password=input("please enter your password: "),
		)
	except:
		print("something went wrong, please make sure these are the correct details for this enviroment.")
		choose() #looping back to choose so the user doesn't get stuck
	print("The home directory on this enviroment is: ")
	output = net_connect.send_command("ls ~")
	print(output)
	#os.system("ls ~") #used for testing ls ~

def Backup():
	try:
		pathing = input("Please specify the full path to the file: ")
		pathing = pathing[::-1] #reverses the path
		filename = ""
		count_slash = 0
		for char in pathing:
			if char == "/":
				count_slash+=1 #counts how many slashes they are to determine how far back to the root the program needs to go
		for char in pathing:
			if  char != "/":
				filename = filename + char #this determines the filename
			else:
				break
		filename = filename[::-1]
		pathing = pathing[::-1]
		length_name = len(filename)
		length_pathing = len(pathing)
		new_pathing = ""
		for i in range(length_pathing-length_name):
			new_pathing += pathing[i]
			print(pathing[i])
		#the above for loop gets the path without the filename
		for i in range(count_slash):
			os.chdir("..")
		#this for loop changes the directory to the root
		os.chdir(str(new_pathing)) #this goes to the new path
		os.system("ls")
		os.system("cp "+filename+" "+filename+".old") #copies the file with the .old suffix
		os.system("ls")
	except:
		print("something went wrong, please make sure you have entered the correct full path for the file and that the file exists.")
		choose()
def Save_Page():
	url = input("what is the URL you would like to save :")
	try:
		global open_url #makes sure it can be used outside of the try and except
		open_url = urllib.request.urlopen(url)
	except ValueError:
		print("URL format unrecognisable")
	try:
		url_content = open_url.read().decode("UTF-8") #trying to turn the code into HTML
		with open(str(url)+"Backupfile.txt","w") as file: #opening the file
			file.write(url_content)
			file.close()
	except:	#this catches any errors that may be wrong with the code
		print("something went wrong")

def Quit():
	choice = input("are you sure you want to quit? Y/N:")
	choice = choice.upper()
	if choice == "Y": #makes sure the user wants to quit
		pass
	elif choice == "N":
		main()
	else:
		print("please input either Y or N")
		time.sleep(1)
		Quit()
	print("quitting in")
	print("3")
	time.sleep(0.5)
	print("2")
	time.sleep(0.5)
	print("1")
	time.sleep(0.5)
	sys.exit("quitting")
	#the time.sleep allows the program to look better

def redirect(choice):
	options1 = ("1","2","3","4","5","Q")
	options2 = (Date, IP, List_Dir, Backup, Save_Page, Quit) #names of tthe functions without the brackets
	count = 0
	if choice not in options1:
		while choice not in options1:
			print("please choose either 1,2,3,4,5 or Q")
			choose() #this error catches ay wrong inputs made in the choose() function
	for option in options1:
		if choice == option:
			return options2[count] #iterates over the first list to find the name of the function
		else:
			count += 1


def main():
	choice = choose()
	option = redirect(choice)
	option()
	main()
	#the main function makes sure that everything runs in order

main()

