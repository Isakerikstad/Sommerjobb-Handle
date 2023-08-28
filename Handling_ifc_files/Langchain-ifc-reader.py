#This script provides an interface for users to upload IFC files and query specific information about the file contents. 
#Utilizing the capabilities of LangChain, it dynamically generates Python code to extract the requested data from the IFC file,
#allowing for flexible and diverse queries related to building models. 

#Improvements to be made:
# 1. Make the code more robust to user input. 2. More Tools for AI to utilize. 3. Split the ifc-file into smaller bits to lower processing time. 4. Paid OpenAI version.


import ifcopenshell as shell
import ifcopenshell.util.element as Element

from langchain.llms import OpenAI
from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    AgentOutputParser,
    load_tools,
    initialize_agent,
    AgentType
)
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.text_splitter import NLTKTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

import sys
import tkinter as tk
from tkinter import filedialog


# load and set our key OPENAI_API_KEY
with open('C:\\Users\\Isak\\Documents\\Programmeringsfiler\\Handle\\Function calling chatGPT\\api_key.txt', 'r') as key:
    api_key = key.read().strip()
llm = ChatOpenAI(openai_api_key=api_key, temperature=0, model="gpt-3.5-turbo-0613")


def select_file():
    #This is a function for selecting the IFC file to be parsed.
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    file = shell.open(filepath)
    return file
file = select_file()

#Here are all the tools for parsing the IFC file. They are all based on the ifcopenshell library.

def get_material(element):
    """Get the material of an element."""
    materials = []
    for elem in file.by_type(element):           
        for rel in elem.HasAssociations:
            if rel.is_a("IfcRelAssociatesMaterial"):
                if rel.RelatingMaterial.is_a('IfcMaterialLayerSetUsage'):
                    try:
                        for mat in rel.RelatingMaterial.ForLayerSet.MaterialLayers:
                            materials.append(f'element with id: {elem.id()}, has material: {mat.Material.Name}')
                    except:
                        try:
                            materials.append(f'element with id: {elem.id()}, has material: {elem.HasAssociations[0][5][0][0][0][0]}')
                        except:
                            materials.append(f'element with id: {elem.id()}, has material: No material')
    return materials

def select_set_by_type(desired_value):
    #Function for selecting all elements of a certain type or description. For example all walls named "IV04".
    # Define your desired attribute and value
    attribute_name = "ObjectType"

    # Iterate over all elements
    selected_elements = []
    for element in file.by_type('IfcRoot'):  # This selects all elements that inherit from IfcRoot
        # Try to get the attribute value. This will fail if the element doesn't have this attribute.
        try:
            attribute_value = element.get_info()[attribute_name]
            # Check if the attribute value is what we want
        except KeyError:
            continue

        if attribute_value is not None and desired_value in attribute_value:
            selected_elements.append(element)

    return selected_elements

def select_by_storey(storey):
    #Tool for selecting all floors
    if storey == "all":
        return file.by_type("IfcBuildingStorey")

    # Tool for selecting all elements on a certain floor. For example all elements on the floor "Plan 01".
    floors = file.by_type("IfcBuildingStorey")
    elements = []

    if storey is None:
        for floor in floors:
            elements.extend(floor.ContainsElements)
        return elements
    else:
        try:
            for floor in floors:
                if floor.Name == storey:
                    elements.extend(floor.ContainsElements)
            return elements
        except:
            return "No floor with that name"

def create_parsing_code(prompt, file=file):
    #This function lets AI create the code for parsing the IFC file.
    chat = ChatOpenAI(openai_api_key=api_key, temperature=0, model="gpt-3.5-turbo-0613")
    messages = [ 
    SystemMessage(content="You are a helpful code writer that specialises in writing functions that parses files using ifcopenshell code library and returns the content. You only parse the predefined file named 'file' given the human prompt. You should only write is so the value is returned, and nothing else but the function, and the it is later going to be called and the result is then fed to another ai, so make it free from errors. So it should only be the function code that is needed to parse the IFC file. It does only takes 'file' as an argument and no other. Do not attempt to open the ifc file as it is already opened and defined as 'file', a global variable. Do not write ifcopenshell.open() "),
    HumanMessage(content=prompt)]
    AI = chat(messages)
    response = AI.content.strip()
    # Execute the code
    # Execute the code and return the result
    try:
        # Create the function using the response
        namespace = {}
        exec(response, namespace)

        # Find the name of the generated function in the namespace
        generated_function_name = None
        for name, value in namespace.items():
            if callable(value):
                generated_function_name = name
                break

        if generated_function_name:
            generated_function = namespace[generated_function_name]
            result = generated_function(file)  # Call the generated function without arguments
            return result
        else:
            return "Generated function not found"
    except Exception as e:
        return f"Error in code: {e}"

def select_by_id(*arg):
    #Tool for selecting an element by its id. It can recieve multiple ids as input.
    elements = []
    for id in arg:
        elements.append(file.by_id(id))
    return elements

"""
def split_file(entity, new_file=file):
    #This tool function splits the IFC file into smaller parts and returns the relevant entity for the task. It is used for lowering the processing time of the AI.
    entity_types = set(element.is_a() for element in file)
    if file.by_type(entity) in entity_types:
        new_file = file.by_type(entity)
        return new_file
"""



          
material_tool = Tool(
    name="get_material",
    func=get_material,
    description="Get a list of materials of given ifc-elements or type. input should be IfcType or IfcElement (like IfcWall, IfcDoor, etc.). It only takes the element type as argument and only works for elements with materials.")

select_by_type_tool = Tool(
    name="select_by_type",
    func=select_set_by_type,
    description="Get a list of elements of given type or description. input should be element type description (like IV04, Betongvegg, etc.). It does not give info on attributes, relating elements or floors or anything else than the description of the element. It only takes the description as argument. A description could be IfcDoor - Focus-ID Hel:YD16, 10,5x21M, sort-hvit, 43dB:2540965")

create_parsing_code_tool = Tool(
    name="create_parsing_code",
    func=create_parsing_code,
    description="Invokes an ai-bot to create code for parsing the IFC file. Good when you need to select items and the other tools do not do the job. Input should be a prompt for the AI to create the code and the code should be executed in the function. It only takes the prompt as argument. Do not give more than one argument!")

storey_tool = Tool(
    name="select_by_storey",
    func=select_by_storey,
    description="If user prompt is asking for all the stories in the file it will get all the stories in the building, then pass 'all' into the function as argument. Or if the user prompt ask for specific elemtns in story it gives you all the element in a certain storey, then pass the storey as argument. There should only be one argument passed to the function and it should be a string.")

id_tool = Tool(
    name="select_by_id",
    func=select_by_id,
    description="Get a list of elements of given id. input should be element id (like #2540965). It only takes the id as argument. It can take multiple ids as argument.")

"""
split_file_tool = Tool(
    name="split_file",
    func=split_file,
    description="Split the IFC file into smaller parts and return the relevant entity for the task. It is used for lowering the processing time of the AI. It only takes the entity as argument. It is used before utilizing other tools to shorten the processing time and lower the number of tokens used in the model. You should pass an argument that is a valid ifc entity. For example 'IfcStorey' or 'IfcWall'. If this tool is used, the other tools will have to use the new file as argument. 'new_file' is the name of the new file.")
"""

exit_tool = Tool(
    name="exit",
    func=exit,
    description="If the input is e or something similar, exit the program")

tools = [material_tool, select_by_type_tool, create_parsing_code_tool, storey_tool, id_tool, exit_tool]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True, max_tokens=1000, max_iterations=3)


#This is the main loop of the program. It asks the user for a query and then returns the result of the query.
query = None
while query != 'e':
    query = input("What would you like to know about the IFC file? e for exit()")
    try:
        response = agent(query)
        print(response)
    except:
        print("Error. Your request probably demanded too many tokens. Try again.") 
