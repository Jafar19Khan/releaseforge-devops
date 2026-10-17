(() => {
  const toggle = document.querySelector(".menu-toggle");
  const mobileNav = document.querySelector("#mobile-nav");
  if (toggle && mobileNav) {
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      mobileNav.hidden = expanded;
      toggle.setAttribute("aria-label", expanded ? "Open navigation" : "Close navigation");
    });
    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        mobileNav.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation");
      });
    });
  }
  const copyButton = document.querySelector("#copy-command");
  const feedback = document.querySelector("#copy-feedback");
  if (copyButton && feedback) {
    copyButton.addEventListener("click", async () => {
      const command = "python tests/smoke_test.py http://127.0.0.1:8082/";
      try {
        await navigator.clipboard.writeText(command);
        feedback.textContent = "Command copied to clipboard.";
      } catch {
        feedback.textContent = "Copy is unavailable here. Select the command text and copy it manually.";
      }
    });
  }
})();
