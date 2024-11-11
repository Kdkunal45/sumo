document.getElementById('videoForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const videoUrl = document.getElementById('videoUrl').value;
    const numQuestions = parseInt(document.getElementById('numQuestions').value);
    
    document.getElementById('error').style.display = 'none';
    document.getElementById('summaryText').innerText = '';
    document.getElementById('quizContent').innerHTML = '';
    document.getElementById('flashcardContent').innerHTML = '';
    
    try {
        // Send POST request to the backend
        const response = await fetch('http://127.0.0.1:5000/process_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                videoUrl: videoUrl,
                numQuestions: numQuestions
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        
        // Display results
        document.getElementById('summaryText').innerText = result.summary;
        displayQuiz(result.quiz);
        displayFlashcards(result.flashcards);

    } catch (error) {
        document.getElementById('error').innerText = 'An error occurred: ' + error.message;
        document.getElementById('error').style.display = 'block';
    }
});

function showTab(tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.add('hidden');
    }
    document.getElementById(tabName).classList.remove('hidden');
}

function displayQuiz(quiz) {
    const quizContent = document.getElementById('quizContent');
    quizContent.innerHTML = '';
    quiz.forEach((question, index) => {
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `
            <h3>Question ${index + 1}</h3>
            <p>${question.question}</p>
            <ul>
                ${question.options.map(option => `<li>${option}</li>`).join('')}
            </ul>
        `;
        quizContent.appendChild(questionElement);
    });
}

function displayFlashcards(flashcards) {
    const flashcardContent = document.getElementById('flashcardContent');
    flashcardContent.innerHTML = '';
    flashcards.forEach((flashcard, index) => {
        const flashcardElement = document.createElement('div');
        flashcardElement.innerHTML = `
            <h3>Flashcard ${index + 1}</h3>
            <p><strong>Question:</strong> ${flashcard.question}</p>
            <p><strong>Answer:</strong> ${flashcard.answer}</p>
        `;
        flashcardContent.appendChild(flashcardElement);
    });
}