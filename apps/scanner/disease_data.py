"""
Static knowledge base mapping raw model labels (PlantVillage dataset
naming convention) to symptoms/treatment. Covers all 38 classes the
model was trained on.

⚠️ Agricultural disclaimer: these descriptions are general-purpose
reference info, not a substitute for professional agronomic diagnosis.
Consider having a plant pathologist or extension service review this
content before using it to advise real growers on treatment decisions.
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "symptoms": "Olive-green to black velvety spots on leaves and fruit; "
                    "leaves may yellow and drop early.",
        "treatment": "Apply fungicide (e.g. captan or myclobutanil) starting at bud break. "
                     "Rake and destroy fallen leaves to reduce overwintering spores.",
    },
    "Apple___Black_rot": {
        "symptoms": "Purple-bordered leaf spots, and 'frogeye' lesions on fruit "
                    "that rot from the blossom end.",
        "treatment": "Prune out dead/cankered wood. Apply fungicide during the growing season "
                     "and remove mummified fruit from the tree and ground.",
    },
    "Apple___Cedar_apple_rust": {
        "symptoms": "Bright orange-yellow spots on leaves, sometimes with tube-like "
                    "structures on the underside.",
        "treatment": "Apply fungicide in spring. Remove nearby cedar/juniper trees if "
                     "feasible, as they host the alternate stage of this fungus.",
    },
    "Apple___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Blueberry___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Maintain regular watering and soil acidity.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "symptoms": "White powdery fungal growth on leaves and shoots; leaves may "
                    "curl or distort.",
        "treatment": "Apply sulfur-based or systemic fungicide. Improve air circulation "
                     "by pruning dense growth.",
    },
    "Cherry_(including_sour)___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "symptoms": "Small rectangular gray-to-tan lesions along leaf veins, "
                    "which can merge and cause significant leaf blighting.",
        "treatment": "Rotate crops and till residue to reduce spore survival. "
                     "Apply foliar fungicide if disease pressure is high.",
    },
    "Corn_(maize)___Common_rust_": {
        "symptoms": "Small, reddish-brown, powdery pustules scattered on both leaf surfaces.",
        "treatment": "Plant resistant hybrids. Fungicide application is rarely needed "
                     "unless infection is severe and early in the season.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "symptoms": "Long, cigar-shaped gray-green lesions on leaves that turn tan.",
        "treatment": "Use resistant hybrids and rotate crops. Fungicide can help "
                     "if applied early during heavy disease pressure.",
    },
    "Corn_(maize)___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Grape___Black_rot": {
        "symptoms": "Small brown circular leaf spots and shriveled, mummified black fruit.",
        "treatment": "Remove mummified berries and infected canes. Apply fungicide "
                     "starting at early shoot growth through fruit set.",
    },
    "Grape___Esca_(Black_Measles)": {
        "symptoms": "Tiger-stripe pattern of yellow/brown discoloration between leaf veins; "
                    "berries may show dark spotting.",
        "treatment": "No cure once established — remove and destroy severely affected vines. "
                     "Avoid pruning wounds during wet weather to limit new infections.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "symptoms": "Small dark angular spots on leaves that enlarge and merge, "
                    "causing premature leaf drop.",
        "treatment": "Apply copper-based fungicide. Improve canopy airflow through pruning.",
    },
    "Grape___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "symptoms": "Blotchy mottled yellowing of leaves (asymmetric across the midrib), "
                    "lopsided bitter fruit, twig dieback.",
        "treatment": "No cure exists. Remove and destroy infected trees to limit spread. "
                     "Control the Asian citrus psyllid insect vector with approved insecticides.",
    },
    "Peach___Bacterial_spot": {
        "symptoms": "Small dark angular spots on leaves that may fall out, creating a "
                    "'shot-hole' look; sunken lesions on fruit.",
        "treatment": "Apply copper-based bactericide during dormancy. Plant resistant "
                     "varieties where available; avoid overhead irrigation.",
    },
    "Peach___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "symptoms": "Small water-soaked spots on leaves that turn brown and scabby "
                    "raised spots on fruit.",
        "treatment": "Apply copper-based bactericide. Use disease-free seed and avoid "
                     "working in fields when foliage is wet.",
    },
    "Pepper,_bell___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Potato___Early_blight": {
        "symptoms": "Concentric ring spots (target-like) on older leaves, "
                    "yellowing around lesions.",
        "treatment": "Apply fungicide at first sign of disease. Rotate crops yearly "
                     "and remove plant debris after harvest.",
    },
    "Potato___Late_blight": {
        "symptoms": "Dark, water-soaked spots on leaves that enlarge rapidly; "
                    "white fungal growth on the underside in humid conditions.",
        "treatment": "Remove and destroy infected foliage immediately. Apply a "
                     "copper-based fungicide. Avoid overhead watering.",
    },
    "Potato___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Raspberry___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Soybean___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Squash___Powdery_mildew": {
        "symptoms": "White powdery patches on leaf surfaces, spreading to cover "
                    "the whole leaf; leaves may yellow and die.",
        "treatment": "Apply sulfur or potassium bicarbonate fungicide. Ensure good "
                     "spacing between plants for airflow.",
    },
    "Strawberry___Leaf_scorch": {
        "symptoms": "Small dark purple spots on leaves that merge into larger "
                    "scorched-looking blotches.",
        "treatment": "Remove infected leaves after harvest. Apply fungicide and "
                     "avoid overhead watering.",
    },
    "Strawberry___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular monitoring and care.",
    },
    "Tomato___Bacterial_spot": {
        "symptoms": "Small water-soaked spots on leaves and fruit that turn dark "
                    "and scabby.",
        "treatment": "Apply copper-based bactericide. Use disease-free seed/transplants "
                     "and avoid overhead watering.",
    },
    "Tomato___Early_blight": {
        "symptoms": "Concentric ring spots (target-like) on older/lower leaves first.",
        "treatment": "Remove affected lower leaves, apply fungicide, and mulch "
                     "to prevent soil splash onto foliage.",
    },
    "Tomato___Late_blight": {
        "symptoms": "Dark, water-soaked spots on leaves that enlarge rapidly; "
                    "white fungal growth on the underside in humid conditions.",
        "treatment": "Remove and destroy infected foliage immediately. Apply a "
                     "copper-based fungicide. Avoid overhead watering.",
    },
    "Tomato___Leaf_Mold": {
        "symptoms": "Pale green/yellow spots on upper leaf surface with olive-green "
                    "to grayish mold on the underside.",
        "treatment": "Improve greenhouse/garden ventilation to lower humidity. "
                     "Apply fungicide if conditions favor disease spread.",
    },
    "Tomato___Septoria_leaf_spot": {
        "symptoms": "Numerous small circular spots with dark borders and gray centers, "
                    "starting on lower leaves.",
        "treatment": "Remove infected leaves, apply fungicide, and rotate crops "
                     "to reduce soil-borne spore carryover.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "symptoms": "Fine yellow stippling on leaves, fine webbing on the underside "
                    "in heavy infestations.",
        "treatment": "Apply miticide or insecticidal soap. Increase humidity, as "
                     "mites thrive in hot, dry conditions.",
    },
    "Tomato___Target_Spot": {
        "symptoms": "Brown concentric-ringed spots on leaves, stems, and fruit.",
        "treatment": "Apply fungicide and improve air circulation through pruning "
                     "and proper plant spacing.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "symptoms": "Upward curling and yellowing of leaves, stunted plant growth, "
                    "reduced fruit set.",
        "treatment": "No cure — remove and destroy infected plants. Control whitefly "
                     "populations, which transmit the virus, with insecticides or netting.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "symptoms": "Mottled light/dark green mosaic pattern on leaves, "
                    "leaf distortion, stunted growth.",
        "treatment": "No cure — remove and destroy infected plants. Disinfect tools "
                     "between plants and wash hands after handling tobacco products.",
    },
    "Tomato___healthy": {
        "symptoms": "No visible disease symptoms detected.",
        "treatment": "No treatment needed. Continue regular watering and monitoring.",
    },
}


def get_disease_info(raw_label: str) -> dict:
    """Looks up symptoms/treatment, with a safe fallback for unmapped labels."""
    return DISEASE_INFO.get(raw_label, {
        "symptoms": "Information not available for this class yet.",
        "treatment": "Please consult a local agricultural expert.",
    })