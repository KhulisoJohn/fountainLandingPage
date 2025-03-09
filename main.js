const navbar = document.getElementById("navbar");
const containerEl = document.querySelector(".sub-cont");

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

const purpose = [
   "A place of Worship",
   "A place of Transformation",
   "A place of Fellowship",
   "A place of Restoration",
   "A place of Deliverance",
   "A place of Inspiration and Grow"
   
  ];

  let purposeIndex = 0;

  let characterIndex = 0;

  updateIndex();

  function updateIndex(){
    characterIndex++;
    containerEl.innerHTML = `
  <span class="fs-2"> ${purpose[purposeIndex].slice(0,characterIndex)} </span>
`;


if(characterIndex === purpose[purposeIndex].length){
  purposeIndex++;
  characterIndex = 0;
}

if(purposeIndex === purpose.length){
  purposeIndex = 0;
}
setTimeout(updateIndex,400);
  }

