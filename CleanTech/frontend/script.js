document.addEventListener('DOMContentLoaded', function() {
    // Show default environment video/image, hide AQI animation on load
    const animationVideo = document.getElementById('aqi-animation');
    const defaultBg = document.getElementById('default-bg');
    if (animationVideo && defaultBg) {
        animationVideo.style.display = "none";
        animationVideo.pause();
        animationVideo.src = "";
        defaultBg.style.display = "block";
    }

    // Get address, lat, lon from display section
    const address = document.getElementById('address').textContent.trim();
    const lat = document.getElementById('latitude').textContent.trim();
    const lon = document.getElementById('longitude').textContent.trim();

    // Fetch and display real-time AQI and pollutants from backend
    fetchAndDisplayRealtimeAQI(lat, lon);

    function fetchAndDisplayRealtimeAQI(lat, lon) {
        fetch(`http://127.0.0.1:5000/realtime-aqi?lat=${lat}&lon=${lon}`) // Adjust endpoint if needed
            .then(response => response.json())
            .then(data => {
                // Update AQI and message
                document.getElementById('realtime-aqi').textContent = data.predicted_aqi.toFixed(2);
                document.getElementById('realtime-message').textContent = data.message;

                // Update pollutant values
                document.getElementById('realtime-co').textContent = data.CO;
                document.getElementById('realtime-no').textContent = data.NO;
                document.getElementById('realtime-no2').textContent = data.NO2;
                document.getElementById('realtime-nox').textContent = data.NOx;
                document.getElementById('realtime-o3').textContent = data.O3;
                document.getElementById('realtime-so2').textContent = data.SO2;
                document.getElementById('realtime-pm25').textContent = data['PM2.5'];
                document.getElementById('realtime-pm10').textContent = data.PM10;
                document.getElementById('realtime-nh3').textContent = data.NH3;

                // Show the correct video based on AQI
                showAQIAnimation(data.predicted_aqi);
            })
            .catch(error => {
                document.getElementById('realtime-message').textContent = "Error fetching data";
            });
    }

    // Video logic: show looping video based on AQI
    function showAQIAnimation(aqi) {
        const animationVideo = document.getElementById('aqi-animation');
        const videoSource = document.getElementById('aqi-video-source');
        const defaultBg = document.getElementById('default-bg');

        let videoFile = "";
        if (aqi <= 50) {
            videoFile = "media/fresh-air.mp4";
        } else if (aqi <= 100) {
            videoFile = "media/walking.mp4";
        } else if (aqi <= 200) {
            videoFile = "media/mask.mp4";
        } else if (aqi <= 300) {
            videoFile = "media/pollution.mp4";
        } else {
            videoFile = "media/pollution1.mp4";
        }

        if (videoFile && animationVideo && videoSource && defaultBg) {
            videoSource.src = videoFile;
            animationVideo.load();
            animationVideo.style.display = "block";
            animationVideo.loop = true;
            animationVideo.play();
            defaultBg.style.display = "none";
        }
    }

    // Contact section toggle (unchanged)
    const contactLink = document.querySelector('a[href="#contact"]');
    const contactSection = document.getElementById('contact');
    if (contactLink && contactSection) {
        contactLink.addEventListener('click', function(e) {
            e.preventDefault();
            if (contactSection.style.display === "none" || contactSection.style.display === "") {
                contactSection.style.display = "block";
                contactSection.scrollIntoView({ behavior: "smooth" });
            } else {
                contactSection.style.display = "none";
            }
        });
    }
});