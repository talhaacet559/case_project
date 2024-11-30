function openForm() {
    document.getElementById("Logout").classList.add("active");
    document.getElementById("BackgroundOverlay").classList.add("active");
    document.querySelector(".main-content").classList.add("blur-background");
}

function closeForm() {
    document.getElementById("Logout").classList.remove("active");
    document.getElementById("BackgroundOverlay").classList.remove("active");
    document.querySelector(".main-content").classList.remove("blur-background");
}