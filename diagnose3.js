const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));

    const diag = await pg.evaluate(() => {
        const results = {};

        // Check if script tags exist in entry-content
        const scripts = document.querySelectorAll('.entry-content script');
        results.scriptCount = scripts.length;
        if (scripts.length > 0) {
            results.scriptPreview = scripts[0].textContent.substring(0, 200);
        }

        // Check if nao-visible class was applied to any elements
        results.naoVisibleCount = document.querySelectorAll('.nao-visible').length;
        results.naoAnimCount = document.querySelectorAll('.nao-anim').length;

        // Check if latest posts were loaded
        const latest = document.getElementById('nao-latest-posts');
        if (latest) {
            results.latestPostsHTML = latest.innerHTML.substring(0, 200);
            results.latestPostCards = latest.querySelectorAll('.nao-post-card').length;
        }

        // Check value cards visibility
        const valueCards = document.querySelectorAll('.nao-value-card');
        results.valueCardCount = valueCards.length;
        if (valueCards.length > 0) {
            const cs = getComputedStyle(valueCards[0]);
            results.valueCard0 = {
                opacity: cs.opacity,
                transform: cs.transform,
                display: cs.display,
                hasVisible: valueCards[0].classList.contains('nao-visible')
            };
        }

        // Check if sidebar is overlapping
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            const rect = sidebar.getBoundingClientRect();
            results.sidebar = {
                display: getComputedStyle(sidebar).display,
                left: rect.left,
                width: rect.width,
                top: rect.top
            };
        }

        return results;
    });

    console.log(JSON.stringify(diag, null, 2));
    await b.close();
})();
