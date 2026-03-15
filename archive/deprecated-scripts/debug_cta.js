const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 12000));
    await pg.evaluate(() => document.querySelectorAll('.nao-anim').forEach(el => el.classList.add('nao-visible')));

    // Scroll to CTA and take element screenshot
    await pg.evaluate(() => document.querySelector('.nao-cta').scrollIntoView({block:'center'}));
    await new Promise(r => setTimeout(r, 1000));

    const ctaInfo = await pg.evaluate(() => {
        const cta = document.querySelector('.nao-cta');
        const s = getComputedStyle(cta);
        return {
            bg: s.backgroundColor,
            color: s.color,
            width: cta.getBoundingClientRect().width,
            height: cta.getBoundingClientRect().height,
            left: cta.getBoundingClientRect().left,
            padding: s.padding,
            innerHTML: cta.innerHTML.substring(0, 300),
            // Check if WP is wrapping content in <p> tags and breaking it
            childrenTags: Array.from(cta.children).map(c => c.tagName + '.' + c.className.substring(0,30))
        };
    });
    console.log(JSON.stringify(ctaInfo, null, 2));

    await pg.screenshot({path: 'c:/Users/tmizu/debug-cta.png'});
    await b.close();
})();
