"use strict";

document.addEventListener("DOMContentLoaded", () => {
    // Header scrolled logic is similar to index
    const header = document.getElementById("main-header");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("header--scrolled");
        } else {
            header.classList.remove("header--scrolled");
        }
    }, { passive: true });

    // Mobile Menu
    const toggle = document.getElementById("menu-toggle");
    const nav = document.getElementById("main-nav");
    
    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            const isExpanded = toggle.getAttribute("aria-expanded") === "true";
            toggle.classList.toggle("active");
            toggle.setAttribute("aria-expanded", !isExpanded);
            nav.classList.toggle("active");
            document.body.classList.toggle("menu-open");
        });
    }

    loadPropertyData();
});

function loadPropertyData() {
    const urlParams = new URLSearchParams(window.location.search);
    const slug = urlParams.get('imovel');
    
    const prop = properties.find(p => p.slug === slug);
    const mainEl = document.getElementById('property-main');

    if (!prop) {
        document.title = "Empreendimento não encontrado | AXA Imóveis Floripa";
        mainEl.innerHTML = `
            <div class="container not-found-state">
                <h2>Empreendimento não encontrado.</h2>
                <p>O imóvel que você procura não está disponível ou o link é inválido.</p>
                <a href="index.html#catalogo" class="btn btn-primary" style="margin-top: 24px;">Ver todos os empreendimentos</a>
            </div>
        `;
        return;
    }

    // Set page title
    document.title = `${prop.name} em ${prop.city} | AXA Imóveis Floripa`;
    
    // Prepare WhatsApp Links
    const waUrl = getWhatsAppLink(prop.name);
    document.querySelectorAll(".btn-whatsapp").forEach(link => {
        link.href = waUrl;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
    });

    // Populate data
    renderPropertyPage(prop, mainEl);
    
    // Update footer disclaimer if exists
    if (prop.legalDisclaimer) {
        const discEl = document.getElementById('footer-disclaimer');
        if (discEl) discEl.textContent = prop.legalDisclaimer;
    }

    // Use explicit gallery array if defined, otherwise fall back to auto-generating paths
    let imagePaths = [];
    if (prop.gallery && prop.gallery.length > 0) {
        imagePaths = prop.gallery.map(p => p.replace(/\?v=\d+$/, ''));
    } else {
        for (let i = 0; i < 8; i++) {
            imagePaths.push(`assets/images/properties/${prop.slug}/image_${i}.webp`);
        }
    }
    
    // Initialize Gallery
    setTimeout(() => {
        initGallery(imagePaths);
        initScrollReveal();
    }, 100);
}

function renderPropertyPage(prop, container) {
    const locString = formatPropertyLocation(prop);
    const typesStr = (prop.propertyTypes || []).join(" e ");
    
    // Generate Stats
    let statsHTML = '';
    const areaStr = formatArea(prop.areaMin, prop.areaMax);
    if (areaStr) statsHTML += `<div class="stat-box"><span class="stat-label">Área</span><span class="stat-value">${areaStr}</span></div>`;
    
    if (prop.bedrooms && prop.bedrooms.length > 0) {
        const bMin = Math.min(...prop.bedrooms);
        const bMax = Math.max(...prop.bedrooms);
        const bStr = bMin === bMax ? `${bMin}` : `${bMin} a ${bMax}`;
        statsHTML += `<div class="stat-box"><span class="stat-label">Dormitórios</span><span class="stat-value">${bStr}</span></div>`;
    }
    
    if (prop.suites && prop.suites.length > 0) {
        const sMax = Math.max(...prop.suites);
        statsHTML += `<div class="stat-box"><span class="stat-label">Suítes</span><span class="stat-value">Até ${sMax}</span></div>`;
    }
    
    statsHTML += `<div class="stat-box"><span class="stat-label">Tipo</span><span class="stat-value">${typesStr}</span></div>`;

    // Generate Amenities
    let amenitiesHTML = '';
    if (prop.amenities && prop.amenities.length > 0) {
        amenitiesHTML = `
            <section class="prop-section reveal">
                <div class="container">
                    <h3>Infraestrutura e Lazer</h3>
                    <ul class="amenities-list">
                        ${prop.amenities.map(a => `<li><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="amenity-icon"><polyline points="20 6 9 17 4 12"></polyline></svg> ${a}</li>`).join('')}
                    </ul>
                </div>
            </section>
        `;
    }

    // Generate Typologies
    let typologiesHTML = '';
    if (prop.typologies && prop.typologies.length > 0) {
        typologiesHTML = `
            <section class="prop-section prop-section--light reveal">
                <div class="container">
                    <h3>Tipologias Disponíveis</h3>
                    <ul class="typology-list">
                        ${prop.typologies.map(t => `<li>${t}</li>`).join('')}
                    </ul>
                </div>
            </section>
        `;
    }

    // Generate Nearby
    let nearbyHTML = '';
    if (prop.nearby && prop.nearby.length > 0) {
        nearbyHTML = `
            <section class="prop-section reveal">
                <div class="container">
                    <h3>Localização que faz diferença</h3>
                    <p class="prop-address">${prop.address ? prop.address + ' - ' : ''}${locString}</p>
                    <ul class="nearby-list">
                        ${prop.nearby.map(n => `<li>${n}</li>`).join('')}
                    </ul>
                </div>
            </section>
        `;
    }

    // Gallery Section — use explicit gallery array or fall back to auto-paths
    let galleryImages = [];
    if (prop.gallery && prop.gallery.length > 0) {
        galleryImages = prop.gallery.map(p => p.replace(/\?v=\d+$/, ''));
    } else {
        for (let i = 0; i < 5; i++) {
            galleryImages.push(`assets/images/properties/${prop.slug}/image_${i}.webp`);
        }
    }
    const [g0, g1, g2, g3, g4] = galleryImages;
    let galleryHTML = `
        <section class="prop-gallery reveal">
            <div class="container">
                <div class="gallery-grid">
                    ${g0 ? `<img src="${g0}" class="gallery-thumb" alt="${prop.name} - Imagem 1" onerror="this.style.display='none'">` : ''}
                    ${g1 ? `<img src="${g1}" class="gallery-thumb" alt="${prop.name} - Imagem 2" onerror="this.style.display='none'">` : ''}
                    ${g2 ? `<img src="${g2}" class="gallery-thumb" alt="${prop.name} - Imagem 3" onerror="this.style.display='none'">` : ''}
                    ${g3 ? `<img src="${g3}" class="gallery-thumb" alt="${prop.name} - Imagem 4" onerror="this.style.display='none'">` : ''}
                    <div class="gallery-more gallery-thumb">
                        ${g4 ? `<img src="${g4}" alt="${prop.name} - Ver mais" onerror="this.style.display='none'">` : ''}
                        <span>Ver Galeria</span>
                    </div>
                </div>
            </div>
        </section>
    `;

    container.innerHTML = `
        <section class="prop-hero reveal">
            <img src="${prop.coverImage}" alt="${prop.name}" class="prop-hero-bg">
            <div class="prop-hero-overlay"></div>
            <div class="container prop-hero-content">
                <div class="prop-hero-meta">${locString}</div>
                <h1 class="prop-hero-title">${prop.name}</h1>
                <p class="prop-hero-headline">${prop.headline}</p>
                <div class="prop-hero-actions">
                    <a href="${getWhatsAppLink(prop.name)}" target="_blank" class="btn btn-primary btn-whatsapp">Tenho interesse</a>
                </div>
            </div>
        </section>

        ${galleryHTML}

        <section class="prop-section reveal">
            <div class="container">
                <div class="prop-about-grid">
                    <div class="prop-desc">
                        <h3>Sobre o empreendimento</h3>
                        <p>${prop.description}</p>
                    </div>
                    <div class="prop-stats">
                        ${statsHTML}
                    </div>
                </div>
            </div>
        </section>

        ${amenitiesHTML}
        ${typologiesHTML}
        ${nearbyHTML}

        <section class="cta-comercial reveal">
            <div class="container">
                <div class="cta-content">
                    <h2>Gostou deste empreendimento?</h2>
                    <p>Entre em contato para consultar valores, condições de pagamento e unidades disponíveis.</p>
                    <a href="${getWhatsAppLink(prop.name)}" target="_blank" class="btn btn-primary btn-whatsapp">Conversar pelo WhatsApp</a>
                </div>
            </div>
        </section>
    `;
}
