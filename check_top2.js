const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:3000});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));

    // Check what's in entry-content
    const info = await pg.evaluate(() => {
        const ec = document.querySelector('.entry-content');
        if (!ec) return {error: 'no .entry-content'};
        const html = ec.innerHTML;
        return {
            length: html.length,
            first500: html.substring(0, 500),
            childCount: ec.children.length,
            visibleHeight: ec.getBoundingClientRect().height
        };
    });
    console.log(JSON.stringify(info, null, 2));

    // Take screenshot at 800px scroll
    await pg.evaluate(() => window.scrollTo(0, 400));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path:'c:/Users/tmizu/live-top-scroll.png'});

    await b.close();
})();
