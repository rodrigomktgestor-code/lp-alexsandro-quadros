"use strict";

/**
 * Normaliza uma string removendo acentos e convertendo para minúsculas
 */
function normalizeString(str) {
    if (!str) return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

/**
 * Gera o link do WhatsApp com a mensagem pré-definida
 */
function getWhatsAppLink(propertyName = null) {
    let message = "Olá, Alexsandro! Acessei o site da AXA Imóveis Floripa e gostaria de conhecer os empreendimentos disponíveis.";
    
    if (propertyName) {
        message = `Olá, Alexsandro! Vi o empreendimento ${propertyName} no site da AXA Imóveis Floripa e gostaria de receber mais informações.`;
    }

    return `https://wa.me/${siteConfig.whatsapp}?text=${encodeURIComponent(message)}`;
}

/**
 * Formata a localização (Bairro, Cidade/UF)
 */
function formatPropertyLocation(property) {
    let parts = [];
    if (property.neighborhood) parts.push(property.neighborhood);
    
    let cityState = property.city;
    if (property.state) cityState += `/${property.state}`;
    parts.push(cityState);
    
    return parts.join(" • ");
}

/**
 * Utilitário para formatar texto de área
 */
function formatArea(min, max) {
    if (!min && !max) return null;
    if (min === max || (!max && min)) return `${min}m²`;
    if (!min && max) return `Até ${max}m²`;
    return `${min} a ${max}m²`;
}

/**
 * Extrai opções únicas de um array de objetos para filtros
 */
function getUniqueValues(arr, key) {
    const values = new Set();
    arr.forEach(item => {
        if (Array.isArray(item[key])) {
            item[key].forEach(val => values.add(val));
        } else if (item[key]) {
            values.add(item[key]);
        }
    });
    return Array.from(values).sort();
}

/**
 * Animação de reveal no scroll
 */
function initScrollReveal() {
    const reveals = document.querySelectorAll(".reveal");
    
    if (reveals.length === 0 || !window.IntersectionObserver) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("reveal--visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });
    
    reveals.forEach(reveal => {
        observer.observe(reveal);
    });
}
