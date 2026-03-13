const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 12000));
    await pg.evaluate(() => document.querySelectorAll('.nao-anim').forEach(el => el.classList.add('nao-visible')));

    const info = await pg.evaluate(() => {
        const cta = document.querySelector('.nao-cta');
        if (!cta) return {error: 'no cta'};

        const ctaRect = cta.getBoundingClientRect();
        const ctaStyle = getComputedStyle(cta);

        // Walk up the DOM tree to find what clips
        const ancestors = [];
        let el = cta.parentElement;
        while (el && el !== document.body) {
            const s = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            ancestors.push({
                tag: el.tagName,
                class: el.className.substring(0, 60),
                width: r.width,
                overflow: s.overflow,
                overflowX: s.overflowX,
                maxWidth: s.maxWidth,
                position: s.position
            });
            el = el.parentElement;
        }

        return {
            ctaWidth: ctaRect.width,
            ctaLeft: ctaRect.left,
            ctaPosition: ctaStyle.position,
            ctaTransform: ctaStyle.transform,
            ancestors: ancestors
        };
    });

    console.log(JSON.stringify(info, null, 2));
    await b.close();
})();
