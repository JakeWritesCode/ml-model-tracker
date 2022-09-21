The idea here is that I want to be able to create a semi automated 'checkpoint' 
when working on training ML models.

This thing should:
- Be imported into a notebook.
- Automatically commit when you get to a certain point, saving the code at point of training.
- Make the commit hash available so you can save data in S3 against it, meaning the data is retained.
- Allow you to save whatever params are important in a dict.
- Save the params, and the results of the model test into a csv so you have a log.