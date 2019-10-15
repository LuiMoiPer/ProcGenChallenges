import tracery

def main():
    for _ in range(15):
        print(generateName())

    """
    Name
    PhysicalDescription
        Height
        Weight
        Hair Color
        Eye Color
        Skin Color
        IdentifyingMarks
            Tattoos
            Scars
    Biography
        Family
    Housing Conditions
        Cell
        Diet
            Base Type
                omni
                vegi
                vega
            Allergens
                peanut
                
        Privlages
    Convitions
        Crime
            Sentenc Plea
    """

def generateName():
    rules = {
        'PrisonerProfile' : [
            '\n#FullName#\n\n#PhysicalDescription#\n',
        ],

        'FullName' : [
            '#FirstName# #LastName#',
            '#FirstName# #MiddleName# #LastName#'
        ],

        'FirstName' : [
            '#FirstNameStartSyllable##FirstNameMiddleSyllables##FirstNameEndSyllable#'
        ],
        'FirstNameStartSyllable': [
            'Al',
            'An',
            'Je',
            'Lin',
            'Ma',
            'Ni',
            'Pa',
            'Ro',
            'Ste',
            'Su',
            'Wil',
        ],
        'FirstNameMiddleSyllables': [
            '#FirstNameMiddleSyllable##FirstNameMiddleSyllables#',
            '#FirstNameMiddleSyllable#',
            ''
        ],
        'FirstNameMiddleSyllable': [
            'an',
            'ber',
            'cho',
            'ex',
            'ge',
            'li',
            'me',
            'ni',
            'pha',
            'tho',
            'tri'
        ],
        'FirstNameEndSyllable': [
            'am',
            'cia',
            'da',
            'fer',
            'ine',
            'la',
            'nie',
            'ny',
            'ry',
            'san',
            'to',
        ],
        
        'MiddleName' : [
            '#MiddleNameStartSyllable##MiddleNameMiddleSyllables##MiddleNameEndSyllable#'
        ],
        'MiddleNameStartSyllable': [
            'A',
            'Do',
            'Ed',
            'Eli',
            'Fran',
            'Ka',
            'Ma',
            'Pe',
            'Ro',
            'Va',
            'Vic',
        ],
        'MiddleNameMiddleSyllables': [
            '#MiddleNameMiddleSyllable##MiddleNameMiddleSyllables#',
            '#MiddleNameMiddleSyllable#',
            ''
        ],
        'MiddleNameMiddleSyllable': [
            'ci',
            'cis',
            'ge',
            'ko',
            'li',
            'mo',
            'sa',
            'tor',
            'war',
            'xan',
            'za',
        ],
        'MiddleNameEndSyllable': [
            'beth',
            'a',
            'co',
            'do',
            'ia',
            'na',
            'nic',
            'rie',
            'rot',
            'ta',
            'ter',
        ],
        
        'LastName' : [
            '#LastNameStartSyllable##LastNameMiddleSyllables##LastNameEndSyllable#'
        ],
        'LastNameStartSyllable': [
            'And',
            'Cun',
            'Fer',
            'Gar',
            'Har',
            'Mar',
            'Mil',
            'Mont',
            'Pat',
            'Rob',
            'Sul',
            'Wil',
        ],
        'LastNameMiddleSyllables': [
            '#LastNameMiddleSyllable##LastNameMiddleSyllables#',
            '#LastNameMiddleSyllable#',
            ''
        ],
        'LastNameMiddleSyllable': [
            'der',
            'di',
            'ert',
            'go',
            'gu',
            'in',
            'li',
            'mer',
            'ing',
            'pen',
            'ter',
        ],
        'LastNameEndSyllable': [
            'ards',
            'cia',
            'ham',
            'ler',
            'na',
            'ris',
            'son',
            'ter',
            'tin',
            'van',
        ],

        'PhysicalDescription' : [
            'Height: #Height#\nWeight: #Weight#\nRace: #Race#\nHair: #HairColor#\nEye: #EyeColor#',
            'Height: #Height#\nWeight: #Weight#\nRace: #Race#\nHair: #HairColor#\nEye: #EyeColor#,\nIdentifying Marks#IdentifyingMarks#',
        ],
        'Height' : ['<HEIGHT>'],
        'Weight' : ['<WEIGHT>'],
        'Race' : [
            'Asian',
            'Black',
            'Indian',
            'White',
        ],
        'HairColor' : [
            'Bald',
            'Black',
            'Blonde',
            'Blue',
            'Gray',
            'Green',
            'Orange',
            'Pink',
            'Purple',
            'Red',
            'Sandy',
            'White',
        ],
        'EyeColor' : [
            'Black',
            'Blue',
            'Brown',
            'Gray',
            'Green',
            'Hazel',
            'Maroon',
            'Multicolored',
            'Pink',
        ]

    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten('#PrisonerProfile#')

if __name__ == "__main__":
    main()