from fontTools.ttLib import TTFont

font = TTFont('franklin')
gsub = font['GSUB'].table

for lookup in gsub.LookupList.Lookup:
    for subtable in lookup.SubTable:
        if hasattr(subtable, 'ligatures'):
            for first_glyph, ligs in subtable.ligatures.items():
                for lig in ligs:
                    components = [first_glyph] + lig.Component
                    print(' + '.join(components), '->', lig.LigGlyph)
