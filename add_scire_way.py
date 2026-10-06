import json
import re

with open('js/properties.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the last item in the array to insert before it, or just find the end of the array.
# Or better, just insert it before the closing '];'

# We don't know the exact number of images yet, but we will add the gallery later or just give it 40.
gallery_items = []
# we will fill this once extraction finishes.

scire_way_obj = '''    },
    {
        id: 15,
        slug: "scire-way",
        name: "Scire Way",
        developer: "Scire Empreendimentos",
        city: "Palhoça",
        neighborhood: "Passa Vinte",
        state: "SC",
        address: "Passa Vinte, Palhoça",
        coordinates: null,
        propertyTypes: ["Apartamento"],
        bedrooms: [2],
        suites: [1],
        areaMin: 49.85,
        areaMax: 55.29,
        parking: null,
        price: null,
        paymentInfo: null,
        delivery: null,
        headline: "Dê forma ao seu próximo caminho.",
        shortDescription: "Duas torres residenciais com apartamentos de dois dormitórios e mais de 10 áreas de lazer.",
        description: "Localizado no bairro Passa Vinte, em Palhoça, o Scire Way foi pensado para acompanhar o momento de quem busca o primeiro imóvel. São duas torres com infraestrutura completa, incluindo varanda com churrasqueira e fechadura eletrônica em todas as unidades.",
        highlights: [
            "Fechadura eletrônica",
            "Varanda com churrasqueira",
            "Estação para recarga de veículos",
            "Reconhecimento facial na portaria"
        ],
        amenities: [
            "Piscina Adulto e Infantil",
            "Playground",
            "Pet Place",
            "Quadra de Areia",
            "Salão de Festas com Espaço Gourmet",
            "Redário",
            "Bicicletário",
            "Horta e Pomar"
        ],
        nearby: [
            "Colégio CMS: 3 min",
            "Bistek Supermercado: 5 min",
            "Shopping Via Catarina: 8 min",
            "Unisul de Pedra Branca: 9 min"
        ],
        typologies: [
            "2 dormitórios (49,85 m² a 50,15 m²)",
            "2 dormitórios com demi-suíte + lavabo (55,29 m²)"
        ],
        coverImage: "assets/images/properties/scire-way/cover.webp?v=1",
        logo: null,
        gallery: [],
        legalDisclaimer: null
    }
];'''

content = re.sub(r'    \}\n\];', scire_way_obj, content)

with open('js/properties.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Scire Way added to properties.js")
