const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));

    // Check if .nao-home wrapper exists and styles are applied
    const diag = await pg.evaluate(() => {
        const home = document.querySelector('.nao-home');
        if (!home) return {error: 'no .nao-home'};

        // Check if entry-content wraps it, which might break full-width
        const ec = document.querySelector('.entry-content');
        const ecStyle = ec ? getComputedStyle(ec) : null;

        // Check nao-full elements
        const fulls = document.querySelectorAll('.nao-full');
        const fullInfo = [];
        fulls.forEach((f, i) => {
            const rect = f.getBoundingClientRect();
            const s = getComputedStyle(f);
            fullInfo.push({
                index: i,
                class: f.className.substring(0, 80),
                width: rect.width,
                height: rect.height,
                display: s.display,
                position: s.position,
                left: s.left,
                transform: s.transform
            });
        });

        // Check computed style on .nao-home children
        const sections = home.children;
        const sectionInfo = [];
        for (let i = 0; i < Math.min(sections.length, 15); i++) {
            const s = sections[i];
            const rect = s.getBoundingClientRect();
            const cs = getComputedStyle(s);
            sectionInfo.push({
                index: i,
                tag: s.tagName,
                class: s.className.substring(0, 80),
                width: rect.width,
                height: rect.height,
                display: cs.display,
                bg: cs.backgroundColor.substring(0, 40),
                overflow: cs.overflow,
                visibility: cs.visibility
            });
        }

        return {
            entryContentMaxWidth: ecStyle ? ecStyle.maxWidth : 'N/A',
            entryContentWidth: ecStyle ? ecStyle.width : 'N/A',
            entryContentOverflow: ecStyle ? ecStyle.overflow : 'N/A',
            naoHomeWidth: getComputedStyle(home).width,
            fulls: fullInfo,
            sections: sectionInfo,
            styleTagCount: document.querySelectorAll('.entry-content style').length
        };
    });

    console.log(JSON.stringify(diag, null, 2));

    // Take screenshots of specific sections
    const heroEl = await pg.$('.nao-hero');
    if (heroEl) {
        await heroEl.screenshot({path: 'c:/Users/tmizu/diag-hero.png'});
        console.log('Hero screenshot saved');
    }

    // Scroll to value section
    await pg.evaluate(() => {
        const vs = document.querySelector('.nao-value-section');
        if (vs) vs.scrollIntoView();
    });
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path: 'c:/Users/tmizu/diag-value.png'});

    // Scroll to stats
    await pg.evaluate(() => {
        const vs = document.querySelector('.nao-stats-ribbon');
        if (vs) vs.scrollIntoView();
    });
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path: 'c:/Users/tmizu/diag-stats.png'});

    await b.close();
})();
