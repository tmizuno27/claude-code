const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));
    await pg.screenshot({path:'c:/Users/tmizu/live-top-final.png', fullPage:false});
    console.log('Title:', await pg.title());
    await b.close();
})();
