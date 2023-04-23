# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:47:46 2023

@author: brain
"""

import tkinter as tk
import random
import time
import pandas as pd
import serial
import threading
import datetime
import ast

# Define some variables needed throughout the code
trial_counter = 0 #trial counter to keep track of how many trials have been completed
set_size = 4 #initial set size of 4 
current_time = time.time() #current time 
timestamp_format = "%H:%M:%S" #format for timestamp
terminate_flag = False
#results_df = pd.DataFrame(columns=['Trial', 'Set Size', 'Correctness', 'Response Time (s)', 'Timestamp'])
TLXquestions = ['How mentally demanding was the task?', 'How physically demanding was the task?', 'How hurried or rushed was the pace of the task?', 'How successful were you in accomplishing what you were asked to do?', 'How hard did you have to work to accomplish your level of performance?', 'How insecure, discouraged, irritated, stressed, and annoyed were you?']
correctness_list = []
response_times_list = []
timestamp_list = []
trial_list = []

# Define the function to receive data from picoboard over the serial port and save the results to a file
def serial_read():
    # Define some variables needed throughout the code
    serialInst = serial.Serial()   # Create a serial instance
    transmission_rate = 0.005 # Define the transmission rate at which data is received from the serial port
    last_received_time = time.time() # Define the last received time as the current time
    portVar = "COM11" # Define the serial port to use
    serialInst.baudrate = 921600 # Define the baud rate
    serialInst.port = portVar # Assign the serial port to the serial instance
    serialInst.open()  # Open the serial port
    df_sensor = pd.DataFrame(columns=["Timestamp", "Sensor1", "Sensor2", "Sensor3"]) # Create an empty DataFrame to store the received data
    
    # Define the function to read data from the serial port
    while not terminate_flag:
        current_time = time.time()
        if serialInst.in_waiting > 0 and current_time - last_received_time > transmission_rate: # Don't read the serial port if there is no data or if the transmission rate is too high
            formatted_time = time.strftime(timestamp_format, time.localtime(current_time)) # Format the current time
            last_received_time = current_time # Update the last received time
            packet = serialInst.readline()# Read the data from the serial port and assign it to the packet variable
            #print(f"{formatted_time}: {packet.decode('utf')}") # Print the received data
            data = packet.decode('utf') # Decode the received data and assign it to the data variable
            data_list = ast.literal_eval(data)        
            Sensor1 = [nested_list[0] for nested_list in data_list]
            Sensor2 = [nested_list[1] for nested_list in data_list]
            Sensor3 = [nested_list[2] for nested_list in data_list]
            Sensor4 = [nested_list[3] for nested_list in data_list]
            df_sensor = pd.concat([df_sensor, pd.DataFrame({"Timestamp": formatted_time, "Sensor1": Sensor1, "Sensor2": Sensor2, "Sensor3": Sensor3, "Board_Time": Sensor4})], ignore_index=True) # Append the received data to the DataFrame
            print('collecting')
            # Save the DataFrame to an Excel file
            df_sensor.to_excel("serial_data_SMT.xlsx")
           

        
        
## In order to run the the read_serial function and the GUI at the same time, we need to create a new thread for the read_serial function ##
# Create a new thread for serial_read function
serial_read_thread = threading.Thread(target=serial_read)

# Start the thread
serial_read_thread.start()

   
        
# Define the function for the sternberg task
def sternberg_task():
    # Define the list of letters to choose from
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Define how much to increase the set size by
    set_size_increment = 1

    

    # Define the lists to store the results


    # Define the function to start the trial
    def start_trial():
        global set_size, trial_counter # Define the set_size and trial_counter variables as global variables so that they can be changed within the function
        
        
        
        # If the trial counter is divisible by 3, increase the set size, this way, the set size will increase every 3 trials
        if trial_counter % 3 == 0:
            set_size += set_size_increment
            
        # Increment the trial counter
        trial_counter += 1
        
        # Clear the feedback label and response times label in the GUI
        response_times_label.config(text='')
        feedback_label.config(text='')
        nasa_question_label.config(text='')
        
        # Clear the test letter label
        test_letter_label.config(text='')
        
        # Choose a random set of letters from the letters list based on the set size
        letter_set = random.sample(letters, set_size)
        
        # Display the letters for this trial in the GUI
        letter_set_label.config(text=' '.join(letter_set))
        
        # Wait for 3 seconds then show blank screen 
        root.after(3000, lambda: show_blank_screen(letter_set))
        
    # Define the function to show a blank screen
    def show_blank_screen(letter_set):
        # Clear the letter set label
        letter_set_label.config(text='')
        
        # Clear the test letter label
        test_letter_label.config(text='')

        # Wait for 3 seconds then show test letter
        root.after(3000, lambda: show_test_letter(letter_set))

        
    # Define the function to show the test letter
    def show_test_letter(letter_set):
        
        # Clear the letter set label
        letter_set_label.config(text='')
        
        # Choose a random test letter
        test_letter = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

        # Display the test letter
        test_letter_label.config(text=test_letter)

        # Record the start time
        start_time = time.time()

        # Bind the on_key_press function to the root window
        root.bind('<KeyPress>', lambda event: on_key_press(event.char, letter_set, test_letter, start_time))

    # Define the function to handle key presses
    def on_key_press(key, letter_set, test_letter, start_time):
        # Record the response time
        response_time = time.time() - start_time
        # Display the response time
        response_times_label.config(text=f"Response time: {response_time:.2f} seconds")

        # Check if the key press was correct
        if key.lower() == 'y' and test_letter in letter_set: # If the key press was correct, display the correct message
            feedback_label.config(text='Correct!')
            correctness = 'Correct' # Set the correctness variable to 'Correct'
        elif key.lower() == 'n' and test_letter not in letter_set: 
            feedback_label.config(text='Correct!')
            correctness = 'Correct' # Set the correctness variable to 'Correct'
        else:
            feedback_label.config(text='Incorrect!') # If the key press was incorrect, display the incorrect message
            correctness = 'Incorrect' # Set the correctness variable to 'Incorrect'

        # Append the correctness and response time to the results lists
        correctness_list.append(correctness) # Append the correctness variable to the correctness_list
        response_times_list.append(response_time) # Append the response_time variable to the response_times_list
        timestamp_list.append(datetime.datetime.now().strftime(timestamp_format)) # Append the current timestamp to the timestamp_list
        trial_list.append(trial_counter)
        # Save the results to a file
        save_results(correctness_list, response_times_list)
        
        # Unbind the on_key_press function from the root window
        root.unbind('<KeyPress>')

        

        if trial_counter % 3 == 0:
            root.after(3000, lambda: createNasaTLXQuestions(TLXquestions))        
        elif trial_counter % 10 == 0:
            root.after(3000, lambda: createNasaTLXQuestions(TLXquestions))
        else:
            root.after(3000, start_trial)

    def createNasaTLXQuestions(TLXquestions):
        def on_keypress(event):
            try:
                question_Text = next(question_generator)
                nasa_question_label.config(text=question_Text)
            except StopIteration:
                print("Trial counter", trial_counter)
                # Show results after 10 trials
                        # Show results after 10 trials
                if trial_counter == 3:
                    show_results()
                #if not 10 trials yet, start another trial
                elif trial_counter <=3:
                    root.unbind('<KeyPress>')
                    feedback_label.config(text='Next trial')
                    print("Start trial again")
                    root.after(3000, start_trial)
    
        def question_generator():
            for question in random.sample(TLXquestionsCopy, len(TLXquestionsCopy)):
                question_Text = question + "\n\n\nUse the slider to adjust your answer.\nPress Q on the keyboard to continue"
                yield question_Text
    
        #make the screen blank again
        feedback_label.config(text='')
        response_times_label.config(text='')
        test_letter_label.config(text='')
        TLXquestionsCopy = list(TLXquestions)
        root.bind('<KeyPress-q>', on_keypress)
    
        question_generator = question_generator()
        question_Text = next(question_generator)
        nasa_question_label.config(text=question_Text)

    def close_window():
        global terminate_flag
        terminate_flag = True
        serial_read_thread.join()
        while terminate_flag == True:
            datamerge()
        
        
    # Define the function to show the results
    def show_results():
        # Unbind the on_key_press function from the root window
        root.unbind('<KeyPress>')
        
        # Calculate the average response time
        avg_response_time = sum(response_times_list) / len(response_times_list)

        # Count the number of correct and incorrect responses
        num_correct = correctness_list.count('Correct')
        num_incorrect = correctness_list.count('Incorrect')
        
        # Remove the instructions and the letter set labels from the GUI 
        instructions_label.pack_forget()
        start_button.pack_forget()  
        nasa_question_label.config(text='')
        letter_set_label.config(text='This is the end of the experiment')
        
        response_times_label.config(text='')
        feedback_label.config(text='')
        test_letter_label.config(text='')
        
        #Display results
        resultpage_label = tk.Label(root, text=f"Thank you for participating!\n\nAverage Response Time: {avg_response_time:.2f} seconds\nNumber of Correct Responses: {num_correct}\nNumber of Incorrect Responses: {num_incorrect}", font=("Arial", 16))
        resultpage_label.pack(pady=10)
        root.after(5000, close_window)
        
    # Define the functions to save the results to a file
    def save_results(correctness_list, response_times_list): 
        # Create a Pandas DataFrame to store the results

        results_df = pd.DataFrame({'Correctness': correctness_list, 'Response Time (s)': response_times_list, 'Timestamp': timestamp_list})
        results_df.to_excel('task_results.xlsx')
    



    # Define the GUI
    # Define the root window and title
    root = tk.Tk()
    root.title('Sternberg Memory Task')
    # Define the initial instructions
    instructions = "1. You will see a set of 5 Letters for 4 seconds. \n2. You will then see a Blank screen for 3 seconds. \n3. You will then see a test letter and have to indicate \nwhether this was part of the 5 letter set \n \n If the letter was part of the set press Y \n If the letter was not part of the set press N"
    instructions_label = tk.Label(root, text=instructions, font=('Helvetica', 18))
    instructions_label.pack(padx=10, pady=10)

    # Create a button to start the task
    start_button = tk.Button(root, text='Start', command= start_trial)
    start_button.pack(padx=10, pady=10)

    # Create a label to display the letters for each trial
    letter_set_label = tk.Label(root, font=('Helvetica', 36))
    letter_set_label.pack(padx=10, pady=10)

    # Create a label to display the test letter
    test_letter_label = tk.Label(root, font=('Helvetica', 48))
    test_letter_label.pack(padx=10, pady=10)

    # Create a label to display the nasaTLX question
    nasa_question_label = tk.Label(root, font=('Helvetica',13))
    nasa_question_label.pack(padx=10, pady=10)

    # Create a label to display the response times
    response_times_label = tk.Label(root)
    response_times_label.pack(padx=10, pady=10)

    # Create a label to display the feedback
    feedback_label = tk.Label(root, font=('Helvetica', 24))
    feedback_label.pack(padx=10, pady=10)

    # Start the GUI
    root.mainloop()


# Create a new thread for the task
sternberg_task_thread = threading.Thread(target=sternberg_task)

# Start the thread
sternberg_task_thread.start()

def datamerge(): 
    while terminate_flag == True:    
        print('data merged')
        results_df = pd.read_excel(r'C:\Users\brain\OneDrive\Desktop\Sensor Data and MWL Tasks\SMT\task_results.xlsx')
        df_sensor = pd.read_excel(r'C:\Users\brain\OneDrive\Desktop\Sensor Data and MWL Tasks\SMT\serial_data_SMT.xlsx')
        df_merged = pd.merge(results_df, df_sensor, on='Timestamp', how='outer')
        # Save the results to an Excel file named 'results.xlsx'
        df_merged.to_excel('results.xlsx')
        
    