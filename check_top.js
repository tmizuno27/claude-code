const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));
    await pg.screenshot({path:'c:/Users/tmizu/live-top-restored.png', fullPage:false});
    const title = await pg.title();
    console.log('Title:', title);
    const heroExists = await pg.evaluate(() => {
        return document.querySelector('.nao-hero') !== null || document.querySelector('.hero') !== null;
    });
    console.log('Hero section exists:', heroExists);
    const contentLen = await pg.evaluate(() => document.querySelector('.entry-content')?.innerHTML?.length || 0);
    console.log('Content length:', contentLen);
    await b.close();
})();
