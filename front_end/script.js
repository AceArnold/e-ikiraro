const services = [
    {
        id: 1,
        title: "Apply for National ID",
        icon: "🪪",
        description: "Buundi National Identity Card",
        page: "national-id.html"
    },
    {
        id: 2,
        title: "Apply for Driver's License",
        icon: "🚗",
        description: "Driver's License Application",
        page: "drivers-license.html"
    },
    {
        id: 3,
        title: "Apply for Passport",
        icon: "✈️",
        description: "Passport Application",
        page: "passport.html"
    }
];
document.addEventListener('DOMContentLoaded', function() {
    setCurrentYear();
    renderServices();
    setupEventListeners();
});
function setCurrentYear() {
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.textContent = currentYear;
    }
}

function renderServices() {
    const servicesGrid = document.getElementById('servicesGrid');
    
    services.forEach(service => {
        const serviceCard = createServiceCard(service);
        servicesGrid.appendChild(serviceCard);
    });
}
function createServiceCard(service) {
    const card = document.createElement('div');
    card.className = 'service-card';
    card.setAttribute('data-service-id', service.id);
    
    card.innerHTML = `
        <h4 class="service-title">${service.title}</h4>
        <div class="service-icon">
            <span class="service-icon-placeholder">${service.icon}</span>
        </div>
    `;
    card.addEventListener('click', () => handleServiceClick(service));
    
    return card;
}

function handleServiceClick(service) {
    console.log(`Service clicked: ${service.title}`);
    window.location.href = service.page;
}

function setupEventListeners() {
    const authButton = document.getElementById('authButton');
    authButton.addEventListener('click', handleAuthClick);

    document.addEventListener('keydown', handleKeyboardNavigation);
}

function handleAuthClick() {
    console.log('Auth button clicked');
   alert('Are you sure you want to logout?\n\n(This feature is currently under development)');

}

function handleKeyboardNavigation(event) {
    const serviceCards = document.querySelectorAll('.service-card');
    const focusedElement = document.activeElement;

    let currentIndex = -1;
    serviceCards.forEach((card, index) => {
        if (card === focusedElement) {
            currentIndex = index;
        }
    });

    if (currentIndex !== -1) {
        switch(event.key) {
            case 'ArrowRight':
                event.preventDefault();
                if (currentIndex < serviceCards.length - 1) {
                    serviceCards[currentIndex + 1].focus();
                }
                break;
            case 'ArrowLeft':
                event.preventDefault();
                if (currentIndex > 0) {
                    serviceCards[currentIndex - 1].focus();
                }
                break;
            case 'ArrowDown':
                event.preventDefault();
                if (currentIndex + 3 < serviceCards.length) {
                    serviceCards[currentIndex + 3].focus();
                }
                break;
            case 'ArrowUp':
                event.preventDefault();
                if (currentIndex - 3 >= 0) {
                    serviceCards[currentIndex - 3].focus();
                }
                break;
            case 'Enter':
            case ' ':
                event.preventDefault();
                focusedElement.click();
                break;
        }
    }
}

function makeCardsFocusable() {
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
    });
}

setTimeout(makeCardsFocusable, 0);

function filterServices(searchTerm) {
    const serviceCards = document.querySelectorAll('.service-card');
    const term = searchTerm.toLowerCase();
    
    serviceCards.forEach(card => {
        const title = card.querySelector('.service-title').textContent.toLowerCase();
        if (title.includes(term)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

window.eIkiraro = {
    filterServices,
    services
};

