"use strict";

const propertyState = {
    all: [],
    filtered: [],
    filters: {
        location: 'all',
        type: 'all',
        bedrooms: 'all',
        text: ''
    }
};

function initFilters() {
    propertyState.all = [...properties];
    propertyState.filtered = [...properties];

    populateSelectFilters();
    populateChips();
    setupEventListeners();
    
    renderProperties(propertyState.filtered);
    updateRegions();
}

function populateSelectFilters() {
    const locSelect = document.getElementById('search-location');
    const typeSelect = document.getElementById('search-type');
    const bedSelect = document.getElementById('search-bedrooms');

    if (!locSelect || !typeSelect || !bedSelect) return;

    // Popula Localização (Cidades)
    const cities = getUniqueValues(propertyState.all, 'city');
    cities.forEach(city => {
        const opt = document.createElement('option');
        opt.value = city;
        opt.textContent = city;
        locSelect.appendChild(opt);
    });

    // Popula Tipo
    const types = getUniqueValues(propertyState.all, 'propertyTypes');
    types.forEach(type => {
        const opt = document.createElement('option');
        opt.value = type;
        opt.textContent = type;
        typeSelect.appendChild(opt);
    });

    // Popula Dormitórios
    const beds = getUniqueValues(propertyState.all, 'bedrooms');
    beds.forEach(bed => {
        const opt = document.createElement('option');
        opt.value = bed;
        opt.textContent = `${bed} ${bed === 1 ? 'dormitório' : 'dormitórios'}`;
        bedSelect.appendChild(opt);
    });
}

function populateChips() {
    const chipsContainer = document.getElementById('filter-chips');
    if (!chipsContainer) return;

    // Remove existing dynamic chips
    chipsContainer.querySelectorAll('.chip:not([data-filter="all"])').forEach(c => c.remove());

    const types = getUniqueValues(propertyState.all, 'propertyTypes');
    types.forEach(type => {
        const chip = document.createElement('button');
        chip.className = 'chip';
        chip.dataset.filterType = 'type';
        chip.dataset.filterValue = type;
        chip.textContent = type;
        chipsContainer.appendChild(chip);
    });

    const cities = getUniqueValues(propertyState.all, 'city');
    cities.forEach(city => {
        const chip = document.createElement('button');
        chip.className = 'chip';
        chip.dataset.filterType = 'location';
        chip.dataset.filterValue = city;
        chip.textContent = city;
        chipsContainer.appendChild(chip);
    });

    // Chip listeners
    chipsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('chip')) {
            // Update UI
            chipsContainer.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');

            // Reset filters via chips
            propertyState.filters.location = 'all';
            propertyState.filters.type = 'all';
            propertyState.filters.bedrooms = 'all';
            propertyState.filters.text = '';
            
            // Sync form visual reset
            document.getElementById('search-form').reset();

            const filterType = e.target.dataset.filterType;
            const filterValue = e.target.dataset.filterValue;

            if (filterType === 'type') {
                propertyState.filters.type = filterValue;
            } else if (filterType === 'location') {
                propertyState.filters.location = filterValue;
            }

            applyFilters();
        }
    });
}

function setupEventListeners() {
    const form = document.getElementById('search-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            propertyState.filters.location = document.getElementById('search-location').value;
            propertyState.filters.type = document.getElementById('search-type').value;
            propertyState.filters.bedrooms = document.getElementById('search-bedrooms').value;
            propertyState.filters.text = document.getElementById('search-text').value;

            // Reset chips
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            document.querySelector('.chip[data-filter="all"]').classList.add('active');

            applyFilters();
            
            // Scroll to catalog
            document.getElementById('catalogo').scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    const clearBtn = document.getElementById('clear-filters-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            // Reset state
            propertyState.filters = { location: 'all', type: 'all', bedrooms: 'all', text: '' };
            
            // Reset UI
            if (form) form.reset();
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            document.querySelector('.chip[data-filter="all"]').classList.add('active');
            
            applyFilters();
        });
    }
}

function applyFilters() {
    const { location, type, bedrooms, text } = propertyState.filters;
    const normalizedText = normalizeString(text);

    propertyState.filtered = propertyState.all.filter(prop => {
        let match = true;

        if (location !== 'all' && prop.city !== location) {
            match = false;
        }

        if (type !== 'all' && (!prop.propertyTypes || !prop.propertyTypes.includes(type))) {
            match = false;
        }

        if (bedrooms !== 'all') {
            const bedVal = parseInt(bedrooms);
            if (!prop.bedrooms || !prop.bedrooms.includes(bedVal)) {
                match = false;
            }
        }

        if (normalizedText) {
            const searchString = normalizeString(`${prop.name} ${prop.city} ${prop.neighborhood} ${prop.propertyTypes?.join(' ')}`);
            if (!searchString.includes(normalizedText)) {
                match = false;
            }
        }

        return match;
    });

    renderProperties(propertyState.filtered);
}
