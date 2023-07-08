# Bookify 

_Bookify_ is a library management application that intends to combine the functionalities of a library catalog with two content-based recommender systems. It allows users to efficiently manage their personal book collections, discover new books, and receive personalized recommendations based on their reading preferences.

## Features

Bookify offers the following key features:

1. **Library Management**: Users can create a digital library by adding books to their collection. Each book entry contains information such as title, author, publication year, and genre, a list of keywords, and, if available, the top sentiments of the description of the book, The users can organize the books into three categories: __Read__, __Currently Reading__, __To Read__

2. **Book Recommendations**: Bookify incorporates two recommender systems to provide personalized book recommendations:
   - **Keyword-Based Recommender System**: this content-based recommender system takes as input a list of keywords or text from the user and suggests books whose descriptions match the prompt the most.
   - **User Profile-Based Recommender System**: this recommender system suggests books based on the emotional user profile, which consists of the top 5 predominant emotions extracted from the descriptions of the rated books

3. **Search and Discovery**: Bookify allows users to explore a vast collection of books by searching for specific titles, authors, or genres. 

4. **Book Details and Reviews**: Users can access detailed information about each book in the app, including summaries, reviews, ratings. They can also add their own reviews and ratings to share their opinions with the community.

5. **User Profiles**: Bookify enables users to create personalized profiles, where they can manage their book collections, track their reading progress, and view their reading history.

## Used Technologies

- **Front-End**: The front-end of Bookify is developed using Angular, a popular TypeScript-based framework for building web applications. Angular provides a scalable and modular architecture, allowing for the development of responsive and interactive user interfaces.
- **Back-end**: The back-end of Bookify is powered by Flask, a lightweight and flexible Python web framework. Flask offers a simple yet powerful foundation for building web applications, providing features such as routing, request handling, and database integration.
- **Authentication and Authorization**: User authentication and authorization in Bookify are handled using JSON Web Tokens (JWT). JWT provides secure and efficient token-based authentication, ensuring that only authenticated users can access protected resources.

- **External Libraries and Packages**: Bookify utilizes various external libraries and packages to enhance its functionality. Some notable examples include:
  - **SQLAlchemy**: A Python library that simplifies database operations by providing an object-relational mapping (ORM) layer.
  - **Pandas**: A powerful data manipulation library in Python used for handling and processing large volumes of book data efficiently. Pandas provides high-performance data structures and data analysis tools, making it ideal for managing and analyzing tabular data.
  - **Dask**: A flexible parallel computing library in Python used for handling big data processing. Dask enables scalable and distributed computing, allowing Bookify to handle large datasets and perform computations in a distributed manner.
  - **NLTK**: The Natural Language Toolkit (NLTK) is a library in Python used for natural language processing tasks. NLTK provides various tools and resources for tasks such as text preprocessing, tokenization, stemming, and sentiment analysis, enhancing Bookify's ability to analyze and extract insights from textual data.
  - **Bootstrap**: A front-end framework that provides pre-styled components and responsive design capabilities for a visually appealing and user-friendly interface.

## Datasets

- [**Amazon Book Reviews Dataset**](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews)
- [**SenticNet**](https://sentic.net/)

## Demo

- Login Page
  
