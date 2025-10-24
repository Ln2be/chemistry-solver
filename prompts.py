"""
Modular prompt system for physics/chemistry exercise solver
Using text-based modular structure for easy maintenance
"""

# ===== CSS STYLES =====
BASE_CSS = """
<style>
.arabic-message {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
    text-align: right;
    line-height: 1.6;
}

.math-steps {
    margin: 10px 0;
    padding-left: 20px;
}

.math-steps li {
    margin-bottom: 8px;
    line-height: 1.5;
}

.final-answer-box {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    border: 2px solid #1976d2;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.final-answer-title {
    color: #1976d2;
    font-weight: bold;
    font-size: 1.1em;
    margin-bottom: 8px;
    text-align: center;
}

.final-answer-value {
    font-size: 1.3em;
    font-weight: bold;
    color: #0d47a1;
    text-align: center;
    padding: 10px;
    background: white;
    border-radius: 5px;
    border: 1px solid #90caf9;
}

.unit {
    font-size: 0.9em;
    color: #666;
    font-weight: normal;
}
</style>
"""

# ===== ERROR MESSAGES =====
MULTIPLE_EXERCISES_MSG = """
<div class="arabic-message" style="color: #e74c3c; background: #fdf2f2; padding: 15px; border-radius: 10px; border: 1px solid #f5c6cb;">
🔄 يرجى تحميل تمرين واحد فقط في كل مرة<br>
<small>لضمان حل دقيق ومفصل، يرجى تحميل صورة تحتوي على تمرين واحد فقط.</small>
</div>
"""

WRONG_SUBJECT_MSG = """
<div class="arabic-message" style="color: #c0392b; background: #fdeaea; padding: 15px; border-radius: 10px; border: 1px solid #f5b7b1;">
🚫 غير مدعوم<br>
<small>عذرًا، هذا التمرين يبدو أنه في [SUBJECT_PLACEHOLDER]. أنا متخصص فقط في الكيمياء والفيزياء.</small>
</div>
"""

UNREADABLE_IMAGE_MSG = """
<div class="arabic-message" style="color: #d35400; background: #fef9e7; padding: 15px; border-radius: 10px; border: 1px solid #fad7a0;">
📷 صورة غير واضحة<br>
<small>لم أتمكن من تحديد تمرين واضح في هذه الصورة. يرجى تحميل صورة واضحة لمشكلة في الكيمياء أو الفيزياء.</small>
</div>
"""

# ===== VALIDATION RULES =====
VALIDATION_RULES = """
**VALIDATION OBLIGATOIRE:**
1. Si l'image contient PLUS D'UN exercice → montre le message en arabe avec classe CSS
2. Si l'image contient des mathématiques, biologie, français, histoire ou autre matière non-scientifique → excuse-toi en arabe avec classe CSS  
3. Si l'image n'est pas lisible ou pas un exercice → signale-le en arabe avec classe CSS
"""

# ===== FORMATTING RULES =====
FORMATTING_RULES = """
**RÈGLES DE FORMATAGE:**
- TOUTES les formules mathématiques en LaTeX
- TOUTES les équations chimiques en LaTeX
- TOUS les composés chimiques en LaTeX
- TOUTES les unités doivent être en LaTeX
- TOUS les calculs mathématiques doivent être présentés sous forme de liste à puces
- LA RÉPONSE FINALE doit être mise en évidence dans un encadré bleu spécial
- **POUR LES TRANSFORMATIONS D'ÉQUATIONS:**
  * Une étape par ligne
  * Montrer chaque transformation clairement
  * Utiliser des flèches (→) entre les étapes
  * Expliquer brièvement chaque transformation

"""

# ===== PHYSICS PREFERENCES =====
PHYSICS_PREFERENCES = """
**MÉTHODES PRÉFÉRÉES:**
- Pour les problèmes de mécanique, utilise de préférence le théorème de l'énergie cinétique (théorème de l'énergie travail)
- Utilise la conservation de l'énergie mécanique seulement si nécessaire

**CONVENTIONS DE NOMENCLATURE:**
- On appelle la deuxieme loi de Newton : La relation fondamentale de la dynamique ou la RFD
"""

# ===== RESPONSE STRUCTURE =====
EXERCISE_HEADER = "🧪 **EXERCICE COMPLET**"

QUESTION_TEMPLATE = """
**📝 QUESTION {question_number}**
- {question_text}

**🔍 CONCEPTS CLÉS**
- Lois physiques: {physics_laws}
- Constantes: {constants}
- Équations chimiques: {chemical_equations}

**🔬 RÉSOLUTION**
1. **Données:** {data}
2. **Formules appliquées:** {formulas}

3. **Calculs détaillés:**
<ul class="math-steps">
{calculations}
</ul>

4. **Raisonnement:** {reasoning}

{final_answer_box}
"""

TIP_SECTION = """
**💡 CONSEIL**
- {tip_content}
"""

# ===== FINAL ANSWER BOX TEMPLATE =====
# CHANGED: Use Streamlit markdown format instead of HTML
FINAL_ANSWER_BOX_TEMPLATE = """
**🎯 RÉPONSE FINALE**

{answer_value}
"""


# ===== CALCULATION STEP TEMPLATES =====
CALCULATION_STEP = "<li>{step_content}</li>"

EQUATION_STEP = "<li>Application de l'équation: ${equation}$</li>"
SUBSTITUTION_STEP = "<li>Substitution des valeurs: ${substitution}$</li>"
SIMPLIFICATION_STEP = "<li>Simplification: ${simplification}$</li>"
FINAL_CALC_STEP = "<li>Calcul final: ${calculation}$</li>"
UNIT_CONVERSION_STEP = "<li>Conversion d'unités: ${conversion}$</li>"

# ===== ABSOLUTE RULES =====
ABSOLUTE_RULES = """
**RÈGLES ABSOLUES:**
- Résoudre TOUTES les questions de l'exercice
- TOUTES les formules, équations, composés chimiques, unités doivent être en LaTeX!
- Préférer le théorème de l'énergie cinétique à la conservation de l'énergie mécanique
- TOUS les calculs mathématiques doivent être présentés sous forme de liste à puces détaillée
- **POUR LA RÉPONSE FINALE: Ne pas répéter les numéros de question, seulement les valeurs finales**
- **FORMAT CORRECT:**
**🎯 RÉPONSE FINALE**
- utiliser une liste unordonnee et conserver le numero de la question de la reponse
- **POUR LES TRANSFORMATIONS D'ÉQUATIONS: Format étape par étape avec explications**
- **EXEMPLE DE FORMAT CORRECT:**
    <ul class="math-steps">
    <li>Équation de départ: $\\frac{1}{2}mv^2 - \\frac{1}{2}mV_C^2 = mgr(1 - \\cos\\theta)$</li>
    <li>Isoler $v^2$: $\\frac{1}{2}mv^2 = \\frac{1}{2}mV_C^2 + mgr(1 - \\cos\\theta)$</li>
    <li>Multiplier par 2: $mv^2 = mV_C^2 + 2mgr(1 - \\cos\\theta)$</li>
    <li>Diviser par m: $v^2 = V_C^2 + 2gr(1 - \\cos\\theta)$</li>
    <li>Racine carrée: $v = \\sqrt{V_C^2 + 2gr(1 - \\cos\\theta)}$</li>
    </ul>

"""


# ===== PROMPT BUILDING BLOCKS =====
def get_validation_section():
    return VALIDATION_RULES

def get_formatting_section():
    return FORMATTING_RULES

def get_physics_preferences_section():
    return PHYSICS_PREFERENCES

def get_absolute_rules_section():
    return ABSOLUTE_RULES

def get_error_response_section():
    return f"""
**Si l'image contient PLUSIEURS exercices:**
{MULTIPLE_EXERCISES_MSG}

**Si ce n'est PAS de la chimie/physique:**
{WRONG_SUBJECT_MSG}

**Si image illisible/pas d'exercice:**
{UNREADABLE_IMAGE_MSG}
"""

def get_success_response_section():
    return """
**Si c'est un exercice de CHIMIE ou PHYSIQUE valide (UN SEUL exercice):**
- Résous TOUTES les questions de l'exercice
- Pour chaque question, fournis une solution complète
- Utilise systématiquement LaTeX pour toutes les formules et équations
- Pour la physique: préfère le théorème de l'énergie cinétique
- Réponds en français simple avec le minimum de mots nécessaires
- Présente TOUS les calculs mathématiques sous forme de liste à puces détaillée


""" + EXERCISE_HEADER

# ===== MAIN PROMPTS =====
def get_chemistry_prompt():
    return f"""
Tu es un tuteur de chimie pour le baccalauréat. Analyse ce problème et fournis une solution claire.

{get_validation_section()}

{get_formatting_section()}

{get_physics_preferences_section()}

{get_success_response_section()}

{get_error_response_section()}

{get_absolute_rules_section()}
"""

def get_physics_prompt():
    return f"""
Tu es un tuteur de physique pour le baccalauréat. Analyse ce problème et fournis une solution claire.

{get_validation_section()}

{get_formatting_section()}

{get_physics_preferences_section()}

{get_success_response_section()}

{get_error_response_section()}

{get_absolute_rules_section()}
"""

# ===== CALCULATION HELPER FUNCTIONS =====
def create_calculation_step(step_content):
    """Create a single calculation step as list item"""
    return CALCULATION_STEP.format(step_content=step_content)

def create_equation_step(equation):
    """Create an equation application step"""
    return EQUATION_STEP.format(equation=equation)

def create_substitution_step(substitution):
    """Create a value substitution step"""
    return SUBSTITUTION_STEP.format(substitution=substitution)

def create_simplification_step(simplification):
    """Create a simplification step"""
    return SIMPLIFICATION_STEP.format(simplification=simplification)

def create_final_calculation_step(calculation):
    """Create a final calculation step"""
    return FINAL_CALC_STEP.format(calculation=calculation)

def create_unit_conversion_step(conversion):
    """Create a unit conversion step"""
    return UNIT_CONVERSION_STEP.format(conversion=conversion)

def build_calculation_steps(steps_list):
    """Build complete calculations section from list of steps"""
    return "\n".join(steps_list)

# ===== FINAL ANSWER FUNCTIONS =====
def create_final_answer_box(answer_value):
    """Create the final answer box with the requested value"""
    return FINAL_ANSWER_BOX.format(answer_value=answer_value)

def create_physics_final_answer(value, unit=""):
    """Create final answer for physics problems"""
    if unit:
        return f"${value}$ <span class='unit'>{unit}</span>"
    return f"${value}$"

def create_chemistry_final_answer(value, unit=""):
    """Create final answer for chemistry problems"""
    if unit:
        return f"${value}$ <span class='unit'>{unit}</span>"
    return f"${value}$"

# ===== QUESTION FORMATTING FUNCTIONS =====
def get_multiple_exercises_message():
    return MULTIPLE_EXERCISES_MSG

def get_wrong_subject_message(subject_name=""):
    if subject_name:
        return WRONG_SUBJECT_MSG.replace("[SUBJECT_PLACEHOLDER]", subject_name)
    return WRONG_SUBJECT_MSG.replace("[SUBJECT_PLACEHOLDER]", "هذه المادة")

def get_unreadable_image_message():
    return UNREADABLE_IMAGE_MSG

def format_question(question_number, question_text, physics_laws="", constants="", 
                   chemical_equations="", data="", formulas="", calculations="", 
                   reasoning="", final_answer=""):
    """Format a single question using the template"""
    return QUESTION_TEMPLATE.format(
        question_number=question_number,
        question_text=question_text,
        physics_laws=physics_laws,
        constants=constants,
        chemical_equations=chemical_equations,
        data=data,
        formulas=formulas,
        calculations=calculations,
        reasoning=reasoning,
        final_answer_box=final_answer
    )

def format_tip(tip_content):
    """Format a tip section"""
    return TIP_SECTION.format(tip_content=tip_content)

# ===== EXPORT FOR BACKWARD COMPATIBILITY =====
# Define these at the END of the file to avoid circular imports
CHEMISTRY_PROMPT = get_chemistry_prompt()
PHYSICS_PROMPT = get_physics_prompt()