const statusText = document.querySelector("#status");
const actionButton = document.querySelector("#action");

actionButton.addEventListener("click", () => {
  statusText.textContent = "Objetivo: practicar push, pull, log y resolucion de conflictos.";
});
