# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:47:46 2023

@author: chico
"""
import tkinter as tk
from tkinter import *
import random
import time
import pandas as pd
import serial
import threading
import datetime
import ast

from menuTest import MenuTest
from dish import Dish
from ingredientType import IngredientType
from task import Task


# Define the trial counter and set size for the sternberg task
trial_counter = 0
set_size = 2
current_time = time.time()
timestamp_format = "%H:%M:%S"
TLXquestions = ['How mentally demanding was the task?', 'How physically demanding was the task?', 'How hurried or rushed was the pace of the task?', 'How successful were you in accomplishing what you were asked to do?', 'How hard did you have to work to accomplish your level of performance?', 'How insecure, discouraged, irritated, stressed, and annoyed were you?']
terminate_flag = False
terminator = True

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
            df_sensor.to_excel("serial_data_ECO.xlsx")
        
        
## In order to run the the read_serial function and the GUI at the same time, we need to create a new thread for the read_serial function ##
# Create a new thread for serial_read function
serial_read_thread = threading.Thread(target=serial_read)

# Start the thread
serial_read_thread.start()



def userInputValidator(pressedKey, dishList, dishCorrect):
    print(pressedKey)
    if pressedKey > len(dishList):
        return bool(False)
    
    userSelectedDish = dishList[pressedKey - 1]
    if userSelectedDish.dishId == dishCorrect.dishId:
        return bool(True)
    else:
        return bool(False)

def nasaTLXInputValidator(pressedKey):
    print(pressedKey)
    nasaTLXConfirmation = ['1']
    if pressedKey > len(nasaTLXConfirmation):
        return bool(False)
    

def ecologicalValidity_task():
    # Define the list of tasks to choose from
    tasks = list(Task)


    # Define the lists to store the results
    correctness_list = []
    response_times_list = []
    timestamp_list = []
    trial_list = []
    # Define the function to start the trial
    def start_trial():
        global set_size, trial_counter
        
        # Increment the trial counter
        trial_counter += 1
        
        # If the trial counter is divisible by 3, increase the set size
        #if trial_counter % 3 == 0:
         #   set_size += set_size_increment
        
        # Clear the feedback
        response_times_label.config(text='')
        feedback_label.config(text='')
        
        # Clear the test letter label
        test_letter_label.config(text='')
        
        # Choose a random set of letters
        textToShow = ""
        tasks_set = tasks[trial_counter - 1]
        print("Tasks set", tasks_set)
        menu = MenuTest.getTasks(tasks_set)
        print("Menu ", menu.dishes)
        for i in range(len(menu.dishes)):
            print(i, menu.dishes[i])
            textToShow += ' '.join(menu.dishes[i].getDish())

            
        letter_set_label.config(text=textToShow)
        # Wait for 10 seconds then show blank screen
        root.after(10000, lambda: show_blank_screen(menuTest= menu))
        

    # Define the function to show a blank screen
    def show_blank_screen(menuTest: MenuTest):
        # Clear the letter set label
        letter_set_label.config(text='')
        
        # Clear the test letter label
        test_letter_label.config(text='')

        # Wait for 3 seconds then show test letter
        root.after(3000, lambda: show_question(menuTest))

        
    # Define the function to show the test letter
    def show_question(menuTest: MenuTest):
        
        # Clear the letter set label
        letter_set_label.config(text='')
        
        # Display the test letter
        question_Text = "Your friend " + menuTest.question + "\n\nWhich dish would you choose?"
        test_letter_label.config(text=question_Text)

        # Record the start time
        start_time = time.time()

        # Bind the on_key_press function to the root window
        root.bind('<KeyPress>', lambda event: on_key_press(event.char, menuTest.dishes, menuTest.correctDish, start_time))

    # Define the function to handle key presses
    def on_key_press(key, dishes, correctDish, start_time):
        # Record the response time
        response_time = time.time() - start_time
        # Display the response time
        response_times_label.config(text=f"Response time: {response_time:.2f} seconds")
        userResponseKey = int(key) # User response key
        isUserCorrect = userInputValidator(userResponseKey, dishes, correctDish)

        if isUserCorrect == True:
             feedback_label.config(text='Correct!')
             correctness = 'Correct'
        else:
            feedback_label.config(text='Incorrect!')
            correctness = 'Incorrect'

        # Append the correctness and response time to the results lists
        correctness_list.append(correctness)
        response_times_list.append(response_time)
        timestamp_list.append(datetime.datetime.now().strftime(timestamp_format))
        trial_list.append(trial_counter)

        # Unbind the on_key_press function from the root window
        root.unbind('<KeyPress>')

        #Save the results to a file
        save_results(correctness_list, response_times_list)
        
        if trial_counter % 3 == 0:
            root.after(3000, lambda: createNasaTLXQuestions(TLXquestions))        
        elif trial_counter % 10 == 0:
            root.after(3000, lambda: createNasaTLXQuestions(TLXquestions))
        else:
            root.after(3000, start_trial)      


    # # Define the function to show the test letter
    def createNasaTLXQuestions(TLXquestions):
        def on_keypress(event):
            try:
                question_Text = next(question_generator)
                test_letter_label.config(text=question_Text)
            except StopIteration:
                print("Trial counter", trial_counter)
                # Show results after 10 trials
                if trial_counter == 3:
                    show_results()
                #if not 10 trials yet, start another trial
                else:
                # Start a new trial
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
        TLXquestionsCopy = list(TLXquestions)
        root.bind('<KeyPress-q>', on_keypress)
        question_generator = question_generator()
        question_Text = next(question_generator)
        test_letter_label.config(text=question_Text)
    def close_window():
        global terminate_flag
        terminate_flag = True
        serial_read_thread.join()
        while terminate_flag == True:
            datamerge()
            root.destroy()
        
    def show_results():
        # Unbind the on_key_press function from the root window
        root.unbind('<KeyPress>')
        
        # Calculate the average response time
        avg_response_time = sum(response_times_list) / len(response_times_list)

        # Count the number of correct and incorrect responses
        num_correct = correctness_list.count('Correct')
        num_incorrect = correctness_list.count('Incorrect')
        
        # Remove the instructions and the letter set labels
        instructions_label.pack_forget()
        start_button.pack_forget()
        letter_set_label.config(text='This is the end of the experiment')
        response_times_label.config(text='')
        feedback_label.config(text='')
        test_letter_label.config(text='')
        
        #Display results
        resultpage_label = tk.Label(root, text=f"Thank you for participating!\n\nAverage Response Time: {avg_response_time:.2f} seconds\nNumber of Correct Responses: {num_correct}\nNumber of Incorrect Responses: {num_incorrect}", font=("Arial", 16))
        resultpage_label.pack(pady=10)
        root.after(3000, close_window)
        
    def save_results(correctness_list, response_times_list):
        # Create a Pandas DataFrame to store the results
        results_df = pd.DataFrame({'Correctness': correctness_list, 'Response Time (s)': response_times_list, 'Timestamp': timestamp_list})
        # Add the timestamp to the DataFrame
        results_df.to_excel('task_resultsECO.xlsx')
 
    




    # Define the root window
    root = tk.Tk()


    # Define the initial instructions
    instructions = "Scenario\nYou are meeting your friends at a restaurant. However, they are late and want you to order a dish for them already. Each of them have different things they want to take into account in their dish.\n1) You will be shown menus with different dishes for 10 seconds. It will start with 2 dishes and will rise throughout.\n2) Remember the given details for each dish.\n3) Decide on a dish based on the given requirements as fast as possible.\n4) You will be shown 6 follow-up questions after each task. Answer these questions with the slider at hand and follow the instructions shown on the screen."
    instructions_label = tk.Label(root, text=instructions, font=('Arial', 11))
    instructions_label.pack(padx=10, pady=10)

    # Create a button to start the task
    start_button = tk.Button(root, text='Start', command= start_trial)
    start_button.pack(padx=10, pady=10)

    # Create a label to display the letters for each trial
    letter_set_label = tk.Label(root, font=('Univers', 15))
    letter_set_label.pack(padx=10, pady=10)

    # Create a label to display the test letter
    test_letter_label = tk.Label(root, font=('Univers', 15))
    test_letter_label.pack(padx=10, pady=10)

    # Create a label to display the response times
    response_times_label = tk.Label(root)
    response_times_label.pack(padx=10, pady=10)

    # Create a label to display the feedback
    feedback_label = tk.Label(root, font=('Arial', 24))
    feedback_label.pack(padx=10, pady=10)

    #Create a label to display the NasaTLX
    nasaTLX_label = tk.Label(root, font=('Univers', 15))
    nasaTLX_label.pack(padx=10, pady=10)

    # Start the GUI
    root.mainloop()

def datamerge(): 
    while terminate_flag == True:    
        print('data merged')
        results_df = pd.read_excel(r'C:\Users\brain\OneDrive\Desktop\TSS task\RestaurantTask\task_resultsECO.xlsx')
        df_sensor = pd.read_excel(r'C:\Users\brain\OneDrive\Desktop\TSS task\RestaurantTask\serial_data_ECO.xlsx')
        df_merged = pd.merge(results_df, df_sensor, on='Timestamp', how='outer')
        # Save the results to an Excel file named 'results.xlsx'
        df_merged.to_excel('results.xlsx')
        print(df_merged)

RestaurantTask_thread = threading.Thread(target=ecologicalValidity_task)

# Start the thread
RestaurantTask_thread.start()


