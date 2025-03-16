// Quiz App Animations and Interactions
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements on page load
    animateOnLoad();
    
    // Add hover effects to cards
    setupCardHoverEffects();
    
    // Setup quiz interactions
    setupQuizInteractions();
    
    // Setup smooth scrolling
    setupSmoothScrolling();
    
    // Setup navbar scroll effect
    setupNavbarScroll();
    
    // Setup hero section animations
    setupHeroAnimations();
    
    // Setup info section animations
    setupInfoSectionAnimations();
    
    // Fix for hero section padding on mobile
    adjustHeroSectionPadding();
    
    // Setup glass morphism effects
    setupGlassMorphism();
    
    // Setup footer animations
    setupFooterAnimations();
});

// Animate elements when page loads
function animateOnLoad() {
    // Animate header elements with staggered delay
    const headerElements = document.querySelectorAll('h1:not(.hero-title), .lead:not(.hero-subtitle), .card');
    headerElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 * index);
    });
    
    // Animate tables
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            
            setTimeout(() => {
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, 50 * index);
        });
    });
}

// Add hover effects to cards
function setupCardHoverEffects() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 6px 15px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Setup hero section animations
function setupHeroAnimations() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    const heroTitle = heroSection.querySelector('.hero-title');
    const heroSubtitle = heroSection.querySelector('.hero-subtitle');
    const heroButtons = heroSection.querySelectorAll('.hero-btn');
    
    if (heroTitle) {
        heroTitle.style.opacity = '0';
        heroTitle.style.transform = 'translateY(30px)';
        heroTitle.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            heroTitle.style.opacity = '1';
            heroTitle.style.transform = 'translateY(0)';
        }, 300);
    }
    
    if (heroSubtitle) {
        heroSubtitle.style.opacity = '0';
        heroSubtitle.style.transform = 'translateY(30px)';
        heroSubtitle.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            heroSubtitle.style.opacity = '1';
            heroSubtitle.style.transform = 'translateY(0)';
        }, 600);
    }
    
    heroButtons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(30px)';
        button.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 900 + (index * 200));
    });
    
    // Add parallax effect to hero section
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        if (scrollPosition < window.innerHeight) {
            heroSection.style.backgroundPosition = `50% ${scrollPosition * 0.4}px`;
        }
    });
}

// Fix for hero section padding on mobile
function adjustHeroSectionPadding() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    function updatePadding() {
        const navbarHeight = navbar.offsetHeight;
        heroSection.style.paddingTop = `${navbarHeight + 80}px`;
    }
    
    // Update on load
    updatePadding();
    
    // Update on resize
    window.addEventListener('resize', updatePadding);
}

// Setup glass morphism effects
function setupGlassMorphism() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Add glass effect to navbar
    function updateGlassEffect() {
        const scrollPosition = window.scrollY;
        const opacity = Math.min(0.1 + (scrollPosition / 500), 0.9);
        
        if (document.documentElement.getAttribute('data-theme') === 'dark') {
            navbar.style.backgroundColor = `rgba(0, 0, 0, ${opacity})`;
        } else {
            navbar.style.backgroundColor = `rgba(255, 255, 255, ${opacity})`;
        }
    }
    
    // Update on scroll
    window.addEventListener('scroll', updateGlassEffect);
    
    // Update on theme change
    document.addEventListener('themeChanged', updateGlassEffect);
    
    // Initial update
    updateGlassEffect();
}

// Setup info section animations
function setupInfoSectionAnimations() {
    const infoSections = document.querySelectorAll('.info-section');
    
    if (infoSections.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateInfoSection(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    infoSections.forEach(section => {
        observer.observe(section);
    });
    
    function animateInfoSection(section) {
        const title = section.querySelector('.section-title');
        const lead = section.querySelector('.lead');
        const cards = section.querySelectorAll('.card, .feature-item');
        
        if (title) {
            title.style.opacity = '0';
            title.style.transform = 'translateY(20px)';
            title.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                title.style.opacity = '1';
                title.style.transform = 'translateY(0)';
            }, 100);
        }
        
        if (lead) {
            lead.style.opacity = '0';
            lead.style.transform = 'translateY(20px)';
            lead.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                lead.style.opacity = '1';
                lead.style.transform = 'translateY(0)';
            }, 300);
        }
        
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 500 + (index * 100));
        });
    }
}

// Setup quiz interactions
function setupQuizInteractions() {
    // Highlight selected answer
    const radioInputs = document.querySelectorAll('.form-check-input[type="radio"]');
    
    radioInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Remove highlight from all options in this question
            const questionContainer = this.closest('.question-container');
            if (questionContainer) {
                const allLabels = questionContainer.querySelectorAll('.form-check-label');
                allLabels.forEach(label => {
                    label.classList.remove('text-primary');
                    label.style.fontWeight = 'normal';
                });
                
                // Highlight selected option
                const selectedLabel = this.nextElementSibling;
                if (selectedLabel) {
                    selectedLabel.classList.add('text-primary');
                    selectedLabel.style.fontWeight = 'bold';
                }
            }
        });
    });
    
    // Animate timer if present
    const timer = document.getElementById('timer');
    if (timer) {
        setInterval(() => {
            const currentTime = timer.textContent;
            const timeArray = currentTime.split(':');
            
            if (timeArray.length === 2) {
                const minutes = parseInt(timeArray[0]);
                const seconds = parseInt(timeArray[1]);
                
                // If less than 1 minute remaining, add pulse effect
                if (minutes === 0 && seconds < 60) {
                    timer.classList.add('text-danger');
                    timer.style.animation = 'pulse 0.8s infinite';
                }
            }
        }, 1000);
    }
    
    // Add progress animation for quiz submission
    const quizForm = document.querySelector('form[action*="submit-quiz"]');
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...';
                submitButton.disabled = true;
            }
        });
    }
}

// Setup smooth scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 70,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

// Setup navbar scroll effect
function setupNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
                navbar.style.padding = '0.5rem 1rem';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.padding = '1rem';
            }
        });
    }
}

// Add confetti effect for quiz results
function showConfetti() {
    const canvas = document.createElement('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1000';
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const confettiCount = 200;
    const confetti = [];
    
    for (let i = 0; i < confettiCount; i++) {
        confetti.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            size: Math.random() * 10 + 5,
            color: `hsl(${Math.random() * 360}, 100%, 70%)`,
            speed: Math.random() * 3 + 2
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        let stillFalling = false;
        
        confetti.forEach(particle => {
            ctx.fillStyle = particle.color;
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fill();
            
            particle.y += particle.speed;
            particle.x += Math.sin(particle.y / 30) * 2;
            
            if (particle.y < canvas.height + particle.size) {
                stillFalling = true;
            }
        });
        
        if (stillFalling) {
            requestAnimationFrame(animate);
        } else {
            canvas.remove();
        }
    }
    
    animate();
}

// Check if we're on a results page and show confetti
if (window.location.href.includes('quiz-result')) {
    const scoreElement = document.querySelector('.progress-bar');
    if (scoreElement) {
        const scoreText = scoreElement.textContent || '';
        const score = parseFloat(scoreText);
        
        if (score >= 70) {
            // Show confetti for good scores
            setTimeout(showConfetti, 500);
        }
    }
}

// Setup footer animations
function setupFooterAnimations() {
    const footer = document.querySelector('.footer');
    if (!footer) return;
    
    // Animate footer elements on scroll
    const footerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateFooterElements();
                footerObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    footerObserver.observe(footer);
    
    function animateFooterElements() {
        // Animate headings
        const headings = footer.querySelectorAll('h5');
        headings.forEach((heading, index) => {
            heading.style.opacity = '0';
            heading.style.transform = 'translateY(20px)';
            heading.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                heading.style.opacity = '1';
                heading.style.transform = 'translateY(0)';
            }, 100 * index);
        });
        
        // Animate lists
        const lists = footer.querySelectorAll('.col-lg-2, .col-lg-3, .col-lg-4');
        lists.forEach((list, index) => {
            list.style.opacity = '0';
            list.style.transform = 'translateY(20px)';
            list.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                list.style.opacity = '1';
                list.style.transform = 'translateY(0)';
            }, 300 + (100 * index));
        });
        
        // Animate social links with a bounce effect
        const socialLinks = footer.querySelectorAll('.social-links a');
        socialLinks.forEach((link, index) => {
            link.style.opacity = '0';
            link.style.transform = 'scale(0.5)';
            link.style.transition = 'opacity 0.5s ease, transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            
            setTimeout(() => {
                link.style.opacity = '1';
                link.style.transform = 'scale(1)';
            }, 600 + (100 * index));
        });
        
        // Animate footer bottom with a fade-in effect
        const footerBottom = footer.querySelector('.footer-bottom');
        if (footerBottom) {
            footerBottom.style.opacity = '0';
            footerBottom.style.transition = 'opacity 1s ease';
            
            setTimeout(() => {
                footerBottom.style.opacity = '1';
            }, 1000);
        }
    }
    
    // Add hover effects to social links
    const socialLinks = footer.querySelectorAll('.social-links a');
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) rotate(5deg)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotate(0)';
        });
    });
    
    // Add typing effect to developer name
    const developerLink = footer.querySelector('.developer-link');
    if (developerLink) {
        const originalText = developerLink.textContent;
        developerLink.textContent = '';
        
        setTimeout(() => {
            typeWriter(developerLink, originalText, 0, 100);
        }, 1500);
    }
    
    function typeWriter(element, text, index, speed) {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(() => typeWriter(element, text, index, speed), speed);
        }
    }
} 