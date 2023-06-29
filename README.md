# Webscraping using selenium and beautifoulsoup
## Job searching on LinkedIn
I built a program to search for jobs using LinkedIn link that is provided by the user or can be provided by the program itself. The final goal is to provide the user with a list of jobs within specified number of pages with information such as the job title, company, location, key skills to be a great fit according to GPT-3. I integrated GPT here to help me identify key skills the recruiter are looking for. 

Current Features:
- User can provide LinkedIn link that links to the specific job page.
- User can provide number of pages they want to search for.
- Error handling of inputs.
- GPT integration.
- Prints each job found in the page with information including job title, company, location, level, and key skills required (GPT).
- Auto fill login credentials with own user and password (when finalised I will change it to user input).
- Uses API key for using GPT (requesting to openai API).
