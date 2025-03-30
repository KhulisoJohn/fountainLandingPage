const navbar = document.getElementById("navbar");
const containerEl = document.querySelector(".sub-cont");
const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navbarSupportedContent");

menuToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.contains("show");
    if (isOpen) {
        navMenu.classList.remove("show");
        menuToggle.innerHTML = '<span class="nav-icon open-menu">&#9776;</span>'; // Show open menu icon
    } else {
        navMenu.classList.add("show");
        menuToggle.innerHTML = '<span class="nav-icon close-menu">&times;</span>'; // Show close menu icon
    }
});

// Close menu when any nav link is clicked
document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        navMenu.classList.remove("show");
        menuToggle.innerHTML = '<span class="nav-icon open-menu">&#9776;</span>'; // Reset to open icon
    });
});

// Condition to check if page is scrolled more than 100vh
const handleScroll = () => {
    window.addEventListener("scroll", () => {
        if (scrollY > 640) {
            navbar.classList.add("scrolledNav");
        } else {
            navbar.classList.remove("scrolledNav");
        }
    });
};
handleScroll();

const purpose = [
    "A place of Worship",
    "A place of Transformation",
    "A place of Fellowship",
    "A place of Restoration",
    "A place of Deliverance",
    "A place of Inspiration and Growth"
];

let purposeIndex = 0;
let characterIndex = 0;

function updateIndex() {
    characterIndex++;
    containerEl.innerHTML = `<span class="fs-2"> ${purpose[purposeIndex].slice(0, characterIndex)} </span>`;
    
    if (characterIndex === purpose[purposeIndex].length) {
        purposeIndex++;
        characterIndex = 0;
    }
    
    if (purposeIndex === purpose.length) {
        purposeIndex = 0;
    }
    
    setTimeout(updateIndex, 200);
}
updateIndex();
