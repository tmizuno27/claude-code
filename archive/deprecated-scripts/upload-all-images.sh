#!/bin/bash
# Upload all images to WordPress via multipart form
CREDS=$(echo -n 't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D' | base64)
BASE="C:/Users/tmizu/nambei-images"
MAPPING_FILE="C:/Users/tmizu/nambei-images/upload-mapping-curl.json"

# Initialize mapping file
echo "{" > "$MAPPING_FILE"
FIRST=true

upload_and_record() {
    local folder="$1"
    local filename="$2"
    local title="$3"
    local alt_text="$4"
    local filepath="$BASE/$folder/$filename"

    if [ ! -f "$filepath" ]; then
        echo "SKIP (not found): $folder/$filename"
        return
    fi

    local result=$(curl -sS -X POST "https://nambei-oyaji.com/wp-json/wp/v2/media" \
        -H "Authorization: Basic $CREDS" \
        -F "file=@${filepath};type=image/jpeg" \
        -F "title=$title" \
        -F "alt_text=$alt_text" \
        2>&1)

    local media_id=$(echo "$result" | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://')

    if [ -n "$media_id" ] && [ "$media_id" != "" ]; then
        echo "OK (ID:$media_id): $folder/$filename"
        # Append to mapping file
        if [ "$FIRST" = true ]; then
            FIRST=false
        else
            echo "," >> "$MAPPING_FILE"
        fi
        echo "  \"$folder/$filename\": $media_id" >> "$MAPPING_FILE"
    else
        echo "FAILED: $folder/$filename"
        echo "  Response: $(echo "$result" | head -c 200)"
    fi

    sleep 0.5
}

echo "=== Uploading all images to WordPress ==="
echo ""

# Paraguay Life
echo "--- Paraguay Life ---"
upload_and_record "paraguay-life" "asuncion-city.jpg" "アスンシオンの街並み" "パラグアイの首都アスンシオンの夜景"
upload_and_record "paraguay-life" "paraguay-building.jpg" "パラグアイの建物" "パラグアイの白い建物と緑の芝"
upload_and_record "paraguay-life" "paraguay-nature.jpg" "パラグアイの自然" "パラグアイの水辺と緑の風景"
upload_and_record "paraguay-life" "asado-bbq.jpg" "アサードBBQ" "南米式バーベキュー"
upload_and_record "paraguay-life" "bbq-cooking.jpg" "アサード調理" "グリルで肉を焼く"
upload_and_record "paraguay-life" "latin-street.jpg" "南米の街並み" "南米の教会と緑の木々"

# Immigration
echo ""
echo "--- Immigration ---"
upload_and_record "immigration" "passport-documents.jpg" "パスポートと渡航書類" "パスポートの写真"
upload_and_record "immigration" "passport-book.jpg" "パスポート" "パスポートブック"
upload_and_record "immigration" "airplane-wing.jpg" "飛行機の翼" "飛行機の翼と空"

# Remote Work
echo ""
echo "--- Remote Work ---"
upload_and_record "remote-work" "remote-work-laptop.jpg" "リモートワーク" "リモートワークのノートパソコン"
upload_and_record "remote-work" "desk-laptop.jpg" "デスクワーク" "デスクでノートパソコンを使う"
upload_and_record "remote-work" "laptop-coffee.jpg" "ノートPCとコーヒー" "ノートパソコンとコーヒー"
upload_and_record "remote-work" "laptop-silver.jpg" "シルバーのノートPC" "シルバーのノートパソコン"

# Family & Education
echo ""
echo "--- Family & Education ---"
upload_and_record "family-education" "school-children.jpg" "学校の子どもたち" "教室の子どもたち"
upload_and_record "family-education" "children-desks.jpg" "授業中の子ども" "机に座る子どもたち"
upload_and_record "family-education" "family-outdoor.jpg" "家族お出かけ" "屋外で遊ぶ子どもたち"
upload_and_record "family-education" "family-picnic.jpg" "子どもたちの自然体験" "草原の子どもたち"
upload_and_record "family-education" "children-playground.jpg" "子どもの遊び場" "広場で遊ぶ子どもたち"

# Finance
echo ""
echo "--- Finance ---"
upload_and_record "finance" "money-exchange.jpg" "外貨" "ドル紙幣"
upload_and_record "finance" "money-banknotes.jpg" "紙幣" "各国の紙幣"
upload_and_record "finance" "mobile-banking.jpg" "モバイルバンキング" "紙幣のクローズアップ"

# Homepage
echo ""
echo "--- Homepage ---"
upload_and_record "homepage" "city-view.jpg" "街の風景" "遠くから見た街"

# General
echo ""
echo "--- General ---"
upload_and_record "general" "starry-night.jpg" "星空" "パラグアイの星空"
upload_and_record "general" "meat-grill.jpg" "グリル肉" "グリルで肉を焼く"
upload_and_record "general" "family-park.jpg" "子どもの遊び" "屋外で遊ぶ子どもたち"

# Close mapping file
echo "" >> "$MAPPING_FILE"
echo "}" >> "$MAPPING_FILE"

echo ""
echo "=== Upload complete ==="
echo "Mapping saved to: $MAPPING_FILE"
