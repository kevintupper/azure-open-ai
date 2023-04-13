import sass  
  
def compile_scss():  
    with open("style.scss", "r") as scss_file, open("style.css", "w") as css_file:  
        css_content = sass.compile(string=scss_file.read())  
        css_file.write(css_content)  
  
if __name__ == "__main__":  
    compile_scss()  
