// function activateTab(selectedTab, contentId) {
//     const tabs = document.querySelectorAll('.tab');
//     const contents = document.querySelectorAll('.content');
    
//     tabs.forEach(tab => tab.classList.remove('active'));
//     contents.forEach(content => content.classList.remove('active'));

//     selectedTab.classList.add('active');
//     document.getElementById(contentId).classList.add('active');
// }

// Get all language tabs, content sections, and the single speak button
const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.content');
const speakButton = document.getElementById('btn-speak');
const playPauseButton = document.getElementById('btn-playpause');
const playPauseIcon = document.getElementById('playpauseicon');
let audio = null;

// Map of languages to their respective language codes
const languageMap = {
transcript: 'en',
en: 'en',
hi: 'hi',
mr:'mr',
gu:'gu',
ml:'ml',
kn:'kn',
bn:'bn',
pa:'pa',
ta:'ta',
te:'te',
ar:'ar',
fr: 'fr',
de: 'de',
ja:'ja',
ru:'ru',
es: 'es',
// Add more languages here
};

// Function to handle tab switching
function switchTab(event) {
    // Deactivate all tabs and content sections
    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));

    // Activate the clicked tab
    const selectedLang = event.target.dataset.lang;
    // console.log(selectedLang);
    event.target.classList.add('active');
    document.getElementById(selectedLang).classList.add('active');

}

// Add event listener for tab switching
tabs.forEach(tab => tab.addEventListener('click', switchTab));

// Add event listener for the single Speak button
// speakButton.addEventListener('click', speakActiveTabContent);
speakButton.addEventListener("click", async () => {
    const activeElement = document.querySelector('.content.active');
    const activeContent = activeElement.textContent;

    if (!activeContent) {
        alert("No content to speak.");
        return;
    }

    if(audio) {
        audio.pause();
        audio.currentTime=0;
    }
    
    try {
        // Get the language code for the active tab
        const language = languageMap[activeElement.id] || "en";

        // Send a POST request to Flask backend
        const response = await fetch("/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: activeContent,
                language: language, // Use the mapped language code
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert("Error: " + errorData.error);
            return;
        }

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        if(audio)
        {
            audio.pause();
        }
		
        audio = new Audio(audioUrl);

        // Play the audio
        audio.play();
        // document.getElementById('btn-pause').disabled = false;
        // document.getElementById('btn-resume').disabled = true;
        playPauseButton.disabled = false; // Enable the play/pause button
        playPauseIcon.classList.remove('fa-play'); // Ensure icon shows 'Pause'
        playPauseIcon.classList.add('fa-pause');
    }
    catch (error) {
        console.error("Error:", error);
        alert("An error occurred while converting text to speech.");
    }
    audio.addEventListener('ended', () => {
        playPauseIcon.classList.remove('fa-pause'); // Switch icon to 'Play'
        playPauseIcon.classList.add('fa-play');
        // currentAudio = null; // Reset the currentAudio as playback is finished
    });
});

playPauseButton.addEventListener('click', () => {
    if (audio.paused) {
      audio.play(); // Resume audio
      playPauseIcon.classList.remove('fa-play'); // Switch icon to 'Pause'
      playPauseIcon.classList.add('fa-pause');
    } else {
      audio.pause(); // Pause audio
      playPauseIcon.classList.remove('fa-pause'); // Switch icon to 'Play'
      playPauseIcon.classList.add('fa-play');
    }
});

// document.getElementById('btn-pause').addEventListener('click', () => {
//     if (audio && !audio.paused) {
//         audio.pause();
//         document.getElementById('btn-pause').disabled = true;
//         document.getElementById('btn-resume').disabled = false;
//     }
// });

// document.getElementById('btn-resume').addEventListener('click', () => {
//     if (audio && audio.paused) {
//         audio.play();
//         document.getElementById('btn-pause').disabled = false;
//         document.getElementById('btn-resume').disabled = true;
//     }
// });