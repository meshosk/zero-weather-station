import re
import sys

# Usage: python fix_namedays_json.py input.json output.json


def fix_namedays_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Odstráň nadbytočné čiarky za posledným objektom pred ]
    content = re.sub(r',\s*\]', ']', content, flags=re.MULTILINE)

    # 2. Pridaj chýbajúce čiarky medzi objektmi: nahrad '}\s*{' za '},\n{' (len v poli)
    content = re.sub(r'}\s*{', '},\n{', content)

    # 3. Odstráň trailing čiarky za posledným atribútom v každom objekte
    # Nahrad ciarku pred } (ale nie pred }, alebo pred ]), teda len vnutri objektu
    content = re.sub(r',\s*}', '}', content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Použitie: python fix_namedays_json.py vstup.json vystup.json')
        sys.exit(1)
    fix_namedays_json(sys.argv[1], sys.argv[2])
