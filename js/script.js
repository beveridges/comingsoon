// =====================================================
// FORM SUBMISSION WITH reCAPTCHA
// =====================================================
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("notifyForm");
  const responseElement = document.getElementById("response");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const submitButton = form.querySelector("button[type='submit']");
    
    // Disable form during submission
    form.style.pointerEvents = "none";
    submitButton.disabled = true;
    submitButton.style.opacity = "0.6";

    grecaptcha.ready(function () {
      grecaptcha.execute("6Ld6kOMrAAAAAGdH-HwPfJFzZqzUOXZ9TKCIS9r1", { action: "submit" })
        .then(function (token) {
          fetch("../save_email.php", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `email=${encodeURIComponent(email)}&recaptcha_token=${token}`,
          })
            .then(res => res.text())
            .then(text => {
              // Check if response indicates success
              const isSuccess = text.toLowerCase().includes("success") || 
                               text.toLowerCase().includes("gracias") || 
                               text.toLowerCase().includes("vielen dank") ||
                               text.toLowerCase().includes("thank you") ||
                               !text.toLowerCase().includes("error");
              
              if (isSuccess) {
                // Simple success message - no animation
                const lang = document.documentElement.lang || "en";
                const messages = {
                  "en": "Thank you! We will notify you soon.",
                  "es": "¡Gracias! Te notificaremos pronto.",
                  "de": "Vielen Dank! Wir werden Sie bald benachrichtigen."
                };
                responseElement.textContent = messages[lang] || messages["en"];
                responseElement.style.color = "#4ade80";
                form.reset();
              } else {
                responseElement.textContent = text;
                responseElement.style.color = "#ff6b6b";
                form.style.pointerEvents = "auto";
                submitButton.disabled = false;
                submitButton.style.opacity = "1";
              }
            })
            .catch(() => {
              responseElement.textContent = "Error sending request.";
              responseElement.style.color = "#ff6b6b";
              form.style.pointerEvents = "auto";
              submitButton.disabled = false;
              submitButton.style.opacity = "1";
            });
        });
    });
  });
});


// Show privacy modal
function showPrivacyModal() {
  const lang = document.documentElement.lang || "en";
  const messages = {
    "en": {
      title: "Privacy Statement",
      text: "We'll only use your email to notify you when we launch. We won't share it with anyone. You can ",
      removalLink: "request removal",
      textAfter: " from our list at any time."
    },
    "es": {
      title: "Declaración de Privacidad",
      text: "Solo usaremos tu correo para notificarte cuando lancemos. No lo compartiremos con nadie. Puedes ",
      removalLink: "solicitar la eliminación",
      textAfter: " de nuestra lista en cualquier momento."
    },
    "de": {
      title: "Datenschutzerklärung",
      text: "Wir verwenden Ihre E-Mail nur, um Sie über den Start zu informieren. Wir geben sie nicht weiter. Sie können jederzeit die ",
      removalLink: "Entfernung anfordern",
      textAfter: " von unserer Liste."
    }
  };
  
  const message = messages[lang] || messages["en"];
  
  // Create or get modal
  let modal = document.getElementById("privacyModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "privacyModal";
    modal.className = "privacy-modal";
    modal.innerHTML = `
      <div class="privacy-modal-content">
        <button class="privacy-modal-close" onclick="closePrivacyModal()">&times;</button>
        <h3 id="privacyModalTitle"></h3>
        <p id="privacyModalText"></p>
      </div>
    `;
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener("click", function(e) {
      if (e.target === modal) {
        closePrivacyModal();
      }
    });
    
    // Close on Escape key
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && modal.classList.contains("active")) {
        closePrivacyModal();
      }
    });
  }
  
  // Set content
  document.getElementById("privacyModalTitle").textContent = message.title;
  
  // Create inline link for removal
  const textElement = document.getElementById("privacyModalText");
  textElement.innerHTML = message.text + 
    '<a href="../remove.html" style="color: #1e90ff; text-decoration: none; border-bottom: 1px solid #1e90ff;">' + 
    message.removalLink + 
    '</a>' + 
    message.textAfter;
  
  // Show modal
  modal.classList.add("active");
}

// Close privacy modal
function closePrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (modal) {
    modal.classList.remove("active");
  }
}


// =====================================================
// RESPONSIVE VIDEO BEHAVIOR — HORIZONTAL FOCAL CENTER
// =====================================================
document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("bg-video");
  if (!video) return;

  const isMobile = window.matchMedia("(max-width: 1024px)").matches;

  if (isMobile) {
    video.pause();
    video.removeAttribute("loop");
    video.setAttribute("preload", "auto");
    video.setAttribute("playsinline", "");

    // === Mobile Clips (rotating sequence) ===
    const clips = [
      { src: "../video/A.webm", centerX: 40 },
      { src: "../video/B.webm", centerX: 55 },
      { src: "../video/C.webm", centerX: 50 },
      { src: "../video/D.webm", centerX: 70 },
    ];

    let currentIndex = 0;
    let nextVideo = null;

    // --- Apply horizontal centering ---
    function setFocalCenter(percentX) {
      video.style.position = "fixed";
      video.style.top = "0";
      video.style.left = "0";
      video.style.width = "100vw";
      video.style.height = "100vh";
      video.style.objectFit = "cover";
      video.style.objectPosition = `${percentX}% center`;
    }

    // --- Preload next video for seamless transition ---
    function preloadNextVideo(index) {
      const nextIndex = (index + 1) % clips.length;
      const nextClip = clips[nextIndex];
      
      if (!nextVideo) {
        nextVideo = document.createElement('video');
        nextVideo.setAttribute('preload', 'auto');
        nextVideo.setAttribute('playsinline', '');
        nextVideo.setAttribute('muted', '');
        nextVideo.style.display = 'none';
        document.body.appendChild(nextVideo);
      }
      
      nextVideo.innerHTML = `<source src="${nextClip.src}" type="video/webm">`;
      nextVideo.load();
    }

    // --- Load and play clip with seamless transition ---
    function playClip(index) {
      const clip = clips[index];
      
      // Preload next video immediately
      preloadNextVideo(index);
      
      // Remove old event listeners to prevent conflicts
      video.oncanplay = null;
      video.onended = null;
      video.onloadedmetadata = null;
      
      // Set new source
      video.innerHTML = `<source src="${clip.src}" type="video/webm">`;
      
      // Set styling before load to prevent grey flash
      setFocalCenter(clip.centerX);
      video.style.backgroundColor = '#000';
      
      // Load video
      video.load();
      
      // Play as soon as enough data is loaded
      video.oncanplaythrough = () => {
        setFocalCenter(clip.centerX);
        video.play().catch(err => console.warn("Playback failed:", err));
      };
      
      // Fallback if canplaythrough doesn't fire
      video.onloadeddata = () => {
        if (video.readyState >= 3) {
          setFocalCenter(clip.centerX);
          video.play().catch(err => console.warn("Playback failed:", err));
        }
      };

      video.onended = () => {
        currentIndex = (currentIndex + 1) % clips.length;
        // Next video should be preloaded, play it instantly
        playClip(currentIndex);
      };
    }

    // Maintain centering on resize/orientation change
    window.addEventListener("resize", () => {
      const clip = clips[currentIndex];
      setFocalCenter(clip.centerX);
    });

    playClip(currentIndex);

  } else {
    // === Desktop ===
    video.style.objectFit = "cover";
    video.style.position = "fixed";
    video.style.top = "0";
    video.style.left = "0";
    video.style.width = "100vw";
    video.style.height = "100vh";
    video.style.objectPosition = "center center";
  }
});
