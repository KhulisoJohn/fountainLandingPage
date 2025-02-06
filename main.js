const navbar = document.getElementById("navbar");

// Condition to check if page is scrolled more than 100vh
const handleScroll = () => {
    window.addEventListener("scroll", () => {
        if (scrollY > 640) {
          navbar.classList.add("scrolledNav");
        }else{
          navbar.classList.remove("scrolledNav");
        }
      });
};
handleScroll();  