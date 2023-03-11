from tkinter import *
import customtkinter
import openai
import os
import pickle

# Initiate APP
root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico')

# Set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Submit to ChatGPT
def speak():
	if chat_entry.get():
		filename="api_key"

		try:
			if os.path.isfile(filename):
				input_file=open(filename, 'rb')
				dummy=pickle.load(input_file)
				# Define api key to ChatGPT
				openai.api_key=dummy
				#Create an instance
				openai.Model.list()
				#Define our query
				response=openai.Completion.create(
					model="text-davinci-003",
					prompt=chat_entry.get(),
					temperature=0,
					max_tokens=60,
					top_p=1.0,
					frequency_penalty=0.0,
					presence_penalty=0.0,
					)

				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")

			else:
				input_file=open(filename, 'wb')
				input_file.close()
				my_text.insert(END, "\n\nYou need an API key to talk with ChatGPT. Get one here:\nhttps://beta.openai.com/account/api_keys")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")
	else:
		my_text.insert(END, "\n\nHey You Forgot to type Anything!")

# Clear the screens
def clear():
	my_text.delete(1.0, END)
	chat_entry.delete(0, END)

# For API
def key():
	filename="api_key"

	try:
		if os.path.isfile(filename):
			input_file=open(filename, 'rb')
			dummy=pickle.load(input_file)
			api_entry.insert(END, dummy)
		else:
			input_file=open(filename, 'wb')
			input_file.close()

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

	root.geometry('600x750')
	api_frame.pack(pady=30)

# Save API key
def save_key():
	filename="api_key"
	try:		
		output_file=open(filename, 'wb')
		pickle.dump(api_entry.get(), output_file)
		api_entry.delete(0, END)
		api_frame.pack_forget()
		root.geometry('600x600')

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

# Create text frame
text_frame=customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add text widget to get GPT responses
my_text=Text(text_frame,bg="#343638",width=65,bd=1,fg="#d6d6d6",relief="flat",wrap=WORD,selectbackground="#1f538d")
my_text.grid(row=0, column=0)

# Create scrollbar for text widget
text_scroll=customtkinter.CTkScrollbar(text_frame,command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

# Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry widget for input text to ChatGPT
chat_entry=customtkinter.CTkEntry(root, placeholder_text="Type Something...",width=535,height=50,border_width=1)
chat_entry.pack(pady=10)

# Create button frame
button_frame=customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create Submit button
submit_button=customtkinter.CTkButton(button_frame,text="Speak to ChatGPT", command=speak)
submit_button.grid(row=0,column=0, padx=25)

# Create Clear button
clear_button=customtkinter.CTkButton(button_frame,text="Clear Response", command=clear)
clear_button.grid(row=0,column=1, padx=35)

# Create API button
api_button=customtkinter.CTkButton(button_frame,text="Update API key", command=key)
api_button.grid(row=0,column=2, padx=25)

#Add API key frame
api_frame=customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)
api_frame.pack_forget()

# Add API enrty widget
api_entry=customtkinter.CTkEntry(api_frame,placeholder_text="Enter your API key",width=350,height=50,border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

#Add API button
api_save_button=customtkinter.CTkButton(api_frame, text="Save Key",command=save_key)
api_save_button.grid(row=0, column=1, padx=10)


root.mainloop()
