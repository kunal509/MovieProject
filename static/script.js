// ==========================================
// 1. Real-Time Search Filter
// ==========================================
const searchInput = document.querySelector('.search-bar input');
const movieCards = document.querySelectorAll('.movie-card');

searchInput.addEventListener('input', function(event) {
    const searchQuery = event.target.value.toLowerCase();

    movieCards.forEach(function(card) {
        const title = card.querySelector('h3').textContent.toLowerCase();
        if (title.includes(searchQuery)) {
            card.style.display = 'block'; 
        } else {
            card.style.display = 'none'; 
        }
    });
});

// ==========================================
// 2. Professional Video Player Logic (Plyr)
// ==========================================
const player = new Plyr('#moviePlayer');
const videoModal = document.getElementById('videoModal');
const closeBtn = document.getElementById('closeBtn');

// Click a movie poster to play
movieCards.forEach(function(card) {
    card.addEventListener('click', function() {
        const videoUrl = card.getAttribute('data-video');
        
        // Feed the video to Plyr
        player.source = {
            type: 'video',
            sources: [
                {
                    src: videoUrl,
                    type: 'video/mp4',
                },
            ],
        };
        
        videoModal.style.display = 'flex'; // Open modal
        
        // Slight delay to ensure modal is open before playing
        setTimeout(() => {
            player.play();
        }, 100);
    });
});

// Click the X to close and stop video
closeBtn.addEventListener('click', function() {
    videoModal.style.display = 'none'; 
    player.stop(); 
});