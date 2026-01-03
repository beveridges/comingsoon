// =====================================================
// FORM SUBMISSION WITH reCAPTCHA
// =====================================================
function initFormHandler() {
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
                // Replace form with thank you message, lock box size
                const lang = document.documentElement.lang || "en";
                const messages = {
                  "en": "Thank you for your interest!",
                  "es": "¡Gracias por tu interés!",
                  "de": "Vielen Dank für Ihr Interesse!"
                };
                
                const contentBox = form.closest(".content-box");
                
                // Lock content box dimensions to prevent resizing
                if (contentBox) {
                  const currentHeight = contentBox.offsetHeight;
                  const currentWidth = contentBox.offsetWidth;
                  const computedStyle = window.getComputedStyle(contentBox);
                  const currentPadding = computedStyle.padding;
                  const currentMaxWidth = computedStyle.maxWidth;
                  
                  // Lock ALL dimensions with inline styles
                  contentBox.style.setProperty("height", currentHeight + "px", "important");
                  contentBox.style.setProperty("min-height", currentHeight + "px", "important");
                  contentBox.style.setProperty("max-height", currentHeight + "px", "important");
                  contentBox.style.setProperty("width", currentWidth + "px", "important");
                  contentBox.style.setProperty("min-width", currentWidth + "px", "important");
                  contentBox.style.setProperty("max-width", currentMaxWidth, "important");
                  contentBox.style.setProperty("padding", currentPadding, "important");
                }
                
                // Keep form in layout but hide its contents and show thank you message instead
                const formHeight = form.offsetHeight;
                const formMarginTop = window.getComputedStyle(form).marginTop;
                
                // Hide form inputs/button
                const emailInput = form.querySelector('input[type="email"]');
                const submitBtn = form.querySelector('button[type="submit"]');
                if (emailInput) emailInput.style.display = 'none';
                if (submitBtn) submitBtn.style.display = 'none';
                
                form.style.height = formHeight + 'px';
                form.style.marginTop = formMarginTop;
                form.style.display = 'flex';
                form.style.alignItems = 'center';
                form.style.justifyContent = 'center';
                
                // Create and show thank you message inside the form
                const thankYouMessage = document.createElement('p');
                thankYouMessage.className = 'thank-you-message';
                thankYouMessage.textContent = messages[lang] || messages["en"];
                thankYouMessage.style.margin = '0';
                thankYouMessage.style.color = 'white';
                thankYouMessage.style.fontSize = '1.1em';
                thankYouMessage.style.fontWeight = '500';
                
                // Add message to form
                form.appendChild(thankYouMessage);
                
                // Hide response element if it exists
                if (responseElement) {
                  responseElement.style.display = 'none';
                }
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
}

// Initialize form handler on page load
document.addEventListener("DOMContentLoaded", function () {
  initFormHandler();
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
  
  // Create inline link for removal - use language-specific path
  // Since we're already in the language directory (en/, es/, de/), use relative path
  const textElement = document.getElementById("privacyModalText");
  textElement.innerHTML = message.text + 
    '<a href="remove.html" style="color: #1e90ff; text-decoration: none; border-bottom: 1px solid #1e90ff;">' + 
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

  // Only handle mobile - desktop video uses CSS + autoplay
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
    // Video element already has autoplay attribute, but ensure it plays
    // in case browser blocks autoplay
    if (video.paused) {
      video.play().catch(err => {
        // Autoplay blocked - will play when user interacts or when video is ready
        console.warn("Video autoplay blocked:", err);
      });
    }
    
    // Also try to play when video becomes ready (handles delayed autoplay)
    video.addEventListener('loadeddata', function() {
      if (video.paused) {
        video.play().catch(err => {
          console.warn("Video play failed:", err);
        });
      }
    }, { once: true });
  }
});


// =====================================================
// CONTINUOUS VIDEO ANIMATION - AJAX LANGUAGE SWITCHING
// Video continues playing uninterrupted when changing languages
// =====================================================
document.addEventListener("DOMContentLoaded", function() {
  const langLinks = document.querySelectorAll('.lang-link');
  
  // Initialize language switcher on page load
  function initLanguageSwitcher() {
    langLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        // Don't do anything if clicking the active language
        if (link.classList.contains('active')) {
          e.preventDefault();
          return;
        }
        
        e.preventDefault();
        const targetUrl = link.getAttribute('href');
        
        // Show loading state (optional - you can remove this if not needed)
        link.style.opacity = '0.6';
        link.style.pointerEvents = 'none';
        
        // Fetch the new page
        fetch(targetUrl)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.text();
          })
          .then(html => {
            // Create a temporary DOM to extract content
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Update the content box
            const newContentBox = doc.querySelector('.content-box');
            const currentContentBox = document.querySelector('.content-box');
            if (newContentBox && currentContentBox) {
              // Preserve any locked dimensions if form was submitted
              const currentStyles = window.getComputedStyle(currentContentBox);
              const hasLockedDimensions = currentContentBox.style.height || 
                                        currentContentBox.style.minHeight === currentContentBox.style.maxHeight;
              
              // Update content
              currentContentBox.innerHTML = newContentBox.innerHTML;
              
              // Re-apply locked dimensions if they existed
              if (hasLockedDimensions) {
                currentContentBox.style.setProperty("height", currentStyles.height, "important");
                currentContentBox.style.setProperty("min-height", currentStyles.minHeight, "important");
                currentContentBox.style.setProperty("max-height", currentStyles.maxHeight, "important");
                currentContentBox.style.setProperty("width", currentStyles.width, "important");
                currentContentBox.style.setProperty("min-width", currentStyles.minWidth, "important");
                currentContentBox.style.setProperty("max-width", currentStyles.maxWidth, "important");
                currentContentBox.style.setProperty("padding", currentStyles.padding, "important");
              } else {
                // Reset dimensions if no form was submitted
                currentContentBox.style.removeProperty("height");
                currentContentBox.style.removeProperty("min-height");
                currentContentBox.style.removeProperty("max-height");
                currentContentBox.style.removeProperty("width");
                currentContentBox.style.removeProperty("min-width");
                currentContentBox.style.removeProperty("max-width");
                currentContentBox.style.removeProperty("padding");
              }
              
              // Update content-box class (for German wider box)
              currentContentBox.className = newContentBox.className;
            }
            
            // Update language switcher active state
            langLinks.forEach(l => {
              l.classList.remove('active');
              l.style.opacity = '';
              l.style.pointerEvents = '';
            });
            link.classList.add('active');
            
            // Update document lang attribute
            document.documentElement.lang = doc.documentElement.lang || 'en';
            
            // Update page title
            document.title = doc.querySelector('title')?.textContent || document.title;
            
            // Update meta description if needed
            const metaDesc = doc.querySelector('meta[name="description"]');
            if (metaDesc) {
              let currentMetaDesc = document.querySelector('meta[name="description"]');
              if (currentMetaDesc) {
                currentMetaDesc.setAttribute('content', metaDesc.getAttribute('content'));
              }
            }
            
            // Update URL without reload
            window.history.pushState({}, '', targetUrl);
            
            // Re-initialize form event listener after content swap
            // (The form element was replaced with new HTML, so we need to re-attach the handler)
            initFormHandler();
            
            // Video continues playing - no interruption! 🎉
          })
          .catch(err => {
            console.error('Error loading language page:', err);
            // Fallback to normal navigation if AJAX fails
            window.location.href = targetUrl;
          });
      });
    });
  }
  
  // Initialize language switcher
  initLanguageSwitcher();
  
  // Handle browser back/forward buttons
  window.addEventListener('popstate', function(e) {
    // For back/forward navigation, do a full reload to ensure everything works correctly
    // This is simpler and more reliable than trying to restore state
    window.location.reload();
  });
});