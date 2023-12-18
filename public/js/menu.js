document.addEventListener("DOMContentLoaded", (event) => {
  const menuTrigger = document.querySelector(".menu-trigger");
  const menu = document.querySelector(".menu");
  const breakpoint = 768; // This is the window width threshold, you can adjust this value

  function shouldMenuBeHidden() {
    return window.innerWidth <= breakpoint;
  }
  function updateMenuVisibility() {
    const shouldBeHidden = shouldMenuBeHidden();
    menuTrigger.classList.toggle("hidden", !shouldBeHidden);
    menu.classList.toggle("hidden", shouldBeHidden);
  }

  updateMenuVisibility();

  menuTrigger?.addEventListener("click", () => {
    menu?.classList.toggle("hidden");
  });

  window.addEventListener("resize", updateMenuVisibility);

  document.querySelector(".menu-trigger");
});
