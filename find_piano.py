"""Find piano works in music21 corpus."""
from music21 import corpus

all_works = []
for composer in ['bach', 'beethoven', 'mozart', 'handel', 'chopin', 'schumann', 'debussy', 'rachmaninoff']:
    try:
        paths = corpus.getComposer(composer)
        for p in paths:
            pstr = str(p)
            idx = pstr.find('music21/corpus')
            if idx >= 0:
                rel = pstr[idx+14:].replace('\\', '/')
            else:
                idx = pstr.upper().find('CORPUS')
                rel = pstr[idx+7:].replace('\\', '/')
            all_works.append((composer, rel))
    except Exception as e:
        print(f'{composer}: {e}')

print(f'Total works found: {len(all_works)}')

# Find piano-specific works
piano_works = []
for composer, work in all_works:
    work_lower = work.lower()
    is_piano = False
    reasons = []

    if 'piano' in work_lower:
        is_piano = True
        reasons.append('piano')
    if 'sonata' in work_lower:
        is_piano = True
        reasons.append('sonata')
    if 'opus' in work_lower and composer == 'beethoven':
        is_piano = True
        reasons.append('beethoven opus')
    if 'pre' in work_lower and composer in ['bach', 'chopin']:
        is_piano = True
        reasons.append('prelude')
    if 'fugue' in work_lower and composer == 'bach':
        is_piano = True
        reasons.append('fugue')
    if 'bwv' in work_lower and composer == 'bach':
        try:
            num_str = work_lower.split('bwv')[1].split('.')[0]
            if num_str.isdigit():
                num = int(num_str)
                if 846 <= num <= 851:
                    is_piano = True
                    reasons.append('wtc')
        except:
            pass
    if any(k in work_lower for k in ['k155','k156','k458','k545','k80']):
        is_piano = True
        reasons.append('mozart k')
    if 'hwv' in work_lower and composer == 'handel':
        is_piano = True
        reasons.append('handel hwv')
    if composer in ['chopin', 'schumann', 'debussy']:
        is_piano = True
        reasons.append(composer)

    if is_piano:
        piano_works.append((work, reasons))

print(f'Piano works found: {len(piano_works)}')
for work, reasons in piano_works[:30]:
    print(f'{work}: {reasons}')
