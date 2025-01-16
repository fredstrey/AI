import json
import requests
from bs4 import BeautifulSoup

# Função para obter o lore do herói
def get_lore(hero):
    url = f"https://dota2.fandom.com/wiki/{hero}/Lore"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lore_div = soup.find('div', {'style': 'font-style:italic; font-size:13px;'})
    if lore_div:
        return lore_div.text.strip()
    else:
        return "Lore not found"

# Lista de heróis
herois = [
    'Abaddon', 'Alchemist', 'Ancient Apparition', 'Anti-Mage', 'Arc Warden', 'Axe', 'Bane', 'Batrider',
    'Beastmaster', 'Bloodseeker', 'Crystal Maiden', 'Dark Seer', 'Dazzle', 'Death Prophet', 'Disruptor', 'Doom',
    'Dragon Knight', 'Drow Ranger', 'Earth Spirit', 'Earthshaker', 'Elder Titan', 'Ember Spirit', 'Enchantress',
    'Enigma', 'Faceless Void', 'Gyrocopter', 'Huskar', 'Invoker', 'Io', 'Jakiro', 'Juggernaut', 'Keeper of the Light',
    'Kunkka', 'Legion Commander', 'Leshrac', 'Lich', 'Lifestealer', 'Lina', 'Lion', 'Lone Druid', 'Luna', 'Magnus',
    'Medusa', 'Meepo', 'Mirana', 'Monkey King', 'Morphling', 'Naga Siren', 'Necrophos', 'Night Stalker', 'Oracle',
    'Outworld Destroyer', 'Pango', 'Phantom Assassin', 'Phantom Lancer', 'Pugna', 'Razor', 'Riki', 'Rubick', 'Sand King',
    'Shadow Demon', 'Shadow Fiend', 'Silencer', 'Skywrath Mage', 'Slardar', 'Slark', 'Sniper', 'Spectre', 'Spirit Breaker',
    'Storm Spirit', 'Sven', 'Techies', 'Terrorblade', 'Tinker', 'Tiny', 'Treant Protector', 'Troll Warlord',
    'Templar Assassin', 'Ursa', 'Vengeful Spirit', 'Venomancer', 'Viper', 'Warlock', 'Weaver', 'Windranger',
    'Witch Doctor', 'Zeus', 'Abaddon', 'Alchemist', 'Ancient Apparition', 'Anti-Mage', 'Arc Warden', 'Axe', 'Bane',
    'Batrider', 'Beastmaster', 'Bloodseeker', 'Crystal Maiden', 'Dark Seer', 'Dazzle', 'Death Prophet', 'Disruptor',
    'Doom', 'Dragon Knight', 'Drow Ranger', 'Earth Spirit', 'Earthshaker', 'Elder Titan', 'Ember Spirit', 'Enchantress',
    'Enigma', 'Faceless Void', 'Gyrocopter', 'Huskar', 'Invoker', 'Io', 'Jakiro', 'Juggernaut', 'Keeper of the Light',
    'Kunkka', 'Legion Commander', 'Leshrac','Kez'
]


# Dicionário para armazenar o lore de cada herói
lore_data = {}

# Iterando sobre a lista de heróis para pegar o lore de cada um
for hero in herois:
    lore = get_lore(hero)
    lore_data[hero] = lore

# Salvando em um arquivo JSON
with open('herois_lore.json', 'w', encoding='utf-8') as json_file:
    json.dump(lore_data, json_file, ensure_ascii=False, indent=4)
