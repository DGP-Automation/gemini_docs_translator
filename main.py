import tkinter as tk
from tkinter import filedialog, ttk
import os
from google import genai
from dotenv import load_dotenv
from prompt import base_prompt


load_dotenv()
gemini_token = os.getenv('GEMINI_TOKEN')
client = genai.Client(api_key=gemini_token)


def translate(prompt: str) -> str:
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=prompt
    )
    return response.text


def select_file():
    """Select a file and print the path"""
    file_path = filedialog.askopenfilename(
        title="Select a Markdown file",
        filetypes=[("Markdown file", "*.md"), ("All Files", "*.*")]
    )
    if file_path:
        file_label.config(text=f"File path: {file_path}")
        global selected_file_path
        selected_file_path = file_path

def execute_logic(file_path, mode, language):
    """
    Main execution logic
    :param file_path: File path
    :param mode: Mode (generator, updater)
    :param language: language (cht, jp, en)
    """
    mode = mode.lower()
    print(f"File Path: {file_path}")
    print(f"Mode: {mode}")
    print(f"Language: {language}")

    if "/zh/" not in file_path:
        result_label.config(text="ZH document is needed")
        return None

    language_path = {
        "Traditional Chinese (Taiwan)": "cht",
        "English": "en",
        "Japanese": "jp"
    }

    # Check if target file is existed
    target_file_path = file_path.replace(r"/zh/", f"/{language_path[language]}/")
    target_file_exist = os.path.exists(target_file_path)
    print(f"{target_file_path} exist: {target_file_exist}")
    if target_file_exist and mode=="generator":
        print(f"{target_file_path} already exist, cannot use generator.")
        result_label.config(text=f"{target_file_path} already exist, cannot use generator.")
        return None
    elif not target_file_exist and mode=="updater":
        print(f"{target_file_path} not exist, cannot use updater.")
        result_label.config(text=f"{target_file_path} not exist, cannot use updater.")
        return None

    origin_markdown_content = open(file_path, "r", encoding="utf-8").read()

    if mode == "generator":
        # Generator Mode
        generator_prompt = base_prompt.format(raw_markdown_content=origin_markdown_content,
                                              special_instructions="",
                                              target_language=language)
        translated_content = translate(generator_prompt)
    elif mode == "updater":
        # Updater Mode
        current_translated_content = open(target_file_path, "r", encoding="utf-8").read()
        updater_prompt = f"""Currently, there is already a  translated version of this file but it's outdated. Please update it based on the current version. Do not make unnecessary changes (but you can still fix typo, grammar or wrong word usage), still output the entire translated document.
        **Current version:** 
        {current_translated_content}
        """
        generator_prompt = base_prompt.format(raw_markdown_content=origin_markdown_content,
                                              special_instructions=updater_prompt,
                                              target_language=language)
        translated_content = translate(generator_prompt)
    else:
        result_label.config(text="Unsupported mode.")
        return None

    lines = translated_content.splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        translated_content = "\n".join(lines[1:-1])

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    with open(target_file_path, "w+", encoding="utf-8") as f:
        f.write(translated_content)
    result_label.config(text=f"{target_file_path} translated with updater mode.")


def execute():
    if selected_file_path:
        selected_mode = mode_var.get()
        selected_language = language_var.get()
        execute_logic(selected_file_path, selected_mode, selected_language)
    else:
        file_label.config(text="Please pick a file")

root = tk.Tk()
root.title("Snap Hutao Docs Translator")
root.geometry("400x400")

file_label = tk.Label(root, text="No file selcted", wraplength=380)
file_label.pack(pady=10)

select_button = tk.Button(root, text="Select Markdown file", command=select_file)
select_button.pack(pady=10)

mode_var = tk.StringVar(value="Generator")
mode_label = tk.Label(root, text="Select Mode:")
mode_label.pack()
mode_dropdown = ttk.Combobox(root, textvariable=mode_var, values=["Generator", "Updater"], state="readonly")
mode_dropdown.pack()

language_var = tk.StringVar(value="Traditional Chinese (Taiwan)")
language_label = tk.Label(root, text="Target Language:")
language_label.pack()
language_dropdown = ttk.Combobox(root, textvariable=language_var, values=["Traditional Chinese (Taiwan)", "English", "Japanese"], state="readonly")
language_dropdown.pack()

execute_button = tk.Button(root, text="Translate", command=execute)
execute_button.pack(pady=20)

result_label = tk.Label(root, text="", wraplength=380, fg="blue")
result_label.pack(pady=10)

selected_file_path = None

root.mainloop()
