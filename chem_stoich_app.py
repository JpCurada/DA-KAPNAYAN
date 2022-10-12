from pyvalem.formula import Formula
from pyvalem.reaction import Reaction, ReactionParseError
import molmass as mm

import streamlit as st
import numpy as np

st.set_page_config(
    page_title="KAPNAYAN",
    page_icon="	:thermometer:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def is_balanced_or_not(reactants_total_molar_mass, products_total_molar_mass):

    if round(reactants_total_molar_mass,2)  == round(products_total_molar_mass,2) :
        return f"It is a BALANCED chemical equation since the mass of reactants is EQUAL to the mass of products.", f"{round(reactants_total_molar_mass,2)}g = {round(products_total_molar_mass,2)}g"

    else:
        return f"It is NOT A BALANCED chemical equation since the mass of reactants is NOT EQUAL to the mass of products.", f"{round(reactants_total_molar_mass,2)}g ≠ {round(products_total_molar_mass,2)}g"

def get_latex_molar_ratio(reaction_substance_list, reaction_moles_list):
    
    # Convert to substance to Latex
    reaction_substance_LaTex = [Formula(compound).latex for compound in reaction_substance_list]

    # List of Molar Ratio
    molar_ratio = [f"{mol} {sub}" for mol, sub in zip(reaction_moles_list, reaction_substance_LaTex)]

    # LaTex Molar Ratio
    LaTex_molar_ratio = " : ".join(molar_ratio)
    return LaTex_molar_ratio

def reactants_of_reaction(reaction):

    # Get the number of mole per reactant
    r_reac = Reaction(reaction).reactants_text_count_map

    # Create a list for reactants only
    reactants_list = list(r_reac)

    # Create a list for number of mole only
    mole_per_reactant_list = list(r_reac.values())
    
    # Create a list for molar mass per reactant
    reactants_molar_mass_list = [mm.Formula(compound).mass for compound in reactants_list]
    
    # Total molar mass of reactants
    reactants_total_molar_mass = sum(np.array(reactants_molar_mass_list) * np.array(mole_per_reactant_list)) 
    
    return r_reac, reactants_list, mole_per_reactant_list, reactants_molar_mass_list, reactants_total_molar_mass

def products_of_reaction(reaction):

    # Get the products and its number of mole
    r_prod = Reaction(reaction).products_text_count_map

    # Create a list for products only
    products_list = list(r_prod)

    # Create a list for number of mole only
    mole_per_product_list = list(r_prod.values())
    
    # Create a list for molar mass per product
    products_molar_mass_list = [mm.Formula(compound).mass for compound in products_list]
    
    # Total molar mass of products
    products_total_molar_mass = sum(np.array(products_molar_mass_list) * np.array(mole_per_product_list)) 
    
    return r_prod, products_list, mole_per_product_list, products_molar_mass_list, products_total_molar_mass

def reaction_deets(reactants_list, products_list, mole_per_reactant_list, mole_per_product_list, reactants_molar_mass_list, products_molar_mass_list):
    # Create lists for the substance, moles, and molar mass of a reaction
    reaction_substance_list = reactants_list + products_list
    reaction_moles_list = mole_per_reactant_list + mole_per_product_list
    reaction_substance_molar_mass_list = reactants_molar_mass_list + products_molar_mass_list
    # Create dictionaries for substance with mole and substance with molar mass
    reaction_substance_mole_dict = dict(zip(reaction_substance_list, reaction_moles_list))
    reaction_substance_molar_mass_dict = dict(zip(reaction_substance_list,reaction_substance_molar_mass_list))
    return reaction_substance_list, reaction_moles_list, reaction_substance_mole_dict, reaction_substance_molar_mass_dict

def mole_to_mole(reaction_substance_mole_dict, mol_amount, mol_substance, determine_substance_mol):
    return mol_amount * (reaction_substance_mole_dict[determine_substance_mol]/reaction_substance_mole_dict[mol_substance])

def mass_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_mass):
    return mass_amount * (1/reaction_substance_molar_mass_dict[mass_substance]) * (reaction_substance_mole_dict[determine_substance_mass]/reaction_substance_mole_dict[mass_substance]) * reaction_substance_molar_mass_dict[determine_substance_mass]

def mass_to_mole(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_mole):
    return mass_amount * (1/reaction_substance_molar_mass_dict[mass_substance]) * (reaction_substance_mole_dict[determine_substance_mole]/reaction_substance_mole_dict[mass_substance]) 

def mole_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mol_amount, mol_substance, determine_substance_mass):
    return mol_amount * (reaction_substance_mole_dict[determine_substance_mass]/reaction_substance_mole_dict[mol_substance]) * (reaction_substance_molar_mass_dict[determine_substance_mass])

def mole_to_number_of_particles(reaction_substance_mole_dict, mol_amount, mol_substance, determine_substance_nop):
    return mol_amount *  (reaction_substance_mole_dict[determine_substance_nop]/reaction_substance_mole_dict[mol_substance]) * (6.022 *(10**23))

def number_of_particles_to_mole(reaction_substance_mole_dict, nop_amount, nop_substance, determine_substance_mole):
    return nop_amount * (1/(6.022 *(10**23))) * (reaction_substance_mole_dict[determine_substance_mole]/reaction_substance_mole_dict[nop_substance]) 

def mass_to_number_of_particles(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_nop):
    return mass_amount * (1/reaction_substance_molar_mass_dict[mass_substance]) * (reaction_substance_mole_dict[determine_substance_nop]/reaction_substance_mole_dict[mass_substance]) * (6.022 *(10**23))

def number_of_particles_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, nop_amount, nop_substance, determine_substance_mass):
    return nop_amount * (1/(6.022 *(10**23))) * (reaction_substance_mole_dict[determine_substance_mass]/reaction_substance_mole_dict[nop_substance]) * (reaction_substance_molar_mass_dict[determine_substance_mass])

st.title('DA-KAPNAYAN')
st.write("""###### A web application for solving problems involving Stoichiometry with Dimensional Analysis""")
st.caption("Stoichiometry is a tough subject for many pupils. The traditional approach of linking chemical quantities in a reaction via dimensional analysis includes a number of phases in which students struggle to determine which conversion factor to develop and how to apply it.")
# st.sidebar.success("S-KAPNAYAN")
st.markdown('---')
st.subheader("Chemical Equation")
reaction = st.text_input('Input a Balanced Chemical Equation:')

st.caption("This input bar is case-sensitive. You should put a space in every element and you must only use this arrow('→') to separate reactants and products.")

with st.expander("Try these examples!"):
    st.write("""
    ##### You can try this balanced chemical equations ^_^
    Just copy and paste it to the input bar.
    1. 6CO2 + 6H2O → C6H12O6 + 6O2
    2. SiCl4 + 4H2O → H4SiO4 + 4HCl
    3. 2Al + 6HCl → 2AlCl3 + 3H2
    4. Na2CO3 + 2HCl → 2NaCl + H2O + CO2
    5. 2C7H6O2 + 15O2 → 14CO2 + 6H2O
    6. 2Ca3(PO4)2 + 6SiO2 → P4O10 + 6CaSiO3
    7. Al2(SO4)3 + 3Ca(OH)2 → 2Al(OH)3 + 3CaSO4
    8. H2SO4 + 8HI → H2S + 4I2 + 4H2O
    9. 2Fe2O3 + 3C → 4Fe + 3CO2
    10. C6H5OH + 7O2 → 6CO2 + 3H2O
    """)

try:
    st.latex(Reaction(reaction).latex)

    # Define Variables
    r_reac, reactants_list, mole_per_reactant_list, reactants_molar_mass_list, reactants_total_molar_mass = reactants_of_reaction(reaction)
    r_prod, products_list, mole_per_product_list, products_molar_mass_list, products_total_molar_mass = products_of_reaction(reaction)

    # Chemical Reaction
    reaction_substance_list, reaction_moles_list, reaction_substance_mole_dict, reaction_substance_molar_mass_dict = reaction_deets(reactants_list, products_list, mole_per_reactant_list, mole_per_product_list, reactants_molar_mass_list, products_molar_mass_list)

    # Balancing Equation
    st.subheader('Verify: Is the chemical equation balanced?')
    is_balanced_or_not_balanced, equate_mass = is_balanced_or_not(reactants_total_molar_mass, products_total_molar_mass)
    st.write('''##### Law of Conservation of Mass''')
    st.caption('_Matter cannot be created or destroyed in chemical reactions. This is the law of conservation of mass. In every chemical reaction, the same mass of matter must end up in the products as started in the reactants. Balanced chemical equations show that mass is conserved in chemical reactions._')
    st.write(f'''##### {equate_mass}''')
    st.caption(is_balanced_or_not_balanced)

    # Molar Ratio
    LaTex_molar_ratio = get_latex_molar_ratio(reaction_substance_list, reaction_moles_list)
    st.subheader('Molar ratio of the chemical equation')
    st.latex(LaTex_molar_ratio)

    st.markdown("---")

    st.header('Dimensional Analysis')
    st.markdown("Note:")
    st.caption("1. Units of mass is represented only by grams(g)\n2. Units of mass is represented only by mole(mol)\n3. Units of number of particles can be represented as atoms, molecules, and particles\n4. 'e+' is equal to 'x10' and its following number is an exponent")

    feature_t1, feature_t2, feature_t3, feature_t4, feature_t5, feature_t6, feature_t7, feature_t8 = st.tabs(['Mole to Mole', 'Mass to Mass','Mass to Mole', 'Mole to Mass', 'Mole to Number of Particles', 'Number of Particles to Mole', 'Mass to Number of Particles', 'Number of Particles to Mass'])  
    
    with feature_t1:
        st.subheader('Mole-to-Mole Conversion')
        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mol_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mole_to_mole_substance")
        mol_amount = st.number_input('Amount of given substance in moles:', value=1.00, key="mole_to_mole_amount")

        st.write("""##### Required: """)
        determine_substance_mol = st.selectbox("Find the amount the mole of this substance:", tuple(reaction_substance_list), key="mole_to_mole_required")

        if mol_substance == determine_substance_mol:
            st.error('Substance in Given must NOT BE EQUAL to Substance in Required. ')
        else:
            st.write(f'''
            ##### Problem:
            _Using the given equation, **determine how many moles of {determine_substance_mol}** would be formed from **{mol_amount} mole of {mol_substance}**_?
            ''')

            mole_to_mole_answer = round(mole_to_mole(reaction_substance_mole_dict, mol_amount, mol_substance, determine_substance_mol),3)
            st.write(f'''
            ##### Answer:
            ### {mole_to_mole_answer} mol {determine_substance_mol}
            _In the given chemical equation, ***{mole_to_mole_answer} mole of {determine_substance_mol}*** would be formed from {mol_amount} mole of {mol_substance}._
            ''')

    with feature_t2:
        st.subheader('Mass-to-Mass Conversion')
        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mass_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mass_to_mass_substance")
        mass_amount = st.number_input('Amount of given substance in grams:', value=1.000, key="mass_to_mass_amount")

        st.write("""##### Required: """)
        determine_substance_mass = st.selectbox("Find the mass of this substance:", tuple(reaction_substance_list), key="mass_to_mass_required")

        if mass_substance == determine_substance_mass:
            st.error('Substance in Given must NOT BE EQUAL to Substance in Required. ')
        else:
            st.write(f'''
            ##### Problem:
            _Using the given equation, **determine how many grams of {determine_substance_mass}** would be formed from **{mass_amount} grams of {mass_substance}**_?
            ''')

            mass_to_mass_answer = round(mass_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_mass),3)
            
            st.write(f'''
            ##### Answer:
            ### {mass_to_mass_answer}g {determine_substance_mass}
            _In the given chemical equation, ***{mass_to_mass_answer} grams of {determine_substance_mass}*** would be formed from {mass_amount} grams of {mass_substance}._
            ''')
        
    with feature_t3:
        st.subheader('Mass-to-Mole Conversion')
        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mass_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mass_to_mole_substance")
        mass_amount = st.number_input('Amount of given substance in grams:', value=1.000, key="mass_to_mole_amount")

        st.write("""##### Required: """)
        determine_substance_mole = st.selectbox("Find the amount of mole of this substance:", tuple(reaction_substance_list), key="mass_to_mole_required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many mole of {determine_substance_mole}** would be formed from **{mass_amount} grams of {mass_substance}**_?
        ''')

        mass_to_mole_answer = round(mass_to_mole(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_mole),3)
        
        st.write(f'''
        ##### Answer:
        ### {mass_to_mole_answer} mol {determine_substance_mole}
        _In the given chemical equation, ***{mass_to_mole_answer} mole of {determine_substance_mole}*** would be formed from {mass_amount} mole of {mass_substance}._
        ''')

    with feature_t4:
        st.subheader('Mole-to-Mass Conversion')
        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mol_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mole_to_mass_substance")
        mol_amount = st.number_input('Amount of given substance in moles:', value=1.000, key="mole_to_mass_amount")

        st.write("""##### Required: """)
        determine_substance_mass = st.selectbox("Find the mass of this substance:", tuple(reaction_substance_list), key="mole_to_mass_required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many grams of {determine_substance_mass}** would be formed from **{mol_amount} moles of {mol_substance}**_?
        ''')

        mole_to_mass_answer = round(mole_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mol_amount, mol_substance, determine_substance_mass),3)
        
        st.write(f'''
        ##### Answer:
        ### {mole_to_mass_answer} g {determine_substance_mass}
        _In the given chemical equation, ***{mole_to_mass_answer} grams of {determine_substance_mass}*** would be formed from {mol_amount} mole of {mol_substance}._
        ''')

    with feature_t5:
        st.subheader('Mole-to-Particles Conversion')

        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mol_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mole_to_nop_substance")
        mol_amount = st.number_input('Amount of given substance in moles:', value=1.000, key="mole_to_nop_amount")

        st.write("""##### Required: """)
        determine_substance_nop = st.selectbox("Find the number of particles of this substance:", tuple(reaction_substance_list), key="mole_to_nop_required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many particles of {determine_substance_nop}** would be formed from **{mol_amount} moles of {mol_substance}**_?
        ''')

        mole_to_nop_answer = mole_to_number_of_particles(reaction_substance_mole_dict, mol_amount, mol_substance, determine_substance_nop)
        formatted_mole_to_nop_answer = format(mole_to_nop_answer, '.4g')

        st.write(f'''
        ##### Answer:
        ### {formatted_mole_to_nop_answer} atoms {determine_substance_nop}
        _In the given chemical equation, ***{formatted_mole_to_nop_answer} particles of {determine_substance_nop}*** would be formed from {mol_amount} mole of {mol_substance}._
        ''')

    with feature_t6:
        st.subheader('Particles-to-Mole Conversion')

        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        nop_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="nop_to_mol_substance")
        nop_amount = st.number_input('Amount of given substance in atoms or molecules:', value=6.022e+23, key="nop_to_mol_amount")

        st.write("""##### Required: """)
        determine_substance_mole = st.selectbox("Find the amount of mole of this substance:", tuple(reaction_substance_list), key="nop_to_mol_required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many moles of {determine_substance_mole}** would be formed from **{nop_amount} particles of {nop_substance}**_?
        ''')

        nop_to_mole_answer = round(number_of_particles_to_mole(reaction_substance_mole_dict, nop_amount, nop_substance, determine_substance_mole),3)

        st.write(f'''
        ##### Answer:
        ### {nop_to_mole_answer} mol {determine_substance_mole}
        _In the given chemical equation, ***{nop_to_mole_answer} moles of {determine_substance_mole}*** would be formed from {nop_amount} mole of {nop_substance}._
        ''')

    with feature_t7:
        st.subheader('Mass-to-Particles Conversion')

        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        mass_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="mass_to_nop_substance")
        mass_amount = st.number_input('Amount of mass in grams:', value=1.000, key="mass_to_nop_amount")

        st.write("""##### Required: """)
        determine_substance_nop = st.selectbox("Find the the number of particles of this substance:", tuple(reaction_substance_list), key="mass_to_nop_required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many molecules of {determine_substance_nop}** would be formed from **{mass_amount} grams of {mass_substance}**_?
        ''')

        mass_to_nop_answer = mass_to_number_of_particles(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, mass_amount, mass_substance, determine_substance_nop)
        formatted_mass_to_nop_answer = format(mass_to_nop_answer, '.4g')

        st.write(f'''
        ##### Answer:
        ### {formatted_mass_to_nop_answer} molecules {determine_substance_nop}
        _In the given chemical equation, ***{formatted_mass_to_nop_answer} molecules of {determine_substance_nop}*** would be formed from {mass_amount} mole of {mass_substance}._
        ''')

    with feature_t8:
        st.subheader('Particles-to-Mass Conversion')

        st.latex(Reaction(reaction).latex)

        st.write("""##### Given: """)
        nop_substance =  st.selectbox("Given substance:", tuple(reaction_substance_list), key="nop_to_mass_substance")
        nop_amount = st.number_input('Amount of given substance in atoms or molecules:', value=6.022e+23, key="nop_to_mass__amount")

        st.write("""##### Required: """)
        determine_substance_mass = st.selectbox("Find the mass of this substance:", tuple(reaction_substance_list), key="nop_to_mass__required")
    
        st.write(f'''
        ##### Problem:
        _Using the given equation, **determine how many grams of {determine_substance_mass}** would be formed from **{nop_amount} molecules of {nop_substance}**_?
        ''')

        nop_to_mass_answer = round(number_of_particles_to_mass(reaction_substance_mole_dict, reaction_substance_molar_mass_dict, nop_amount, nop_substance, determine_substance_mass),3)

        st.write(f'''
        ##### Answer:
        ### {nop_to_mass_answer} g {determine_substance_mass}
        _In the given chemical equation, ***{nop_to_mass_answer} grams of {determine_substance_mass}*** would be formed from {nop_amount} molecules of {nop_substance}._
        ''')

except ReactionParseError:
    pass

st.markdown('---')

personal_col, reference_col = st.columns(2)

with personal_col:
    st.subheader('About the Creator')
    st.write("""###### This Web application is under development and will have more features soon!""")
    st.caption('"_Exploring Python modules and maximizing the potential of Streamlit._"')
    st.caption("_— John Paul M. Curada | Python and Data Science Enthusiast_")

    st.write("**Contacts:**")
    
    st.caption("For feedbacks, suggestions, bugs, and inquiries, message me at: ")
    st.caption("Email: j.curada02@gmail.com")
    st.caption("Twitter: https://twitter.com/jpcodesss_")


