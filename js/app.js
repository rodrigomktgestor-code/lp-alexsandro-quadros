"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initApp();
});

function initApp() {
    setupHeader();
    setupMobileMenu();
    setupWhatsAppLinks();
    updateHeroStats();
    
    // Initialize properties list and filters if on index page
    if (document.getElementById('catalogo')) {
        initFilters();
    }
    
    // Setup scroll reveal animation
    setTimeout(initScrollReveal, 100);
}

function setupHeader() {
    const header = document.getElementById("main-header");
    if (!header) return;

    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("header--scrolled");
        } else {
            header.classList.remove("header--scrolled");
        }
    }, { passive: true });
}

function setupMobileMenu() {
    const toggle = document.getElementById("menu-toggle");
    const nav = document.getElementById("main-nav");
    
    if (!toggle || !nav) return;

    const closeMenu = () => {
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("active");
        document.body.classList.remove("menu-open");
    };

    toggle.addEventListener("click", () => {
        const isExpanded = toggle.getAttribute("aria-expanded") === "true";
        toggle.classList.toggle("active");
        toggle.setAttribute("aria-expanded", !isExpanded);
        nav.classList.toggle("active");
        document.body.classList.toggle("menu-open");
    });

    // Close on escape
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && nav.classList.contains("active")) {
            closeMenu();
        }
    });

    // Close on click outside
    document.addEventListener("click", (e) => {
        if (nav.classList.contains("active") && !nav.contains(e.target) && !toggle.contains(e.target)) {
            closeMenu();
        }
    });

    // Close on link click
    nav.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeMenu);
    });
}

function setupWhatsAppLinks() {
    const waLinks = document.querySelectorAll(".btn-whatsapp");
    const waUrl = getWhatsAppLink();
    
    waLinks.forEach(link => {
        link.href = waUrl;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
    });
}

function updateHeroStats() {
    const statsContainer = document.getElementById("hero-stats");
    if (!statsContainer) return;

    const totalProps = properties.length;
    const cities = getUniqueValues(properties, 'city').length;
    
    let types = getUniqueValues(properties, 'propertyTypes');
    if (types.length > 3) {
        types = types.slice(0, 3);
    }
    const typesStr = types.join(", ");

    statsContainer.innerHTML = `
        <span><strong>${totalProps}</strong> empreendimentos</span> &bull; 
        <span><strong>${cities}</strong> cidades</span> &bull; 
        <span>${typesStr}</span>
    `;
}

function renderProperties(propsList) {
    const grid = document.getElementById("properties-grid");
    const emptyState = document.getElementById("empty-state");
    const resultsCount = document.getElementById("results-count");
    
    if (!grid) return;

    // Update count
    if (resultsCount) {
        resultsCount.textContent = `${propsList.length} ${propsList.length === 1 ? 'empreendimento encontrado' : 'empreendimentos encontrados'}`;
    }

    grid.innerHTML = "";

    if (propsList.length === 0) {
        grid.style.display = "none";
        emptyState.style.display = "block";
        return;
    }

    grid.style.display = "grid";
    emptyState.style.display = "none";

    const fragment = document.createDocumentFragment();

    propsList.forEach(prop => {
        const card = document.createElement("a");
        card.href = `empreendimento.html?imovel=${prop.slug}`;
        card.className = "property-card reveal";
        
        const locString = formatPropertyLocation(prop);
        const typesStr = (prop.propertyTypes || []).join(" e ");
        
        let attrsHTML = "";
        
        if (typesStr) {
            attrsHTML += `<div class="attr-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg> ${typesStr}</div>`;
        }

        if (prop.bedrooms && prop.bedrooms.length > 0) {
            const minB = Math.min(...prop.bedrooms);
            const maxB = Math.max(...prop.bedrooms);
            const bedStr = minB === maxB ? `${minB} dormitórios` : `${minB} a ${maxB} dormitórios`;
            attrsHTML += `<div class="attr-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 4v16M2 8h20M22 4v16M2 12h20M2 16h20"></path></svg> ${bedStr}</div>`;
        }

        const areaStr = formatArea(prop.areaMin, prop.areaMax);
        if (areaStr) {
            attrsHTML += `<div class="attr-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg> ${areaStr}</div>`;
        }

        const badgeHTML = prop.propertyTypes && prop.propertyTypes.length > 0 
            ? `<div class="property-badge">${prop.propertyTypes[0]}</div>` 
            : "";

        let imgStyle = "";
        if (prop.slug === "terra-golden-resort") {
            imgStyle = ' style="object-position: top;"';
        } else if (prop.slug === "viva-serenita") {
            imgStyle = ' style="object-position: bottom;"';
        }

        card.innerHTML = `
            <div class="property-image">
                ${badgeHTML}
                <img src="${prop.coverImage}" alt="${prop.name}" loading="lazy"${imgStyle}>
            </div>
            <div class="property-content">
                <div class="property-location">${locString}</div>
                <h3 class="property-title">${prop.name}</h3>
                <div class="property-attributes">
                    ${attrsHTML}
                </div>
                <div class="property-footer">
                    <span class="card-link">Ver detalhes <svg class="card-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span>
                </div>
            </div>
        `;
        
        fragment.appendChild(card);
    });

    grid.appendChild(fragment);
    initScrollReveal(); // re-init on new elements
}

function updateRegions() {
    const regionsGrid = document.getElementById("regions-grid");
    if (!regionsGrid) return;

    const cities = getUniqueValues(properties, 'city');
    const fragment = document.createDocumentFragment();

    cities.forEach(city => {
        const count = properties.filter(p => p.city === city).length;
        
        const card = document.createElement("div");
        card.className = "region-card reveal";
        card.innerHTML = `
            <h3 class="region-name">${city}</h3>
            <span class="region-count">${count} ${count === 1 ? 'empreendimento' : 'empreendimentos'}</span>
        `;
        
        card.addEventListener('click', () => {
            // Apply location filter and scroll
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            const chipLoc = document.querySelector(`.chip[data-filter-value="${city}"]`);
            if (chipLoc) chipLoc.classList.add('active');

            propertyState.filters = { location: city, type: 'all', bedrooms: 'all', text: '' };
            applyFilters();
            
            document.getElementById('catalogo').scrollIntoView({ behavior: 'smooth' });
        });

        fragment.appendChild(card);
    });

    regionsGrid.appendChild(fragment);
}
