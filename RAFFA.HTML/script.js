// Smooth muncul saat halaman dibuka
window.addEventListener("load", () => {
    document.body.style.opacity = "1";
});

// Efek mengetik
const text = "Web Developer & Programmer";
const typing = document.querySelector(".hero-text h2");

typing.textContent = "";

let i = 0;

function typeWriter() {
    if (i < text.length) {
        typing.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 80);
    }
}

typeWriter();

// Efek navbar saat discroll
const nav = document.querySelector("nav");

window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
        nav.style.background = "rgba(5,10,25,.95)";
        nav.style.boxShadow = "0 5px 20px rgba(0,0,0,.3)";
    } else {
        nav.style.background = "rgba(7,17,31,.8)";
        nav.style.boxShadow = "none";
    }
});

// Efek hover card
const cards = document.querySelectorAll(".card");

cards.forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-10px) scale(1.03)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0) scale(1)";
    });
});

body{
    opacity:0;
    transition:1s;
}