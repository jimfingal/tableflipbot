# -*- coding: utf-8 -*-
import random

# Example flippers
# (╯°□°)╯︵ 
# (ヽ ゜Д゜)ノ ︵ 
# (ﾉ ಥ益ಥ）)ﾉ︵ 
# (ノ^_^)ノ︵
# (╯°Д°）╯︵
# (╯'□')╯︵ 
# (ﾉಥДಥ)ﾉ︵
# (._.) ~ ︵
# ʕノ•ᴥ•ʔノ ︵ 
# (/¯◡ ‿ ◡)/¯ ~ 
# ┗[© ♒ ©]┛ ︵ 
# ︵ ლ(⌒-⌒ლ)
# ヽ(`Д´)ﾉ︵ 

flipper_arms = ['╯', 'ノ', '\\', 'ﾉ', 'ﾉ', '~', '/¯', 'ヽ'] * 3 + ['ლ']
flipper_eyes = ['°', '゜' 'ಥ', '^', "'", '.', '•', '◡', '©', '´', '`']
flipper_noses = ['□', 'Д', '_', 'ᴥ', '◡', 'O']
flipper_chars = ['︵', '︵', '︵','~']
flipper_flesh = [''] * 4 + [' ']
flipper_sides = [('(', ')')] * 4 + [('ʕ', 'ʔ'), ('[', ']')]

# Ha, pun!
flip_table = {
    "a" : 'ɐ',
    "b" : 'q',
    "c" : 'ɔ', 
    "d" : 'p',
    "e" : 'ǝ',
    "f" : 'ɟ',
    "g" : 'b',
    "h" : 'ɥ',
    "i" : 'ı',
    "j" : 'ſ',
    "k" : 'ʞ',
    "l" : 'ן',
    "m" : 'ɯ',
    "n" : 'u',
    "o" : 'o',
    "p" : 'd',
    "q" : 'b',
    "r" : 'ɹ',
    "s" : 's',
    "t" : 'ʇ',
    "u" : 'n',
    "v" : 'ʌ',
    "w" : 'ʍ',
    "x" : 'x',
    "y" : 'ʎ',
    "z" : 'z',
    "1" : "Ɩ",
    "2" : "ᄅ",
    "3" : "Ɛ",
    "4" : "ㄣ",
    "5" : "ϛ",
    "6" : "9",
    "7" : "ㄥ",
    "8" : "8",
    "9" : "6",
    "0" : "0",
    ",": '\'',
    "\'" : ',',
    '.' : '˙',
    '[' : ']',
    '(' : ')',
    '{' : '}',
    '?' : '¿',
    '!' : '¡',
    "\"": ",,",
    '<' : '>',
    '>' : '<',
    '[' : ']',
    ']' : '[',
    '{' : '}',
    '}' : '{',
    '(' : ')',
    '(' : ')',
    '(' : ')',
    '(' : ')',
    '&' : '⅋',
    '%' : '%',
    '_' : '‾',
    '^' : 'v',
    '#' : '#',
    '$' : '$',
    ' ' : ' '
}

def get_flipper():
    flip = random.choice(flipper_chars)
    flesh1 = random.choice(flipper_flesh)
    flesh2 = random.choice(flipper_flesh)
    flesh3 = random.choice(flipper_flesh)

    sides = random.choice(flipper_sides)
    arm = random.choice(flipper_arms)
    nose = random.choice(flipper_noses)
    eye = random.choice(flipper_eyes)
    
    return sides[0] + arm + flesh1 + eye +  flesh2 + nose + eye + flesh3 + sides[1] + arm + flip

def get_flipped(string): 
    return ''.join(map(lambda x: flip_table.get(x, x), reversed(string.lower())))

def get_flipped_string(string):
    
    flipper = get_flipper()
    flipped = get_flipped(string)
    
    return flipper + "  " + flipped