const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 12000));

    // Check state
    const state = await pg.evaluate(() => ({
        naoVisibleCount: document.querySelectorAll('.nao-visible').length,
        naoAnimCount: document.querySelectorAll('.nao-anim').length,
        sidebarDisplay: document.getElementById('sidebar') ? getComputedStyle(document.getElementById('sidebar')).display : 'none',
        latestPosts: document.querySelectorAll('.nao-post-card').length,
        valueCardOpacity: document.querySelector('.nao-value-card') ? getComputedStyle(document.querySelector('.nao-value-card')).opacity : 'N/A'
    }));
    console.log(JSON.stringify(state, null, 2));

    // Screenshots
    await pg.screenshot({path: 'c:/Users/tmizu/home-1-hero.png'});

    await pg.evaluate(() => window.scrollTo(0, 800));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-2-latest.png'});

    await pg.evaluate(() => window.scrollTo(0, 1800));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-3-value.png'});

    await pg.evaluate(() => window.scrollTo(0, 2600));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-4-stats.png'});

    await pg.evaluate(() => window.scrollTo(0, 3600));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-5-pillars.png'});

    await pg.evaluate(() => window.scrollTo(0, 5000));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-6-about.png'});

    await pg.evaluate(() => window.scrollTo(0, 6500));
    await new Promise(r => setTimeout(r, 2000));
    await pg.screenshot({path: 'c:/Users/tmizu/home-7-cta.png'});

    await b.close();
})();
