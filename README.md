# sumo


### 1. Set Up the Project Structure

Create a new folder for your project and organize it as follows:

```plaintext
 youtube-summarizer/youtube-summarizer/
├── backend/
│   └── app.py (your Flask backend code)
├── frontend/
│   └── index.html (the HTML file above)
└── .env (for your API keys)

```

### 2. Set Up the Backend

1. Create a virtual environment:


```shellscript
 cd youtube-summarizer/backendcd youtube-summarizer/backend
python -m venv venv

```

2. Activate the virtual environment:


- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`


3. Install required packages:


```shellscript
 pip install flask flask-cors youtube-transcript-api python-dotenv requestspip install flask flask-cors youtube-transcript-api python-dotenv requests

```

4. Create `.env` file in the backend folder:


```plaintext
 GEMINI_API_KEY=your_api_key_hereGEMINI_API_KEY=your_api_key_here
GEMINI_API_URL=your_api_url_here

```

### 3. Set Up the Frontend

1. Simply save the HTML file provided above in the frontend folder
2. No additional setup is needed as all CSS and JavaScript are included in the HTML file


### 4. Run the Application

1. Start the Flask backend:


```shellscript
 cd backendcd backend
python app.py

```

The backend will run on `http://localhost:5000`

2. Open the frontend:


- Using VS Code's Live Server extension:

- Install the "Live Server" extension in VS Code
- Right-click on index.html and select "Open with Live Server"



- Or simply open the index.html file in your browser


### 5. Using the Application

1. Enter a YouTube video URL in the input field
2. Set the number of questions you want (1-10)
3. Click "Analyze"
4. Wait for the results to appear in the three sections
5. Click on flashcards to reveal answers


### 6. Troubleshooting

- If you see CORS errors, ensure the Flask backend has CORS properly configured
- If the backend fails to start, check that all required packages are installed
- If the API calls fail, verify your API keys in the .env file
- Make sure the backend URL in the frontend JavaScript matches your Flask server address


The implementation includes:

1. A responsive dark-themed UI matching the provided screenshot
2. Error handling and loading states
3. Interactive quiz and flashcard components
4. Full integration with the Flask backend
5. All styles and scripts in a single file for easy deployment
