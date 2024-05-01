# App Imports
import streamlit as st

# AI Imports
import google.generativeai as genai
import os

# Carbon Measurement imports
import eco2ai

# File Handling Imports
import subprocess
import csv
import pandas as pd


# Carbon Tracker Object Initialization
tracker = eco2ai.Tracker(project_name="CodeOptimizer", experiment_description="Optimizing energy consumed by codes")

# Gemini Model Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# User Input Handling
def process_input(input_text, area, language):

    # Temporary Best Values
    best_value = 100
    best_code = ""
    og_val = best_value

    # Processing Gemini Output To Make It Completely Executable
    def remove_python_code_block(string):
        if string.startswith("```python"):
            string = string[len("```python"):].lstrip()

        if string.endswith("```"):
            string = string[:-len("```")].rstrip()

        return string
    

    # Get list of alternatives for area specified by users
    response = model.generate_content(input_text + "Given the previous code, identify all libraries related to " + area + "and return a string of at least 4 CLOSELY RELATED alternatives that DO ONLY " + area + " to it as per the code's use case each separated by a space in " + language + ". Do not include any other text in your answer apart from this string of all alternatives, please include at least 4.")
    libraries = list(response.text.split(" "))

    # Add current code in the middle of array so that carbon measurement happens in same environment
    middle_index = len(libraries) // 2
    libraries = libraries[:middle_index] + ["self"] + libraries[middle_index:]

    # For each alternative
    for library in libraries:

        # Add that dependency if required
        result = subprocess.run("poetry add " + library, shell=True, capture_output=True, text=True)

        # Generate alternative code for current library
        alternative = model.generate_content(input_text + "Given the previous code, rewrite it exactly and correctly using " + library + ". The goal is to maintain the functionality of the original code while adapting it to the syntax and conventions of the target library. Ensure that the data types, functions, and overall structure of the code are preserved and that it is fully complete and correct with all imports and does only what the given code does and nothing more and return only the code. Give your answer as a string and not markdown")

        
        try:
            # If we reach original code
            if library == "self":
                # Measure original code's carbon emission
                tracker.start()
                exec(input_text)
                tracker.stop()

                # Get emissions and set as original benchmark to surpass
                file_path = "emission.csv"
                df = pd.read_csv(file_path)
                og_val = float(df.iloc[-1]["CO2_emissions(kg)"])
            else:
                # Format alternate code
                newcode = remove_python_code_block(alternative.text)

                # Measure alternate code's carbon emission
                tracker.start()
                exec(newcode)
                tracker.stop()

                # Display current alternative to user
                st.info("Alternative: " + library+"\n")
                st.code(newcode)
                
                # Obtain emissions for current alternative
                file_path = "emission.csv"
                df = pd.read_csv(file_path)
                latest_value = float(df.iloc[-1]["CO2_emissions(kg)"])

                # Display current alternative's emissions to user
                st.warning("Carbon Emissions: "+str(latest_value)+" (kg)")
                st.write("\n\n")

                # If this alternative has better emissions, update best value and corresponding code
                if latest_value < best_value :
                    best_value = latest_value
                    best_code = alternative.text
            

        # In case an error comes disacrd that entry
        except Exception as e:
            tracker.start()
            tracker.stop()
            with open('emission.csv', 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                rows = list(csv_reader)

            if rows:
                rows.pop()

            with open('emission.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(rows)
            print("An error occurred:", e)

    # Display results and best alternate code to use
    st.info("Original Emission: "+str(og_val))
    if og_val < best_value:
        best_value = og_val
    return [remove_python_code_block(best_code), best_value, (((og_val - best_value)/og_val)*100)]

def main():
    # Headings
    st.title("Code Optimizer")
    st.write("Find alternatives to reduce the carbon footprint of your code")

    # User Input
    input_lang = st.text_input("Enter language of code:")
    input_area = st.text_input("Enter area to optimize:")
    input_text = st.text_area("Enter some code:", height=200)

    # Getting input and processing
    if st.button("Process"):
        if input_text and input_area and input_lang:
            output_text = process_input(input_text, input_area, input_lang)
            st.write("Best Code:\n")
            st.code(output_text[0])
            st.success("Carbon Emissions: "+str(output_text[1])+" (kg) with "+str(output_text[2])+"% reduction")
        else:
            st.write("Please enter some text.")

# Running The App
if __name__ == "__main__":
    main()

