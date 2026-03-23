#!/bin/bash
CREDS=$(echo -n 't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D' | base64)
BASE="C:/Users/tmizu/nambei-images"

upload_simple() {
    local filepath="$1"
    local wp_name="$2"

    local result=$(curl -sS -X POST "https://nambei-oyaji.com/wp-json/wp/v2/media" \
        -H "Authorization: Basic $CREDS" \
        -F "file=@${filepath};filename=${wp_name};type=image/jpeg" \
        2>&1)

    local media_id=$(echo "$result" | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://')

    if [ -n "$media_id" ] && [ "$media_id" -gt 0 ] 2>/dev/null; then
        echo "$media_id"
    else
        echo "0"
    fi
}

echo "=== Uploading all remaining images ==="

# Track results
declare -A MEDIA_IDS

# Already uploaded
MEDIA_IDS[asuncion-aerial]=1101
MEDIA_IDS[asuncion-city]=1102
MEDIA_IDS[airplane-window]=1095
MEDIA_IDS[airplane-city-view]=1096
MEDIA_IDS[laptop-wooden-table]=1097
MEDIA_IDS[school-children]=1098
MEDIA_IDS[hero-landscape]=1099
MEDIA_IDS[meat-grill]=1100
MEDIA_IDS[py-building]=1103

# Upload remaining files
FILES=(
    "$BASE/paraguay-life/paraguay-nature.jpg|nao-py-nature.jpg|py-nature"
    "$BASE/paraguay-life/asado-bbq.jpg|nao-asado.jpg|asado"
    "$BASE/paraguay-life/bbq-cooking.jpg|nao-bbq-cook.jpg|bbq-cook"
    "$BASE/paraguay-life/latin-street.jpg|nao-latin-st.jpg|latin-street"
    "$BASE/immigration/passport-documents.jpg|nao-passport1.jpg|passport1"
    "$BASE/immigration/passport-book.jpg|nao-passport2.jpg|passport2"
    "$BASE/immigration/airplane-wing.jpg|nao-air-wing.jpg|air-wing"
    "$BASE/remote-work/remote-work-laptop.jpg|nao-rw-laptop.jpg|rw-laptop"
    "$BASE/remote-work/desk-laptop.jpg|nao-desk-lp.jpg|desk-lp"
    "$BASE/remote-work/laptop-coffee.jpg|nao-lp-coffee.jpg|lp-coffee"
    "$BASE/remote-work/laptop-silver.jpg|nao-lp-silver.jpg|lp-silver"
    "$BASE/family-education/school-classroom.jpg|nao-classroom.jpg|classroom"
    "$BASE/family-education/children-desks.jpg|nao-ch-desks.jpg|ch-desks"
    "$BASE/family-education/family-outdoor.jpg|nao-fam-out.jpg|fam-out"
    "$BASE/family-education/family-picnic.jpg|nao-fam-pic.jpg|fam-pic"
    "$BASE/family-education/children-playground.jpg|nao-ch-play.jpg|ch-play"
    "$BASE/finance/money-exchange.jpg|nao-money-ex.jpg|money-ex"
    "$BASE/finance/money-banknotes.jpg|nao-money-bn.jpg|money-bn"
    "$BASE/finance/mobile-banking.jpg|nao-mob-bank.jpg|mob-bank"
    "$BASE/homepage/city-view.jpg|nao-cityview.jpg|cityview"
    "$BASE/general/starry-night.jpg|nao-stars.jpg|stars"
    "$BASE/general/family-park.jpg|nao-fam-park.jpg|fam-park"
)

for entry in "${FILES[@]}"; do
    IFS='|' read -r filepath wpname key <<< "$entry"

    if [ ! -f "$filepath" ]; then
        echo "SKIP: $filepath"
        continue
    fi

    mid=$(upload_simple "$filepath" "$wpname")
    if [ "$mid" != "0" ]; then
        echo "OK ID:$mid -> $wpname ($key)"
        MEDIA_IDS[$key]=$mid
    else
        echo "FAIL: $wpname"
    fi
    sleep 0.5
done

echo ""
echo "=== Upload Results ==="
for key in "${!MEDIA_IDS[@]}"; do
    echo "  $key: ${MEDIA_IDS[$key]}"
done

# Save to file
echo "=== Saving mapping ==="
python3 -c "
import json
data = {
$(for key in "${!MEDIA_IDS[@]}"; do echo "    '$key': ${MEDIA_IDS[$key]},"; done)
}
with open(r'C:\Users\tmizu\nambei-images\final-media-ids.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Saved to final-media-ids.json')
"
