This project is a quiz application built using Flask, a micro web framework for Python, along with SQLAlchemy, which is used for database management. The application allows users to select quiz topics from a dropdown menu, then presents them with random questions from the chosen category. After answering the questions, users can check their answers, and the application will display the score.

The project consists of several components:

*  kviz.py: This file contains the main Flask application code. It defines routes for handling user requests, retrieving questions from the database based on the selected category, processing user responses, and calculating the score.

*  index.html: This HTML template file provides the user interface for selecting quiz topics. It contains a dropdown menu where users can choose a quiz category and a button to submit their selection.

*  pitanja.html: This HTML template file is responsible for displaying the quiz questions to the user. It dynamically generates HTML elements based on the questions retrieved from the database and includes a form for users to submit their answers.

*  SQL files: These SQL files contain the schema and sample data for different quiz categories, such as films, games, history, etc. They define the structure of the database tables storing quiz questions and correct answers.

Overall, this project serves as a simple yet functional quiz application where users can test their knowledge across various topics. It provides a basic user interface and utilizes a relational database to store and manage quiz data. Users can interact with the application via a web browser, select quiz categories, answer questions, and receive immediate feedback on their performance.
