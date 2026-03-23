#!/bin/bash
# Download Unsplash images using curl
# Extract og:image base URL from photo pages, then download at 1200px

BASE="/c/Users/tmizu/nambei-images"
SUCCESS=0
FAIL=0

download_unsplash() {
    local folder="$1"
    local filename="$2"
    local photo_id="$3"
    local filepath="$BASE/$folder/$filename"

    mkdir -p "$BASE/$folder"

    if [ -f "$filepath" ] && [ $(stat -c%s "$filepath" 2>/dev/null || echo 0) -gt 10000 ]; then
        echo "SKIP (exists): $folder/$filename"
        SUCCESS=$((SUCCESS+1))
        return
    fi

    # Extract og:image URL from Unsplash photo page
    local og_url=$(curl -sL "https://unsplash.com/photos/$photo_id" | grep -o 'og:image" content="[^"]*"' | head -1 | sed 's/og:image" content="//' | sed 's/"$//')

    if [ -z "$og_url" ]; then
        echo "FAILED (no og:image): $folder/$filename"
        FAIL=$((FAIL+1))
        return
    fi

    # Extract base image URL (before ?)
    local base_url=$(echo "$og_url" | sed 's/&amp;/\&/g' | grep -o 'https://images.unsplash.com/photo-[^?]*')

    if [ -z "$base_url" ]; then
        echo "FAILED (no base URL): $folder/$filename"
        FAIL=$((FAIL+1))
        return
    fi

    # Download at 1200px width
    local download_url="${base_url}?w=1200&q=80&auto=format&fit=crop"
    curl -sL -o "$filepath" "$download_url"

    local size=$(stat -c%s "$filepath" 2>/dev/null || echo 0)
    if [ "$size" -gt 10000 ]; then
        echo "OK (${size} bytes): $folder/$filename"
        SUCCESS=$((SUCCESS+1))
    else
        echo "FAILED (too small ${size}b): $folder/$filename"
        rm -f "$filepath"
        FAIL=$((FAIL+1))
    fi

    sleep 1
}

echo "=== Paraguay Life ==="
download_unsplash "paraguay-life" "asuncion-aerial.jpg" "YdoBxW3Wyfw"
download_unsplash "paraguay-life" "asuncion-city.jpg" "oqkFQjB10sE"
download_unsplash "paraguay-life" "paraguay-building.jpg" "vlsbdUGONAU"
download_unsplash "paraguay-life" "paraguay-nature.jpg" "aRojbOaBiKg"
download_unsplash "paraguay-life" "asado-bbq.jpg" "uIiMSu88RZQ"
download_unsplash "paraguay-life" "bbq-cooking.jpg" "pZyDC7BVN7s"
download_unsplash "paraguay-life" "latin-street.jpg" "5zqhGcQTMQU"

echo ""
echo "=== Immigration ==="
download_unsplash "immigration" "passport-documents.jpg" "rHBbnVLoWuY"
download_unsplash "immigration" "passport-book.jpg" "gMJ3tFOLvnA"
download_unsplash "immigration" "airplane-window.jpg" "gdxOGN_fTjE"
download_unsplash "immigration" "airplane-wing.jpg" "NrxINA10fQg"
download_unsplash "immigration" "airplane-city-view.jpg" "mLDJLlx_ei4"

echo ""
echo "=== Remote Work ==="
download_unsplash "remote-work" "remote-work-laptop.jpg" "ub3-qbPvRLc"
download_unsplash "remote-work" "desk-laptop.jpg" "Ki_pIEtS6pk"
download_unsplash "remote-work" "laptop-wooden-table.jpg" "7ZWVnVSaafY"
download_unsplash "remote-work" "laptop-coffee.jpg" "vE5Pxaaw6g0"
download_unsplash "remote-work" "laptop-silver.jpg" "e-uz4ozRqc0"

echo ""
echo "=== Family & Education ==="
download_unsplash "family-education" "school-classroom.jpg" "jEEYZsaxbH4"
download_unsplash "family-education" "school-children.jpg" "N_aihp118p8"
download_unsplash "family-education" "children-desks.jpg" "xmgvQdoo6Sg"
download_unsplash "family-education" "family-outdoor.jpg" "qbGAavRDlus"
download_unsplash "family-education" "family-picnic.jpg" "XtfWBR2jshg"
download_unsplash "family-education" "children-playground.jpg" "cL2ElgHHUSc"

echo ""
echo "=== Finance ==="
download_unsplash "finance" "money-exchange.jpg" "8lnbXtxFGZw"
download_unsplash "finance" "money-banknotes.jpg" "-ca8YHMKxFU"
download_unsplash "finance" "mobile-banking.jpg" "CTsI2OuMYaM"

echo ""
echo "=== Homepage ==="
download_unsplash "homepage" "hero-landscape.jpg" "78A265wPiO4"
download_unsplash "homepage" "city-view.jpg" "ITahX43XmuE"

echo ""
echo "=== General ==="
download_unsplash "general" "starry-night.jpg" "GvCNfC4j1-A"
download_unsplash "general" "meat-grill.jpg" "51mrkwMbuBc"
download_unsplash "general" "family-park.jpg" "jPp7KoOBVSk"

echo ""
echo "=== RESULTS: $SUCCESS success, $FAIL failed ==="
echo ""
echo "=== Files ==="
for dir in "$BASE"/*/; do
    dirname=$(basename "$dir")
    echo ""
    echo "$dirname/:"
    ls -lh "$dir" 2>/dev/null | grep -v "^total"
done
