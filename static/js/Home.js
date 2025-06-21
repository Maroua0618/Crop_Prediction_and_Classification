// Slideshow functionality
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");

// Auto slideshow timer
const slideInterval = setInterval(nextSlide, 3000);

// Function to change slide
function showSlide(n) {
  // Hide all slides
  slides.forEach((slide) => {
    slide.classList.remove("active");
  });

  // Remove active state from all dots
  dots.forEach((dot) => {
    dot.classList.remove("active");
  });

  // Set current slide and dot as active
  slides[n].classList.add("active");
  dots[n].classList.add("active");
  currentSlide = n;
}

// Next slide function
function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

// Previous slide function
function prevSlide() {
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(currentSlide);
}

// Add click event for dots
dots.forEach((dot, index) => {
  dot.addEventListener("click", () => {
    showSlide(index);
  });
});
