#!/bin/bash
CREDS=$(echo -n 't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D' | base64)
BASE="C:/Users/tmizu/nambei-images"

# Output mapping file
echo "{" > "$BASE/media-ids.json"
FIRST=true

upload() {
    local filepath="$1"
    local wp_filename="$2"
    local title="$3"
    local alt="$4"
    local key="$5"

    if [ ! -f "$filepath" ]; then
        echo "SKIP: $filepath not found"
        return
    fi

    local result=$(curl -sS -X POST "https://nambei-oyaji.com/wp-json/wp/v2/media" \
        -H "Authorization: Basic $CREDS" \
        -F "file=@${filepath};filename=${wp_filename};type=image/jpeg" \
        -F "title=$title" \
        -F "alt_text=$alt" \
        2>&1)

    local media_id=$(echo "$result" | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://')

    if [ -n "$media_id" ] && [ "$media_id" -gt 0 ] 2>/dev/null; then
        echo "OK ID:$media_id -> $wp_filename"
        if [ "$FIRST" = true ]; then FIRST=false; else echo "," >> "$BASE/media-ids.json"; fi
        echo "  \"$key\": $media_id" >> "$BASE/media-ids.json"
    else
        echo "FAIL: $wp_filename"
    fi
    sleep 0.3
}

echo "=== Uploading remaining images ==="

# Already uploaded (from previous attempts):
# asuncion-aerial.jpg -> 1101
# nao-asuncion-city.jpg -> 1102
# airplane-window.jpg -> 1095
# airplane-city-view.jpg -> 1096
# laptop-wooden-table.jpg -> 1097
# school-children.jpg -> 1098
# hero-landscape.jpg -> 1099
# meat-grill.jpg -> 1100

# Record existing uploads
echo "  \"asuncion-aerial\": 1101," >> "$BASE/media-ids.json"
echo "  \"asuncion-city\": 1102," >> "$BASE/media-ids.json"
echo "  \"airplane-window\": 1095," >> "$BASE/media-ids.json"
echo "  \"airplane-city-view\": 1096," >> "$BASE/media-ids.json"
echo "  \"laptop-wooden-table\": 1097," >> "$BASE/media-ids.json"
echo "  \"school-children\": 1098," >> "$BASE/media-ids.json"
echo "  \"hero-landscape\": 1099," >> "$BASE/media-ids.json"
echo "  \"meat-grill\": 1100" >> "$BASE/media-ids.json"
FIRST=false

# Upload remaining images with nao- prefix
upload "$BASE/paraguay-life/paraguay-building.jpg" "nao-py-building.jpg" "パラグアイの建物" "パラグアイの白い建物" "py-building"
upload "$BASE/paraguay-life/paraguay-nature.jpg" "nao-py-nature.jpg" "パラグアイの自然" "パラグアイの水辺" "py-nature"
upload "$BASE/paraguay-life/asado-bbq.jpg" "nao-asado-bbq.jpg" "アサードBBQ" "南米式バーベキュー" "asado-bbq"
upload "$BASE/paraguay-life/bbq-cooking.jpg" "nao-bbq-cooking.jpg" "アサード調理" "グリルで肉を焼く" "bbq-cooking"
upload "$BASE/paraguay-life/latin-street.jpg" "nao-latin-street.jpg" "南米の街並み" "南米の教会と緑" "latin-street"

upload "$BASE/immigration/passport-documents.jpg" "nao-passport-docs.jpg" "パスポートと書類" "パスポートの写真" "passport-docs"
upload "$BASE/immigration/passport-book.jpg" "nao-passport-book.jpg" "パスポート" "パスポートブック" "passport-book"
upload "$BASE/immigration/airplane-wing.jpg" "nao-airplane-wing.jpg" "飛行機の翼" "飛行機の翼と空" "airplane-wing"

upload "$BASE/remote-work/remote-work-laptop.jpg" "nao-remote-laptop.jpg" "リモートワーク" "リモートワークのノートPC" "remote-laptop"
upload "$BASE/remote-work/desk-laptop.jpg" "nao-desk-laptop.jpg" "デスクワーク" "デスクのノートPC" "desk-laptop"
upload "$BASE/remote-work/laptop-coffee.jpg" "nao-laptop-coffee.jpg" "ノートPCとコーヒー" "ノートPCとコーヒー" "laptop-coffee"
upload "$BASE/remote-work/laptop-silver.jpg" "nao-laptop-silver.jpg" "シルバーのノートPC" "シルバーのノートPC" "laptop-silver"

upload "$BASE/family-education/school-classroom.jpg" "nao-school-room.jpg" "教室" "教室の子どもたち" "school-room"
upload "$BASE/family-education/children-desks.jpg" "nao-children-desks.jpg" "授業中" "机に座る子どもたち" "children-desks"
upload "$BASE/family-education/family-outdoor.jpg" "nao-family-outdoor.jpg" "家族" "屋外で遊ぶ子どもたち" "family-outdoor"
upload "$BASE/family-education/family-picnic.jpg" "nao-family-picnic.jpg" "自然体験" "草原の子どもたち" "family-picnic"
upload "$BASE/family-education/children-playground.jpg" "nao-children-play.jpg" "子どもの遊び" "広場で遊ぶ子どもたち" "children-play"

upload "$BASE/finance/money-exchange.jpg" "nao-money-exchange.jpg" "外貨" "ドル紙幣" "money-exchange"
upload "$BASE/finance/money-banknotes.jpg" "nao-money-notes.jpg" "紙幣" "各国の紙幣" "money-notes"
upload "$BASE/finance/mobile-banking.jpg" "nao-mobile-bank.jpg" "モバイルバンキング" "紙幣クローズアップ" "mobile-bank"

upload "$BASE/homepage/city-view.jpg" "nao-city-view.jpg" "街の風景" "遠くから見た街" "city-view"

upload "$BASE/general/starry-night.jpg" "nao-starry-night.jpg" "星空" "パラグアイの星空" "starry-night"
upload "$BASE/general/family-park.jpg" "nao-family-park.jpg" "子どもの遊び" "屋外の子どもたち" "family-park"

echo "" >> "$BASE/media-ids.json"
echo "}" >> "$BASE/media-ids.json"

echo ""
echo "=== Done ==="
cat "$BASE/media-ids.json"
